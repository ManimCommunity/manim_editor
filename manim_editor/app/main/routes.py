from flask import render_template, flash
from ...editor import get_scenes

from . import bp


@bp.route("/")
@bp.route("/index")
def index():
    flash("test", "info")
    return render_template("index.html", title="Index")


@bp.route("/create_project")
@bp.route("/create_project1")
def set_project_name():
    return render_template("set_project_name.html", title="Create New Project")


@bp.route("/create_project2")
def section_selection():
    scenes = get_scenes()
    return render_template("section_selection.html", title="Create New Project", scenes=scenes)
