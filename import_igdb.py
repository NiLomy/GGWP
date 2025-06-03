#!/usr/bin/env python3

# ЗАПУСК: python import_igdb.py --clear --client-id 8wqmm7x1n2xxtnz94lb8mthadhtgrt --client-secret ovbq0hwscv58hu46yxn50hovt4j8kj

import os
import sys
import argparse
import time
import django
import requests
from voyager import Index

from index import create_index, save_index, get_index

# --- Настройка Django ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ggwp.settings')
django.setup()

from django.db import transaction
from games.models import Genre, Game

# --- Аргументы ---
parser = argparse.ArgumentParser(description='Import genres and games from IGDB')
parser.add_argument('--client-id',     required=True)
parser.add_argument('--client-secret', required=True)
parser.add_argument('--total-games',   type=int, default=1000)
parser.add_argument('--batch-size',    type=int, default=500)
parser.add_argument('--clear',         action='store_true',
                    help='Если указан, перед импортом очищает таблицы Genre и Game')
args = parser.parse_args()

IGDB_API_URL     = 'https://api.igdb.com/v4'
RATE_LIMIT_DELAY = 0.3  # 4 запроса в сек → 0.25 с запасом

access_token = None

COVER_SIZE = "cover_big_2x"  # https://api-docs.igdb.com/#images

def auth():
    global access_token
    auth_url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": args.client_id,
        "client_secret": args.client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(auth_url, params=params)
    access_token = response.json().get("access_token")

def rate_limited_post(endpoint: str, body: str):
    global access_token
    if access_token is None:
        auth()

    time.sleep(RATE_LIMIT_DELAY)
    headers = {
        'Client-ID':     args.client_id,
        'Authorization': f'Bearer {access_token}',
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

def fetch_games(total, page_size) -> list[Game]:
    print(f'Fetching {total} games in batches of {page_size}…')
    offset = 0
    fetched = 0
    games = []
    while fetched < total:
        batch = min(page_size, total - fetched)
        body = (
            f'fields name,summary,storyline,first_release_date,rating,genres,cover.image_id;'
            f'where summary != null & storyline != null & first_release_date != null & game_type = 0;'
            f'sort rating desc; offset {offset}; limit {batch};'
        )
        items = rate_limited_post('games', body)

        with transaction.atomic():
            for it in items:
                gid = it.get('id')
                if not gid:
                    continue
                unix_ts = it.get('first_release_date')
                release_date = time.strftime('%Y-%m-%d', time.gmtime(float(unix_ts))) if unix_ts else None

                # https://api-docs.igdb.com/#images
                cover_id = it.get('cover', {}).get('image_id', '')
                if cover_id:
                    cover_url = f"https://images.igdb.com/igdb/image/upload/t_{COVER_SIZE}/{cover_id}.jpg"
                else:
                    cover_url = ""

                game_obj, _ = Game.objects.update_or_create(
                    id=gid,
                    defaults={
                        'name':         it.get('name', ''),
                        'description':  it.get('summary', ''),
                        'storyline':    it.get('storyline', ''),
                        'release_date': release_date,
                        'image_url':    cover_url,
                        'rating':       it.get('rating'),
                    }
                )
                games.append(game_obj)
                if 'genres' in it and hasattr(game_obj, 'genres'):
                    game_obj.genres.set(it['genres'])

        fetched += len(items)
        offset += len(items)
        print(f'  → Imported {fetched}/{total} games…')
    print('Done importing games.')
    return games

def fill_index(games: list[Game], index: Index):
    print("Loading transformer...")
    from sentence_transformers import SentenceTransformer
    transformer = SentenceTransformer('all-MiniLM-L6-v2')

    print("Embedding descriptions...")
    summaries = [f"{game.description} {game.storyline}" for game in games]
    embeddings = transformer.encode(summaries)

    print("Filling index...")
    ids = [game.id for game in games]
    index.add_items(embeddings, ids=ids)
    save_index(index)

    print("Done creating index.")

if __name__ == '__main__':
    if args.clear:
        clear_tables()
        index = create_index()
    else:
        index = get_index()
    fetch_genres()
    games = fetch_games(args.total_games, args.batch_size)
    fill_index(games, index)
