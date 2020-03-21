from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from project1.db import get_db

bp = Blueprint("posts", __name__, url_prefix="/posts")


