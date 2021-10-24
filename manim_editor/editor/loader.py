import os
from pathlib import Path
from typing import List, Optional, Any, Dict
import json
from collections.abc import Iterable
from fractions import Fraction

from .scene import Section, Scene


def get_section(raw_section: Dict[str, Any], index_path: str, new_id: int) -> Optional[Section]:
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
        # Hodaka laesst gruessen
        "duration": str,
        "nb_frames": str,
    }.items():
        if key not in raw_section:
            return None
        if type(raw_section[key]) is not req_type:
            return None

    parent_path = Path(index_path).parent.absolute()
    return Section(
        new_id,
        raw_section["name"],
        raw_section["type"],
        os.path.join(parent_path, raw_section["video"]),
        int(raw_section["width"]),
        int(raw_section["height"]),
        Fraction(raw_section["avg_frame_rate"]),
        float(raw_section["duration"]),
    )


def get_scene(path: str, new_id: int) -> Optional[Scene]:
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
        section = get_section(raw_section, path, len(sections))
        if section is None:
            return None
        sections.append(section)
    return Scene(
        new_id,
        os.path.basename(path)[:-5],
        os.path.abspath(path),
        os.path.getmtime(path),
        sections)


def get_scenes(path=".") -> List[Scene]:
    """Search recursively in ``path`` for any valid JSON section index files."""
    raw_scenes: List[str] = []
    # TODO: add depth limit
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".json"):
                raw_scenes.append(os.path.join(root, file))

    scenes: List[Scene] = []
    for raw_scene in raw_scenes:
        scene = get_scene(raw_scene, len(scenes))
        if scene is not None:
            scenes.append(scene)
    return scenes
