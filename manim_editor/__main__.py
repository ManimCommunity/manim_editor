from .app import create_app
import click
import logging
from waitress import serve
import socket

from .config import Config
from .editor import set_config


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
    print(f"Starting Manim Editor. Open {url} in a browser. (Press CTRL+C to quit)")
    serve(app, host="0.0.0.0", port=port)


def run_debug() -> None:
    Config.set("FFMPEG_LOGLEVEL", "info")
    set_config(Config)
    app = create_app(Config)
    app.run(debug=True)


@click.command()
@click.option("--debug", is_flag=True, help="Launch in Debug mode.")
@click.option("--version", is_flag=True, help="Print version and exit.")
def main(debug: bool, version: bool) -> None:
    if version:
        print(f"Manim Editor v{Config.VERSION}")
        return
    if debug:
        run_debug()
    else:
        run_normal()


if __name__ == "__main__":
    main()
