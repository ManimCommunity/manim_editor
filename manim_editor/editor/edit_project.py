import jinja2
from pathlib import Path
from distutils.dir_util import copy_tree
from typing import List

from .config import get_config
from .scene import Section


def emulate_url_for(endpoint: str, path: str = "", name: str = "", filename: str = "") -> str:
    """Translate flask urls into local urls for project.
    Can't be ``Path`` since flask uses strings here.
    ``name`` is being ignored as the output path will be from the project dir already.
    """
    if endpoint == "static":
        return filename
    elif endpoint == "main.serve_project_static":
        return path
    raise ValueError(f"Endpoint '{endpoint}' can't be emulated.")


def export_presentation(project_name: str, sections: List[Section]) -> None:
    print(f"Exporting Project '{project_name}' as presentation.")
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([
            get_config().ROOT_DIR / "app" / "templates",
            get_config().ROOT_DIR / "app" / "main" / "templates",
            get_config().ROOT_DIR / "app" / "error" / "templates",
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
    with open(Path(project_name) / "index.html", "w") as file:
        file.write(html)
    copy_tree(get_config().ROOT_DIR / "app" / "static" / "webpack", str(Path(project_name) / "webpack"))
    copy_tree(get_config().ROOT_DIR / "app" / "static" / "img", str(Path(project_name) / "img"))
    print(f"Presentation is ready at '{Path(project_name).absolute()}'")
    print("Run 'python3 -m http.server' in that directory. Simply opening the .html file won't work.")
