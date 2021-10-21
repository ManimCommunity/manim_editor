from flask import render_template
from ...editor import get_indices

from . import bp


@bp.route("/")
@bp.route("/index")
def index():
    indices = get_indices()
    return render_template("index.html", title="Index", indices=indices)


@bp.route("/test")
def test():
    return render_template("test.html", title="Test")
