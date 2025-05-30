# games/recommendation.py
from index import get_index
import numpy as np

RECOMMENDATIONS_COUNT = 10


def get_recommended_game_ids(game_id_1: int, game_id_2: int) -> list[int]:
    idx = get_index()

    queries = idx.get_vectors([game_id_1, game_id_2])
    final_query = np.sum(queries, axis=0)

    neighbor_ids, distances = idx.query(final_query, k=(RECOMMENDATIONS_COUNT + 2))

    return [game_id for game_id in neighbor_ids if game_id not in {game_id_1, game_id_2}][:RECOMMENDATIONS_COUNT]
