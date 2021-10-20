from flask import Flask

from ..config import Config


def create_app(config=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    # blueprints
    from .error import bp as errors_bp
    app.register_blueprint(errors_bp)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
