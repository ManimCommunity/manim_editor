import os
from flask import render_template, flash, redirect, url_for, request
from ...editor import get_scenes, validate_project_name

from . import bp


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html", title="Index", cwd=os.getcwd())


@bp.route("/create_project")
def create_project():
    return redirect(url_for("main.set_project_name"))


@bp.route("/create_project1")
def set_project_name():
    return render_template("set_project_name.html", title="Create New Project")


@bp.route("/create_project2", methods=["POST"])
def section_selection():
    project_name = request.form["project_name"].strip()
    if not validate_project_name(project_name):
        flash(f"'{project_name}' is not a valid project name. Make sure that a folder with that name can be created in the CWD.", "danger")
        return redirect(url_for("main.set_project_name"))

    flash(f"Successfully created '{project_name}' directory in CWD. Everything the Manim Editor will create ends up in this directory.", "success")
    scenes = get_scenes()
    return render_template("section_selection.html", title="Create New Project", scenes=scenes, project_name=project_name)
