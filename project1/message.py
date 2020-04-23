from project1 import create_app
from flask import *
from datetime import datetime
import sqlite3
import os

from project1.db import get_db

bp = Blueprint("message", __name__, url_prefix='/message')


@bp.route('/send', methods=['POST'])
def sendMessage():
    db = get_db()

    _id = request.form['']
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


@bp.route('/delete', methods=['GET,POST'])
def deleteMessage():
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


@bp.route('/favorite', methods['GET'])
def favoriteMessage():
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


# WSGI entrypoint for VOTES
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2015)
