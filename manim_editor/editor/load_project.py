"""Load a Manim Editor project."""
import os
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from .manim_loader import Section, valid_json_load
from .commands import walk
from .config import get_config


def get_project_section(raw_section: Dict[str, Any]) -> Section:
    """Create :class:`.Section` from dict read from a project json file created by the Manim Editor."""

    return Section(
        int(raw_section["id"]),
        raw_section["name"],
        # TODO: should be converted to PresentationSectionType
        raw_section["type"],
        raw_section["original_video"],
        int(raw_section["width"]),
        int(raw_section["height"]),
        Fraction(raw_section["fps"]),
        float(raw_section["duration"]),
        raw_section["project_name"],
        raw_section["in_project_video"],
        raw_section["in_project_thumbnail"],
        int(raw_section["in_project_id"]),
    )


def get_project(path: str) -> Tuple[Optional[str], List[Section]]:
    """Parse project json file if valid.
    ``path`` is path to prject dir, not to the json index file.
    Otherwise return ``None`` as name.
    """
    raw_sections = valid_json_load(os.path.join(path, "project.json"), get_config().PROJECT_SCHEMA)
    if raw_sections is None:
        return None, []
    name = os.path.basename(path)
    sections: List[Section] = []
    for raw_section in raw_sections:
        sections.append(get_project_section(raw_section))
    return name, sections


def get_projects() -> Dict[str, List[Section]]:
    """Get all projects in the current working directory.
    No recursive search will be applied."""
    # get all projects in this dir
    project_paths: List[str] = []
    for root, _, files in walk(".", 1):
        for file in files:
            if file == "project.json":
                project_paths.append(root)
    projects: Dict[str, List[Section]] = {}
    for project_path in project_paths:
        name, sections = get_project(project_path)
        # don't include invalid
        if name is not None:
            projects[name] = sections
    return projects
