from project1 import create_app
from flask import *
from datetime import datetime
import sqlite3
import os

from project1.db import get_db

bp = Blueprint("message", __name__, url_prefix='/message')


@bp.route('/send', methods=['GET,POST'])
def sendMessage():
    db = get_db()

    _id = request.form['id']
    _userfrom = request.form['userfrom']
    _userto = request.form['userto']
    _ts = request.form['ts']
    _message = request.form['messagecontent']
    _flag = request.form['flag']

    valid_userfrom = db.execute(
        'SELECT userName FROM users WHERE username = ? ', (_userfrom)).fetchone()
    valid_userto = db.execute(
        'SELECT userName FROM users WHERE username = ?', (_userto)).fetchone()
    valid_message = db.execute(
        'SELECT messagecontent FROM users WHERE messagecontent = ?', (_message)).fetchone()

    if valid_userfrom is None:
        # error case 1, no user in database to send messages to
        return Response(json.dumps({"message": "users don't exist"}), status=404, content_type="application/json")

    if valid_userfrom is not None and valid_userto is None:
        # error case 2
        return Response(json.dumps({"message": "receiver account doesn't exist"}), status=404, content_type="application/json")

    if valid_userfrom is None and valid_userto is not None:
        return Response(json.dumps({"message": "sending account doesn't exist"}), status=404, content_type="application/json")

    if valid_message is None:
        return Response(json.dumps({"message": "provide a message"}), status=404, content_type="application/json")

    else:
        db.execute(
            'INSERT INTO messages (userfrom,userto,ts,messagecontent,flag) VALUES (?,?,?,?,?)', (_userfrom, _userto, _ts, _message, _flag))
        db.commit()
    return Response(status=201)


@bp.route('/delete', methods=['GET,POST,DELETE'])
def deleteMessage():
    db = get_db()

    _userfrom = request.form['userfrom']
    _message = request.form['messagecontent']

    if _userfrom is None:
        # error case 1
        return Response(json.dumps({"message": "user doesn't exist"}), status=404, content_type="application/json")

    if _message is None:
        # error case 2
        return Response(json.dumps({"message": "message doesn't exist"}), status=404, content_type="application/json")

    if _message == "":
        return Response(json.dumps({"message": "no message provided"}), status=404, content_type="application/json")
    else:
        return Response(status=201)


@bp.route('/favorite', methods['GET'])
def favoriteMessage():

    _message = request.form['messagecontent']
    _flag = request.form['flag']

    if _message is None:
        return Response(json.dumps({"message": "message can't be found"}), status=404, content_type="application/json")

    return Response(status=201)


# WSGI entrypoint for VOTES
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2015)
