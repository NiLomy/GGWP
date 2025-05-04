#!/usr/bin/env python3

# ЗАПУСК: python import_igdb.py --client-id 8wqmm7x1n2xxtnz94lb8mthadhtgrt --token ovbq0hwscv58hu46yxn50hovt4j8kj

import os
import sys
import argparse
import time
import django
import requests

# --- Настройка Django ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ggwp.settings')
django.setup()

from django.db import transaction
from games.models import Genre, Game

# --- Аргументы ---
parser = argparse.ArgumentParser(description='Import genres and games from IGDB')
parser.add_argument('--client-id',  required=True)
parser.add_argument('--token',      required=True)
parser.add_argument('--total-games', type=int, default=1000)
parser.add_argument('--batch-size',  type=int, default=500)
parser.add_argument('--clear',       action='store_true',
                    help='Если указан, перед импортом очищает таблицы Genre и Game')
args = parser.parse_args()

IGDB_API_URL     = 'https://api.igdb.com/v4'
RATE_LIMIT_DELAY = 0.3  # 4 запроса в сек → 0.25 с запасом

def rate_limited_post(endpoint: str, body: str):
    time.sleep(RATE_LIMIT_DELAY)
    headers = {
        'Client-ID':     args.client_id,
        'Authorization': f'Bearer {args.token}',
        'Accept':        'application/json',
        'Content-Type':  'text/plain',
    }
    url = f'{IGDB_API_URL}/{endpoint}'
    resp = requests.post(url, headers=headers, data=body)
    resp.raise_for_status()
    return resp.json()

def clear_tables():
    print('Clearing tables...')
    with transaction.atomic():
        Game.objects.all().delete()
        Genre.objects.all().delete()
    print('Tables cleared.')

def fetch_genres():
    print('Fetching genres…')
    body = 'fields name; limit 500;'
    data = rate_limited_post('genres', body)
    with transaction.atomic():
        for item in data:
            name = item.get('name')
            if not name:
                continue
            Genre.objects.update_or_create(
                id=item['id'],
                defaults={'name': name}
            )
    print(f'Imported {Genre.objects.count()} genres.')

def fetch_release_dates(ids):
    """
    Возвращает словарь { game_id: earliest_unix_date }
    по списку release_date IDs, делая запросы пачками по 500.
    """
    rd_map = {}
    # Убираем дубли и готовим список
    unique_ids = list(set(ids))
    batch_size = 500

    # Разбиваем на чанки по 500
    for i in range(0, len(unique_ids), batch_size):
        chunk = unique_ids[i:i + batch_size]
        ids_str = ','.join(str(x) for x in chunk)
        body = f'fields date,game; where id = ({ids_str}); limit {len(chunk)};'
        data = rate_limited_post('release_dates', body)

        # Обрабатываем ответ
        for rd in data:
            game_id = rd.get('game')
            date_unix = rd.get('date')
            if not (game_id and date_unix):
                continue
            prev = rd_map.get(game_id)
            rd_map[game_id] = min(prev, date_unix) if prev else date_unix

    return rd_map

def fetch_games(total, page_size):
    print(f'Fetching {total} games in batches of {page_size}…')
    offset = 0
    fetched = 0
    while fetched < total:
        batch = min(page_size, total - fetched)
        body = (
            f'fields name,summary,storyline,release_dates,rating,genres; '
            f'offset {offset}; limit {batch};'
        )
        items = rate_limited_post('games', body)

        rd_ids = []
        for it in items:
            rd_ids.extend(it.get('release_dates', []))
        rd_map = fetch_release_dates(rd_ids)

        with transaction.atomic():
            for it in items:
                gid = it.get('id')
                if not gid:
                    continue
                unix_ts = rd_map.get(gid)
                release_date = time.strftime('%Y-%m-%d', time.gmtime(unix_ts)) if unix_ts else None

                game_obj, _ = Game.objects.update_or_create(
                    id=gid,
                    defaults={
                        'name':         it.get('name', ''),
                        'description':  it.get('storyline',''),
                        'release_date': release_date,
                        'rating':       it.get('rating'),
                    }
                )
                if 'genres' in it and hasattr(game_obj, 'genres'):
                    game_obj.genres.set(it['genres'])

        fetched += len(items)
        offset  += len(items)
        print(f'  → Imported {fetched}/{total} games…')
    print('Done importing games.')

if __name__ == '__main__':
    if args.clear:
        clear_tables()
    fetch_genres()
    fetch_games(args.total_games, args.batch_size)