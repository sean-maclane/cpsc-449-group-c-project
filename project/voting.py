from flask import *
from datetime import datetime
import sqlite3
import os

from project.db import get_db

bp = Blueprint("voting", __name__, url_prefix='/voting')


@bp.route('/upvote', methods=['GET', 'POST'])
def upvote():
    db = get_db()

    _username = request.form['username']
    _password = request.form['password']
    _post_title = request.form['title']

    if(_username == "" and _password == ""):
        return Response(json.dumps({"message": "Provide login information"}), status=404, content_type="application/json")

    login_id = db.execute(
        'SELECT id FROM users WHERE username = ? and password = ?', (_username, _password,)).fetchone()
    if login_id is None:
        return Response(json.dumps({"message": "Create an account to upvote and downvote"}), status=404, content_type="application/json")

    post_id = db.execute(
        'SELECT id FROM posts WHERE title = ?',  (_post_title,)).fetchone()
    if post_id is None:
        return Response(json.dumps({"message": "Post not fund"}), status=404, content_type="application/json")


    db.execute('UPDATE posts SET upvotes=upvotes+1 WHERE id = ?', (post_id))
    db.commit()
    return Response(status=201)


@bp.route('/downvote', methods=['GET', 'POST'])
def downvote():
    db = get_db()

    _username = request.form['username']
    _password = request.form['password']
    _post_title = request.form['title']

    if(_username == "" and _password == ""):
        return Response(json.dumps({"message": "Provide login information"}), status=404, content_type="application/json")

    login_id = db.execute(
        'SELECT id FROM users WHERE username = ? and password = ?', (_username, _password)).fetchone()
    if login_id is None:
        return Response(json.dumps({"message": "Create an account to upvote and downvote"}), status=404, content_type="application/json")

    post_id = db.execute(
        'SELECT id FROM posts WHERE title = ?',  (_post_title,)).fetchone()
    if post_id is None:
        return Response(json.dumps({"message": "Post not fund"}), status=404, content_type="application/json")

    db.execute('UPDATE posts SET downvotes=downvotes+1 WHERE id = ?', (post_id))
    db.commit()
    return Response(status=201)


@bp.route('/voteSegregation', methods=['GET', 'POST'])
def voteSegregation():
    db = get_db()

    _post_title = request.form['title']
    _post_community = request.form['community']

    if _post_title == "" and _post_community == "":
        return Response(json.dumps({"message": "Provide a title and community"}), status=404, content_type="application/json")

    if _post_title == "":
        return Response(json.dumps({"message": "Provide a title"}), status=404, content_type="application/json")

    if _post_community == "":
        return Response(json.dumps({"message": "Provide a community"}), status=404, content_type="application/json")
    
    db.execute("SELECT upvotes, downvotes FROM posts WHERE title = ? AND community = ?", (_post_title, _post_community))
    #db.execute("SELECT upvotes, downvotes FROM posts WHERE title = ?", (_post_title), "AND community = ?", (_post_community))
    return Response(json.dumps({"message": "Upvotes and downvotes of the post retrieved successfully"}), status=201, content_type="application/json")


@bp.route('/topScoring', methods=['GET'])
def topScoring():
    db = get_db()

    _post_community = request.form['community']

    if _post_community == "":
        return Response(json.dumps({"message": "Provide a community"}), status=404, content_type="application/json")    

    db.execute('SELECT TOP 10 title FROM posts WHERE community = ? ORDER BY upvotes DESC', (_post_community,))
    return Response(status=201)


# WSGI entrypoint for VOTING
from project import create_app
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2015)
