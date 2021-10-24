import os
from typing import Tuple


def create_project_dir(project_name: str) -> Tuple[bool, str]:
    """Ensure existence of project dir. Return True if success and error or success message."""
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


def populate_project(project_name: str) -> bool:
    pass
