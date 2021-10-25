from .app import create_app
import click
import logging
from waitress import serve

from .config import Config
from .editor import set_config


def run_normal() -> None:
    set_config(Config)
    app = create_app(Config)
    # disable logging for every get/post request
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    print("Starting Manim Editor. Open http://localhost:5000 in a browser. (Press CTRL+C to quit)")
    serve(app, host="0.0.0.0", port=5000)


def run_debug() -> None:
    Config.set("FFMPEG_LOGLEVEL", "info")
    set_config(Config)
    app = create_app(Config)
    app.run(debug=True)


@click.command()
@click.option("--debug", is_flag=True, help="Launch in Debug mode.")
def main(debug) -> None:
    if (debug):
        run_debug()
    else:
        run_normal()


if __name__ == "__main__":
    main()
