import os
from pathlib import Path
from voyager import Index, Space

index = None
index_path = "res/game_index.voyager"


def get_index(path: str = index_path) -> Index:
    global index

    if index is None:
        if not Path(path).exists():
            raise FileNotFoundError(f"Index file not found: {path}")

        with open(path, 'rb') as f:
            index = Index.load(f)

    return index


def create_index(path: str = index_path) -> Index:
    global index

    if not os.path.exists(path):
        with open(path, 'w+'): pass

    index = Index(Space.Cosine, num_dimensions=384, M=16, ef_construction=400)
    index.save(path)

    return index


def save_index(new_index: Index, path: str = index_path) -> Index:
    global index

    if not os.path.exists(path):
        with open(path, 'w+'): pass

    index = new_index
    index.save(path)

    return index
