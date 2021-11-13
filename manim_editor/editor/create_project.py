"""Create Manim Editor project."""
import json
import os
from pathlib import Path
from typing import List, Tuple

from .manim_loader import get_scenes
from .presentation_classes import Section, Slide

__all__ = ["create_project_dir", "populate_project_with_loaded_sections", "populate_project"]


def create_project_dir(project_name: str) -> Tuple[bool, str]:
    """Ensure existence of project dir.
    Return True if success and message for the user.
    """
    print(f"Creating project '{project_name}'.")
    # TODO: valid dir name check for Windows
    if project_name == "":
        return False, "The project name can't be empty."
    if os.path.exists(project_name):
        # empty dirs are ok
        if len(os.listdir(project_name)) == 0:
            return True, f"The project directory '{project_name}' has already been created. It will be used."
        return (
            False,
            f"The project name '{project_name}' points to a filled directory. If this is a project, you can open it instead.",
        )
    try:
        os.mkdir(project_name)
    except FileNotFoundError:
        return False, f"Creation of project directory '{project_name}' failed."
    return True, f"Created new project directory '{project_name}'."


def populate_project_with_loaded_sections(project_name: str, sections: List[Section]) -> bool:
    if not len(sections):
        raise RuntimeError(f"No sections given for project '{project_name}'.")
    if sections[0].is_sub_section:
        raise RuntimeError(f"The first section of project '{project_name}' can't be a sub section.")

    # load slides
    slides: List[Slide] = []
    for id, section in enumerate(sections):
        # add sub section
        if section.is_sub_section:
            if not slides[-1].populate_sub_section(section):
                return False
        else:
            # set main section
            slides.append(Slide())
            if not slides[-1].populate_main_section(section, project_name, id):
                return False

    # write project file
    with open(Path(project_name) / "project.json", "w") as file:
        json.dump([slide.get_dict() for slide in slides], file, indent=4)
    return True


def populate_project(project_name: str, scene_ids: List[int]) -> bool:
    """Create project JSON file, copy selected section video files and create thumbnails.
    Return False at failure.
    """
    print(f"Populating project '{project_name}'.")
    # select scenes according to ids set by frontend
    scenes = [scene for scene in get_scenes() if scene.id in scene_ids]
    sections: List[Section] = []
    for scene in scenes:
        sections += scene.sections

    success = populate_project_with_loaded_sections(project_name, sections)
    if success:
        # xD
        print(f"Project '{project_name}' population finished.")
    else:
        print(f"Project '{project_name}' population failed.")
    return success
