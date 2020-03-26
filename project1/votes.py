from flask import *
from datetime import datetime
import sqlite3
import os

from project1.db import get_db

bp = Blueprint("votes", __name__, url_prefix='/votes')


@bp.route('/upvote', methods=['POST'])
def incrementKarma():
    db = get_db()

    _username = request.form['username']
    _password = request.form['password']

    if(_username == "" and _password == ""):
        # error case 1
        return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

    login_id = db.execute(
        'SELECT id FROM users WHERE username = ? and password = ?', (_username, _password)).fetchone()
    if login_id is None:
        # error case 2
        return Response(json.dumps({"message": "Create an account"}), status=404, content_type="application/json")

    db.execute('UPDATE users SET karma=karma+1 WHERE id = ?', (login_id))
    db.commit()
    return Response(status=201)


@bp.route('/downvote', methods=['POST'])
def decrementKarma():
    db = get_db()

    _username = request.form['username']
    _password = request.form['password']

    if(_username == "" and _password == ""):
        # error case 1
        return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

    login_id = db.execute(
        'SELECT id FROM users WHERE username = ? and password = ?', (_username, _password)).fetchone()
    if login_id is None:
        # error case 2
        return Response(json.dumps({"message": "Create an account"}), status=404, content_type="application/json")

    db.execute('UPDATE users SET karma=karma-1 WHERE id = ?', (login_id))
    db.commit()
    return Response(status=201)