from flask import *
from datetime import datetime
import sqlite3
import os

from project.db import get_db

bp = Blueprint("message", __name__, url_prefix='/message')


@bp.route('/send', methods=['GET', 'POST'])
def sendMessage():
    db = get_db()

    _userfrom = request.form['userfrom']
    _userto = request.form['userto']
    _message = request.form['messagecontent']
    _flag = request.form['flag']

    if _userfrom == "":

        return Response(json.dumps({"message": "No user from"}), status=404, content_type="application/json")

    if _userto == "":

        return Response(json.dumps({"message": "No user to"}), status=404, content_type="application/json")

    if _message == "":
        return Response(json.dumps({"message": "No message"}), status=404, content_type="application/json")

    else:
        db.execute(
            'INSERT INTO messages (userfrom,userto,messagecontent,flag) VALUES (?,?,?,?)', (_userfrom, _userto, _message, _flag))
        db.commit()
    return Response(status=201)


@bp.route('/delete', methods=['GET', 'POST', 'DELETE'])
def deleteMessage():
    db = get_db()

    _userfrom = request.form['userfrom']
    _message = request.form['messagecontent']

    if _userfrom == "":
        # error case 1
        return Response(json.dumps({"message": "user doesn't exist"}), status=404, content_type="application/json")

    if _message == "":
        return Response(json.dumps({"message": "no message provided"}), status=404, content_type="application/json")
    else:
        db.execute("DELETE from messages WHERE userfrom=? AND messagecontent=?",
                   (_userfrom, _message))
        db.commit()
        return Response(status=201)


@bp.route('/flag', methods=['GET', 'POST'])
def favoriteMessage():

    _message = request.form['messagecontent']
    _flag = request.form['flag']

    if _message == "":
        return Response(json.dumps({"message": "message can't be found"}), status=404, content_type="application/json")
    if _flag == 0:
        return Response(json.dumps({"message": "message isn't flagged"}), status=404, content_type="application/json")
    else:
        return Response(status=201)


# WSGI entrypoint for MESSAGE
from project import create_app
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2015)
