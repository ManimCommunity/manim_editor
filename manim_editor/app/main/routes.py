from flask import render_template
from ...editor import get_scenes

from . import bp


@bp.route("/")
@bp.route("/index")
def index():
    scenes = get_scenes()
    return render_template("index.html", title="Index", scenes=scenes)


@bp.route("/test")
def test():
    return render_template("test.html", title="Test")
