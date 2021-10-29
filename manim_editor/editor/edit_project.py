import jinja2
import pathlib
import os
from .config import get_config
from .load_project import get_project

BASE_DIR = pathlib.Path(__file__).parent.absolute()
ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader([
        os.path.join(BASE_DIR, "..", "app", "templates"),
        os.path.join(BASE_DIR, "..", "app", "main", "templates"),
        os.path.join(BASE_DIR, "..", "app", "error", "templates"),
    ]),
    autoescape=jinja2.select_autoescape(["html"])
)


def url_for_stub(*args, **kwargs):
    return "test"


def get_flashed_messages_stub(*args, **kwargs):
    return {}


def test():
    name = "test"
    project_name, sections = get_project(os.path.join(name, "project.json"))
    return ENV.get_template("edit_project.html").render(version=get_config().VERSION, title="Edit Project", name=name, sections=sections, url_for=url_for_stub, get_flashed_messages=get_flashed_messages_stub)
