"""Functions used to load the render results of Manim."""
import os
from pathlib import Path
from typing import List, Optional, Any, Dict
from fractions import Fraction

from .scene import Section, Scene
from .config import get_config
from .commands import walk, valid_json_load


def get_manim_section(raw_section: Dict[str, Any], index_path: Path, new_id: int) -> Section:
    """Create :class:`.Section` from dict read from a section index created by Manim."""

    parent_path = index_path.parent.absolute()
    return Section(
        new_id,
        raw_section["name"],
        raw_section["type"],
        parent_path / raw_section["video"],
        int(raw_section["width"]),
        int(raw_section["height"]),
        Fraction(raw_section["avg_frame_rate"]),
        float(raw_section["duration"]),
    )


def get_scene(path: Path, new_id: int) -> Optional[Scene]:
    """Check if path points to a valid section index file.
    Return ``None`` if file isn't a section index.
    """
    raw_sections = valid_json_load(path, get_config().SECTION_INDEX_SCHEMA)
    if raw_sections is None:
        return None

    sections: List[Section] = []
    for raw_section in raw_sections:
        sections.append(get_manim_section(raw_section, path, len(sections)))
    return Scene(
        new_id,
        path.name[:-5],
        path.absolute(),
        os.path.getmtime(path),
        sections)


def get_scenes() -> List[Scene]:
    """Search recursively in CWD for any valid JSON section index files."""
    scene_index_paths: List[Path] = []
    for root, _, files in walk(Path("."), get_config().RECURSION_DEPTH):
        for file in files:
            if file.endswith(".json"):
                scene_index_paths.append(root / file)

    scenes: List[Scene] = []
    for scene_index_path in scene_index_paths:
        scene = get_scene(scene_index_path, len(scenes))
        # valid scene with at least one section?
        if scene is not None and len(scene.sections):
            scenes.append(scene)
    return scenes
