from flask import *
from datetime import datetime
import sqlite3
import os

from project1.db import get_db

bp = Blueprint("accounts", __name__, url_prefix='/accounts')


@bp.route('/create', methods=['GET', 'POST'])
def signup():
    db = get_db()

    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        _email = request.form['email']

        _karma = 0

        if _username == "" and _password == "" and _email == "":
            return Response(json.dumps({"message": "Error in creating your account"}), status=404, content_type="application/json")

        if '@' not in _email:
            return Response(json.dumps({"message": "Not proper Email"}), status=404, content_type="application/json")
            
        else:
            db.execute("INSERT INTO users(userName,email,password,karma) VALUES(?,?,?,?)",
                       (_username, _email, _password, _karma))
            db.commit()

            return Response(status=201)


@bp.route('/updateEmail', methods=['GET', 'POST', 'PUT'])
def updateEmail():
    db = get_db()

    _username = request.form['username']
    _password = request.form['password']
    _new_email = request.form['email']

    if(_username == "" and _password == ""):
        # error case 1
        return Response(json.dumps({"message": "Provided information"}), status=404, content_type="application/json")
    
    if(_new_email == ""):
        # error case 1
        return Response(json.dumps({"message": "Enter a new email for account"}), status=404, content_type="application/json")

    login_id = db.execute(
        'SELECT id FROM users WHERE username = ? and password = ?', (_username, _password)).fetchone()
    if login_id is None:
        # error case 2
        return Response(json.dumps({"message": "No account to update email"}), status=404, content_type="application/json")

    db.execute('UPDATE users SET email = ? WHERE id = ?', (_new_email, login_id))
    db.commit()
    return Response(status=201)


@bp.route('/delete', methods=['GET', 'POST'])
def deleteAcc():
    db = get_db()

    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']

        validUser = db.execute(
            'SELECT userName FROM users WHERE userName=? AND password=?', (_username, _password,)).fetchone()

        if _username == "" and _password == "":
            return Response(json.dumps({"message": "Provide Information"}), status=404, content_type="application/json")

        if validUser is None:
            return Response(json.dumps({"message": "No account to delete"}), status=404, content_type="application/json")

        else:
            db.execute("DELETE from users WHERE username=? AND password=?",
                       (_username, _password))
            db.commit()

            return Response(status=201)
            
            
# WSGI entrypoint for ACCOUNTS
from project1 import create_app
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2015)
