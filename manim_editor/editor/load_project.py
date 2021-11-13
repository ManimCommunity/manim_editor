"""Load a Manim Editor project."""
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .commands import walk
from .config import get_config
from .manim_loader import valid_json_load
from .presentation_classes import Slide

__all__ = ["get_project", "get_projects"]


def get_project(name: str) -> Tuple[Optional[str], List[Slide]]:
    """Parse project json file if valid.
    ``path`` is path to prject dir, not to the json index file.
    Otherwise return ``None`` as name.
    """
    path = Path(name)
    raw_slides = valid_json_load(path / "project.json", get_config().PROJECT_SCHEMA)
    if raw_slides is None:
        return None, []
    slides: List[Slide] = []
    for raw_slide in raw_slides:
        slide = Slide()
        slide.load(raw_slide)
        slides.append(slide)
    return name, slides


def get_projects() -> Dict[str, List[Slide]]:
    """Get all projects in the current working directory.
    No recursive search will be applied."""
    # get all projects in this dir
    project_paths: List[Path] = []
    for root, _, files in walk(Path("."), 1):
        for file in files:
            if file == "project.json":
                project_paths.append(root)
    projects: Dict[str, List[Slide]] = {}
    for project_name in project_paths:
        name, slides = get_project(str(project_name))
        # don't include invalid
        if name is not None:
            projects[name] = slides
    return projects
