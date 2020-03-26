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

        validEmail = db.execute(
            'SELECT email FROM users WHERE email=?', (_email,)).fetchone()

        validUser = db.execute(
            'SELECT userName FROM users WHERE userName=?', (_username,)).fetchone()

        if _username == "" and _password == "" and _email == "":
            return Response(json.dumps({"message": "Error in creating your account"}), status=404, content_type="application/json")

        if _email == "":
            return Response(json.dumps({"message": "Not Proper email"}), status=404, content_type="application/json")

        if validEmail is not None:
            return Response(json.dumps({"message": "Email already in use"}), status=404, content_type="application/json")

        if validUser is not None:

            return Response(json.dumps({"message": "Username already in use"}), status=404, content_type="application/json")

        else:
            db.execute("INSERT INTO users(userName,email,password,karma) VALUES(?,?,?,?)",
                       (_username, _email, _password, _karma))
            db.commit()

            return Response(status=201)


@bp.route('/updateEmail', methods=['GET', 'POST', 'PUT'])
def updateEmail():
    db = get_db()

    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        new_email = request.form['email']

        validEmail = db.execute(
            'SELECT email FROM users WHERE email=?', (new_email,)).fetchone()

        validUser = db.execute(
            'SELECT userName FROM users WHERE userName=? AND password=?', (_username, _password,)).fetchone()

        if _username == "" and _password == "" and new_email == "":

            return Response(json.dumps({"message": "Provided information"}), status=404, content_type="application/json")

        if new_email == "":

            return Response(json.dumps({"message": "Enter a new email for account"}), status=404, content_type="application/json")

        if validUser is None:

            return Response(json.dumps({"message": "No account to update email"}), status=404, content_type="application/json")

        if validUser is not None and validEmail is not None:

            return Response(json.dumps({"message": "Please provide a unique email"}), status=404, content_type="application/json")

        if validEmail is not None:

            return Response(json.dumps({"message": "Enter a new email for account"}), status=404, content_type="application/json")

        else:
            db.execute("UPDATE users SET email=? WHERE userName =? OR password=?",
                       (new_email, _username, _password))
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