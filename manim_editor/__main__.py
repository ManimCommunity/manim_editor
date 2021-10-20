from .app import create_app
import click


@click.command()
@click.option("--debug", help="Launch Flask in Debug mode.")
def main(debug=False):
    app = create_app()
    app.run(debug=debug)


if __name__ == "__main__":
    main()
