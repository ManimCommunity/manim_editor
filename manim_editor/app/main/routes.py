"""Main backend file."""
import os
from pathlib import Path

from flask import (
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from ...editor import (
    create_project_dir,
    export_presentation,
    get_project,
    get_projects,
    get_scenes,
    populate_project,
)
from . import bp


@bp.route("/")
@bp.route("/index")
def index():
    return redirect(url_for("main.project_selection"))


@bp.route("/project_selection")
def project_selection():
    projects = get_projects()
    return render_template(
        "project_selection.html",
        version=current_app.config["VERSION"],
        title="Project Selection",
        cwd=os.getcwd(),
        projects=projects,
    )


@bp.route("/edit_project/<name>")
def edit_project(name: str):
    project_name, slides = get_project(name)
    if project_name is None:
        abort(404)
    return render_template(
        "edit_project.html",
        version=current_app.config["VERSION"],
        title="Edit Project",
        name=name,
        slides=slides,
        present_export=False,
    )


# ajax
@bp.route("/export_presentation", methods=["POST"])
def export_presenter():
    project = request.json
    if project is None:
        abort(400)
    project_name, slides = get_project(project["name"])
    if project_name is None:
        print(f"Project '{project['name']}' couldn't be found.")
        return jsonify(success=False)
    export_presentation(project_name, slides)
    return jsonify(success=True)


@bp.route("/serve_project_static/<name>/<path>")
def serve_project_static(name: str, path: str):
    """Since the projects are not in the Flask static folder, this function serves the videos and thumbnails instead."""
    abspath = (Path(name) / path).absolute()
    # NOTE: this should never be used in an online environment, for a local one it's fine
    return send_file(abspath)


@bp.route("/create_project")
def create_project():
    return redirect(url_for("main.set_project_name"))


@bp.route("/create_project1")
def set_project_name():
    return render_template("set_project_name.html", version=current_app.config["VERSION"], title="Create New Project")


@bp.route("/create_project2", methods=["GET", "POST"])
def scene_selection():
    # when users play around with the address bar
    if request.method == "GET":
        return redirect(url_for("main.set_project_name"))
    project_name = request.form["project_name"].strip()
    success, message = create_project_dir(project_name)
    if not success:
        flash(message, "danger")
        return redirect(url_for("main.set_project_name"))

    flash(message, "success")
    scenes = get_scenes()
    if len(scenes) == 0:
        flash(
            "No sections were found. You must render you scene with the '--save_sections' flag. Refer to the documentation for more information.",
            "danger",
        )
    return render_template(
        "scene_selection.html",
        version=current_app.config["VERSION"],
        title="Create New Project",
        scenes=scenes,
        project_name=project_name,
    )


# ajax
@bp.route("/create_project3", methods=["POST"])
def confirm_scene_selection():
    project = request.json
    if project is None:
        abort(400)
    project_name: str = project["name"]
    scene_ids = project["scene_ids"]
    success = populate_project(project_name, scene_ids)
    if success:
        flash(f"The project '{project_name}' has successfully been populated.", "success")
        return jsonify(success=True)
    else:
        # the flash will be taken care of by the client
        abort(500)
