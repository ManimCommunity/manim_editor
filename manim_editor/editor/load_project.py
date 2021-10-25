"""Load a Manim Editor project."""
import os
import pathlib
from fractions import Fraction
from typing import Any, Dict, List, Optional

from .manim_loader import Section, valid_json_load
from .commands import walk
from .config import get_config


class Project:
    def __init__(self, name: str, sections: List[Section]):
        self.name = name
        self.sections = sections


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


def get_project(path: str) -> Optional[Project]:
    """Parse project json file if valid.
    Otherwise return ``None``.
    """
    raw_sections = valid_json_load(path, get_config().PROJECT_SCHEMA)
    if raw_sections is None:
        return None
    name = os.path.basename(pathlib.Path(path).parent)
    sections: List[Section] = []
    for raw_section in raw_sections:
        sections.append(get_project_section(raw_section))
    return Project(name, sections)


def get_projects() -> List[Project]:
    """Get all projects in the current working directory.
    No recursive search will be applied."""
    # get all projects in this dir
    project_paths: List[str] = []
    for root, _, files in walk(".", 1):
        for file in files:
            if file == "project.json":
                project_paths.append(os.path.join(root, file))
    projects: List[Project] = []
    for project_path in project_paths:
        project = get_project(project_path)
        # don't include invalid
        if project is not None:
            projects.append(project)
    return projects
