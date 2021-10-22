import os
from .app import create_app
import click
import logging
from waitress import serve

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def set_dotenv() -> None:
    dotenv = os.path.join(BASEDIR, ".env")
    if not os.path.exists(dotenv):
        print("Creating '.env' file with SECRET_KEY")
        with open(dotenv, "w") as file:
            file.write(f"SECRET_KEY={os.urandom(16)}")


@click.command()
@click.option("--debug", is_flag=True, help="Launch Flask in Debug mode.")
def main(debug) -> None:
    set_dotenv()
    app = create_app()
    if debug:
        app.run(debug=True)
    else:
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)
        print("Starting Manim Editor. Open http://localhost:5000 in a browser. (Press CTRL+C to quit)")
        serve(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
