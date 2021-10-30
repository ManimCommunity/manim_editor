import os
import click
import logging
from waitress import serve
import socket
from typing import Optional

from .app import create_app
from .config import Config
from .editor import set_config, create_project_dir, get_scene, populate_project_with_loaded_sections, export_presentation


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
    print(f"Starting Manim Editor v{Config.VERSION}. Open {url} in a browser. (Press CTRL+C to quit)")
    serve(app, host="0.0.0.0", port=port)


def run_debug() -> None:
    Config.set("FFMPEG_LOGLEVEL", "info")
    set_config(Config)
    app = create_app(Config)
    app.run(debug=True)


# TODO: quick test, this is only for testing purposes
def run_quick_present_export(section_index_path: str) -> None:
    """Create a project form a single scene and export the presentation."""
    Config.set("FFMPEG_LOGLEVEL", "info")
    set_config(Config)
    project_name = os.path.basename(section_index_path)[:-5]

    success, msg = create_project_dir(project_name)
    if not success:
        raise RuntimeError(msg)
    scene = get_scene(section_index_path, 0)
    if scene is None:
        raise RuntimeError(f"Couldn't find a section index file at '{section_index_path}'.")
    if not populate_project_with_loaded_sections(project_name, scene.sections):
        raise RuntimeError("Failed to populate project.")
    export_presentation(project_name, scene.sections)


@click.command()
@click.option("--debug", is_flag=True, help="Launch in Debug mode.")
@click.option("--version", is_flag=True, help="Print version and exit.")
@click.option("--quick_present_export", help="Create a project from a scene and export the presentation. The path to the section index file must be provided as the argument.")
def main(debug: bool, version: bool, quick_present_export: Optional[str]) -> None:
    if version:
        print(f"Manim Editor v{Config.VERSION}")
        return
    if quick_present_export is not None:
        run_quick_present_export(quick_present_export)
        return
    if debug:
        run_debug()
    else:
        run_normal()


if __name__ == "__main__":
    main()
