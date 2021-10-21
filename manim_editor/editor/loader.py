import os
from pathlib import Path
from typing import List, Optional, Any, Dict
import json
from collections.abc import Iterable

from .section import Section, Index


def get_section(raw_section: Dict[str, Any], index_path: str) -> Optional[Section]:
    """Create :class:`.Section` from dict read from an section index.
    Return ``None`` if dict is invalid. This happens when a JSON file that isn't a section index gets read.
    """

    for key, req_type in {
        "name": str,
        "type": str,
        "video": str,
        "codec_name": str,
        "width": int,
        "height": int,
        "avg_frame_rate": str,
        "duration": str,
        "nb_frames": str,
    }.items():
        if key not in raw_section:
            return None
        if type(raw_section[key]) is not req_type:
            return None

    parent_path = Path(index_path).parent.absolute()
    return Section(
        raw_section["name"],
        raw_section["type"],
        os.path.join(parent_path, raw_section["video"])
    )


def get_index(path: str) -> Optional[Index]:
    """Check if path points to a valid section index file.
    Return None if it is invalid. Return a list of :class:`.Section` otherwise.
    """
    with open(path, "r") as file:
        try:
            raw_sections = json.load(file)
        except json.decoder.JSONDecodeError:
            return None
    if not isinstance(raw_sections, Iterable):
        return None

    sections: List[Section] = []
    for raw_section in raw_sections:
        if not isinstance(raw_section, dict):
            return None
        section = get_section(raw_section, path)
        if section is None:
            return None
        sections.append(section)
    return Index(os.path.abspath(path), sections)


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
