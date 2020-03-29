from flask import *
from datetime import datetime
import sqlite3
import os

from project1.db import get_db

bp = Blueprint("posts", __name__, url_prefix='/posts')


@bp.route('/create', methods=['GET', 'POST'])
def create_post():
    db = get_db()

    _username = request.form['username']
    _post_title = request.form['title']
    _post_community = request.form['community']
    _post_body = request.form['text']

    if (_username == "" and _post_title == "" and _post_community == "" and _post_body == ""):
        # error case 1
        return Response(json.dumps({"message": "Please fill out information"}), status=404, content_type="application/json")

    login_id = db.execute('SELECT id FROM users WHERE username = ?', (_username,))
    if login_id is None:
        # error case 2
        return Response(json.dumps({"message": "Create an account"}), status=404, content_type="application/json")

    if _post_title is None:
        # error case 3
        return Response(json.dumps({"message": "Enter post title"}), status=404, content_type="application/json")

    if _post_community is None:
        # error case 4
        return Response(json.dumps({"message": "Enter post community"}), status=404, content_type="application/json")

    if _post_body is None:
        # error case 5
        return Response(json.dumps({"message": "Please input some text body for the post"}), status=404, content_type="application/json")

    if _post_title is not None and _post_community is not None and _post_body is not None:
        db.execute("INSERT INTO posts (community, title, text, Username, dt) VALUES (?, ?, ?, ?, ?)", (_post_community, _post_title, _post_body, _username, datetime.now()))
        db.commit()
        return Response(json.dumps({"message": "Post created successfully"}), status=201, content_type="application/json")


@bp.route('/delete', methods=['GET', 'POST', 'DELETE'])
def delete_post():
    db = get_db()

    _post_title = request.form['title']

    if _post_title is None:
        return Response(json.dumps({"message": "Post title not found"}), status=404, content_type="application/json")

    if _post_title is not None:
        db.execute('DELETE FROM posts where title = ?', (_post_title,))
        db.commit()
        return Response(json.dumps({"message": "Post deleted successfully"}), status=201, content_type="application/json")


@bp.route('/retrieve', methods=['GET', 'POST'])
def retrieve_existing_post():
    """
    Posts can be retrieved by anyone accessing the site; login not required.
    Post title will be search for and values will be retrieved based on the ID
    of the search field
    """
    db = get_db()

    _post_title = request.form['title']
    _post_community = request.form['community']

    if _post_title == "" and _post_community == "":
        return Response(json.dumps({"message": "Provide a title and community"}), status=404, content_type="application/json")

    if _post_title == "":
        return Response(json.dumps({"message": "Provide a title"}), status=404, content_type="application/json")

    if _post_community == "":
        return Response(json.dumps({"message": "Provide a community"}), status=404, content_type="application/json")
    
    db.execute("SELECT community, title, text, dt FROM posts WHERE title = ?", (_post_title,))
    return Response(json.dumps({"message": "Post retrieved successfully"}), status=201, content_type="application/json")
        

# WSGI entrypoint for POSTS
from project1 import create_app
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2015)
