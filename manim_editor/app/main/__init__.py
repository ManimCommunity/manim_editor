from flask import Blueprint

bp = Blueprint("main", __name__, template_folder="templates")

from . import routes  # nopep8
