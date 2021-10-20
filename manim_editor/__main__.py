from .app import create_app
import click


@click.command()
@click.option('--debug', is_flag=True, help="Launch Flask in Debug mode.")
def main(debug):
    app = create_app()
    app.run(debug=debug)


if __name__ == "__main__":
    main()
