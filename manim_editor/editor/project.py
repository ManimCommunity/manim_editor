import os
import json
import pathlib
from fractions import Fraction
from typing import Any, Dict, Tuple, List, Optional

from .manim_loader import get_scenes, Section, valid_json_load
from .commands import walk
from .config import get_config


def create_project_dir(project_name: str) -> Tuple[bool, str]:
    """Ensure existence of project dir. Return True if success and error or success message."""
    print(f"Creating project '{project_name}'.")
    # TODO: valid dir name check for Windows
    if project_name == "":
        return False, "The project name can't be empty."
    if os.path.exists(project_name):
        # empty dirs are ok
        if len(os.listdir(project_name)) == 0:
            return True, f"The project directory '{project_name}' has already been created. It will be used."
        return False, f"The project name '{project_name}' points to a filled directory."
    try:
        os.mkdir(project_name)
    except FileNotFoundError:
        return False, f"Creation of project directory '{project_name}' failed."
    return True, f"Created new project directory '{project_name}'."


class SectionId:
    def __init__(self, scene_id: int, section_id: int):
        self.scene_id = scene_id
        self.section_id = section_id


def populate_project(project_name: str, section_ids: List[SectionId]) -> bool:
    """Create project JSON file, copy selected section video files and create thumbnails.
    Return False at failure."""
    print(f"Populating project '{project_name}'.")
    # TODO: could theoretically be cached
    scenes = get_scenes()
    sections: List[Section] = []
    for section in section_ids:
        sections.append(scenes[section.scene_id].sections[section.section_id])

    project: List[Dict[str, Any]] = []

    # prepare section
    for id, section in enumerate(sections):
        section.set_project(project_name, id)
        section.copy_video()
        if not section.create_thumbnail():
            return False
        project.append(section.get_dict())

    # write project file
    with open(os.path.join(project_name, "project.json"), "w") as file:
        json.dump(project, file, indent=4)
    return True


class Project:
    def __init__(self, name: str, sections: List[Section]):
        self.name = name
        self.sections = sections


def get_project_section(raw_section: Dict[str, Any]) -> Section:
    """Create :class:`.Section` from dict read from a project json file created by the Manim Editor."""

    return Section(
        int(raw_section["id"]),
        raw_section["name"],
        # TODO: should be converted to PresentationsectionType
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
    """Get all projects in the current working directory."""
    # get all projects in this dir
    project_paths: List[str] = []
    for root, _, files in walk(".", 1):
        for file in files:
            if file == "project.json":
                project_paths.append(os.path.join(root, file))
    projects: List[Project] = []
    for project_path in project_paths:
        project = get_project(project_path)
        if project is not None:
            projects.append(project)
    return projects
