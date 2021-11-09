from flask import render_template

from . import bp


@bp.app_errorhandler(400)
def bad_request(_):
    return render_template("400.html"), 401


@bp.app_errorhandler(401)
def access_denied_error(_):
    return render_template("401.html"), 401


@bp.app_errorhandler(404)
def not_found_error(_):
    return render_template("404.html"), 404


@bp.app_errorhandler(418)
def teapot(_):
    return render_template("418.html"), 418


@bp.app_errorhandler(500)
def internal_error(_):
    return render_template("500.html"), 500
