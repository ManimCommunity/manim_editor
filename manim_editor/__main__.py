import logging
import socket
from pathlib import Path
from typing import List, Optional

import click
from waitress import serve

from .app import create_app
from .config import Config
from .editor import (
    Section,
    create_project_dir,
    export_presentation,
    get_project,
    get_scene,
    populate_project_with_loaded_sections,
    set_config,
)


def find_open_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    sock.listen(1)
    _, port = sock.getsockname()
    sock.close()

    return port


def run_normal() -> None:
    set_config(Config)
    app = create_app(Config)
    # disable logging for every get/post request
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    port = find_open_port()
    url = f"http://localhost:{port}"
    print(f"Starting Manim Editor {Config.VERSION}. Open {url} in a browser. (Press CTRL+C to quit)")
    serve(app, host="0.0.0.0", port=port)


def run_debug() -> None:
    Config.set("FFMPEG_LOGLEVEL", "info")
    set_config(Config)
    app = create_app(Config)
    app.run(debug=True)


def run_quick_present_export(section_index_paths: List[Path], project_name: Optional[str] = None) -> None:
    """Create a project from scene(s) and export the presentation.
    Using the name of the first project if ``project_name`` is not given.
    """
    set_config(Config)
    if project_name is None:
        project_name = section_index_paths[0].name[:-5]

    success, msg = create_project_dir(project_name)
    if not success:
        raise RuntimeError(msg)

    sections: List[Section] = []
    for section_index_path in section_index_paths:
        scene = get_scene(section_index_path, 0)
        if scene is None:
            raise RuntimeError(f"Couldn't find a section index file at '{section_index_path}'.")
        sections += scene.sections
    if not populate_project_with_loaded_sections(project_name, sections):
        raise RuntimeError("Failed to populate project.")
    project_name, slides = get_project(project_name)
    if project_name is None:
        raise RuntimeError("Failed to load project.")
    export_presentation(project_name, slides)


@click.command()
@click.option("--debug", is_flag=True, help="Launch in Debug mode.")
@click.option("--version", is_flag=True, help="Print version and exit.")
@click.option(
    "--quick_present_export",
    help="Create a project from a scene and export the presentation. The path to the section index file must be provided as the argument.",
    multiple=True,
)
@click.option(
    "--project_name", help="Use this name for the project being created use the name of the first section when not provided."
)
def main(debug: bool, version: bool, quick_present_export: List[str], project_name: Optional[str]) -> None:
    if version:
        print(f"Manim Editor {Config.VERSION}")
        return
    if len(quick_present_export):
        run_quick_present_export([Path(section_index_path) for section_index_path in quick_present_export], project_name)
        return
    if debug:
        run_debug()
    else:
        run_normal()
