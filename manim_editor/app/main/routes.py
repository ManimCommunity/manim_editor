import os
from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from ...editor import get_scenes, create_project_dir, SectionId, populate_project, get_projects

from . import bp


@bp.route("/")
@bp.route("/index")
def index():
    return redirect(url_for("main.project_selection"))


@bp.route("/project_selection")
def project_selection():
    for project in get_projects():
        print(project.name)
        for section in project.sections:
            print(section.in_project_video)
    return render_template("project_selection.html", title="Project Selection", cwd=os.getcwd())


@bp.route("/create_project")
def create_project():
    return redirect(url_for("main.set_project_name"))


@bp.route("/create_project1")
def set_project_name():
    return render_template("set_project_name.html", title="Create New Project")


@bp.route("/create_project2", methods=["POST"])
def section_selection():
    project_name = request.form["project_name"].strip()
    success, message = create_project_dir(project_name)
    if not success:
        flash(message, "danger")
        return redirect(url_for("main.set_project_name"))

    flash(message, "success")
    scenes = get_scenes()
    if len(scenes) == 0:
        flash("No sections were found. You must render you scene with the '--save_sections' flag. Refer to the documentation for more information.", "danger")
    return render_template("section_selection.html", title="Create New Project", scenes=scenes, project_name=project_name)


# ajax
@bp.route("/create_project3", methods=["POST"])
def confirm_section_selection():
    project = request.json
    if project is None:
        abort(400)
    project_name = project["name"]
    sections = [SectionId(section["scene_id"], section["section_id"]) for section in project["sections"]]
    success = populate_project(project_name, sections)
    if success:
        flash(f"The project '{project_name}' has successfully been populated.", "success")
        return jsonify(success=True)
    else:
        # the flash will be taken care of by the client
        return jsonify(success=False)
