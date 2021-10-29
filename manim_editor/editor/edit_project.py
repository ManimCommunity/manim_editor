import jinja2
import pathlib
import os
from distutils.dir_util import copy_tree
from typing import List

from .config import get_config
from .scene import Section

BASE_DIR = pathlib.Path(__file__).parent.absolute()
ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader([
        os.path.join(BASE_DIR, "..", "app", "templates"),
        os.path.join(BASE_DIR, "..", "app", "main", "templates"),
        os.path.join(BASE_DIR, "..", "app", "error", "templates"),
    ]),
    autoescape=jinja2.select_autoescape(["html"])
)


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
    html = ENV.get_template("edit_project.html").render(
        present_export=True,
        version=get_config().VERSION,
        name=project_name,
        sections=sections,
        url_for=emulate_url_for
    )
    with open(os.path.join(project_name, "index.html"), "w") as file:
        file.write(html)
    copy_tree(os.path.join(BASE_DIR, "..", "app", "static", "webpack"), os.path.join(project_name, "webpack"))
    copy_tree(os.path.join(BASE_DIR, "..", "app", "static", "img"), os.path.join(project_name, "img"))
