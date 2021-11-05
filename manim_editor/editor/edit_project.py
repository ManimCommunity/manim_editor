import jinja2
import os
from distutils.dir_util import copy_tree
from typing import List

from .config import get_config
from .scene import Section


def emulate_url_for(endpoint: str, path: str = "", name: str = "", filename: str = "") -> str:
    """Translate flask urls into local urls for project.
    ``name`` is being ignored as the output path will be from the project dir already.
    """
    if endpoint == "static":
        return filename
    elif endpoint == "main.serve_project_static":
        return path
    raise ValueError(f"Endpoint '{endpoint}' can't be emulated.")


def export_presentation(project_name: str, sections: List[Section]) -> None:
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([
            os.path.join(get_config().ROOT_DIR, "app", "templates"),
            os.path.join(get_config().ROOT_DIR, "app", "main", "templates"),
            os.path.join(get_config().ROOT_DIR, "app", "error", "templates"),
        ]),
        autoescape=jinja2.select_autoescape(["html"])
    )

    html = jinja2_env.get_template("edit_project.html").render(
        present_export=True,
        version=get_config().VERSION,
        name=project_name,
        sections=sections,
        url_for=emulate_url_for
    )
    with open(os.path.join(project_name, "index.html"), "w") as file:
        file.write(html)
    copy_tree(os.path.join(get_config().ROOT_DIR, "app", "static", "webpack"), os.path.join(project_name, "webpack"))
    copy_tree(os.path.join(get_config().ROOT_DIR, "app", "static", "img"), os.path.join(project_name, "img"))
