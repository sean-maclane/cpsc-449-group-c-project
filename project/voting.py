from flask import *
from datetime import datetime
import sqlite3
import os

from project.db import get_db

bp = Blueprint("voting", __name__, url_prefix='/voting')

     
# WSGI entrypoint for VOTING
from project import create_app
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2015)
