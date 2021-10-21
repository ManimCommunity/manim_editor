import os
from typing import List
from .section import get_index, Index


def get_indices(path=".") -> List[Index]:
    """Search recursively in ``path`` for any valid JSON section index files."""
    raw_indices: List[str] = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".json"):
                raw_indices.append(os.path.join(root, file))

    indices: List[Index] = []
    for raw_index in raw_indices:
        index = get_index(raw_index)
        if index is not None:
            indices.append(index)
    return indices
