import os


def validate_project_name(project_name: str) -> bool:
    # TODO: valid dir name check for Windows
    if project_name == "":
        return False
    if os.path.exists(project_name):
        return False
    try:
        os.mkdir(project_name)
    except FileNotFoundError:
        return False
    return True
