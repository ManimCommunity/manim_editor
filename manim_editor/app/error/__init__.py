from flask import Blueprint

bp = Blueprint("error", __name__, template_folder="templates")

from . import handlers  # nopep8
