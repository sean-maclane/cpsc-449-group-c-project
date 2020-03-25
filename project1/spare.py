from flask import *
from datetime import datetime
from marshmallow import Schema, fields, pprint
import sqlite3
import os

from project1.db import get_db

appmain_blueprint = Blueprint("app_main", __name__)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    userName = fields.Str()
    email = fields.Str()
    karma = fields.Int()
    # formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, Users):
        return "{},{},{}".format(Users.userName, Users.email, Users.karma)


# These lines need to move inside the functions that call them
# This way they can be portable in the instances
#schema = UserSchema(many=True)
#userResult = schema.dump(Users.query.all())

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    community = fields.Str()
    Username = fields.Str()

    def format_name(self, Posts):
        return "{},{},{}".format(Posts.title, Posts.community, Posts.Username)

# These lines need to move inside the functions that call them
# This way they can be portable in the instances
#Postschema = PostSchema(many=True)
#postResult = Postschema.dump(Posts.query.all())


@appmain_blueprint.route('/')
def home():
    return render_template('home.html')


@appmain_blueprint.route('/account')
def account():
    return render_template('signup.html')


@appmain_blueprint.route('/json/posts')
def jsonf():
    return jsonify(postResult)


@appmain_blueprint.route('/json/users')
def jsonUsers():
    return jsonify(userResult)


@appmain_blueprint.route('/votes/upvote', methods=['POST'])
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


@appmain_blueprint.route('/votes/downvote', methods=['POST'])
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


@appmain_blueprint.route('/posts/create', methods=['GET', 'POST'])
def create_post():
    db = get_db()

    _username = request.form['username']
    _password = request.form['password']
    _post_title = request.form['Post Title']
    _post_community = request.form['Post Community']
    _post_body = request.form['Post Body']

    if(_username == "" and _password == ""):
        # error case 1
        return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

    login_id = db.execute('SELECT id FROM user WHERE username = ? and password = ?', (_username)
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

    if _post_title is not None and _post_community is not None and if _post_body is not None:
        db.execute('INSERT INTO post (community_id, author_id, title, body)
                    VALUES (
                        (SELECT id FROM community WHERE community_name = ?, (_post_community)),
                        login_id,
                        ?, (_post_title),
                        ?, (_post_body)
                    )
                ')
        db.commit()
        return Response(json.dumps({"message": "Post created successfully"}), status=201, content_type="application/json")


@appmain_blueprint.route('/posts/delete', methods=['GET', 'POST', 'DELETE'])
def delete_post():
    """
    User has to be logged in to delete one of his/her posts
    Get the title of the post, retrieve the ID from post title and then delete
    """
    db = get_db()

    _username = request.form['username']
    _post_title = request.form['Post Title']
    _post_community = request.form['Post Community']

    login_id = db.execute('SELECT id FROM users WHERE username = ? and password = ?', (_username))
    if login_id is None:
        # error case 2
        return Response(json.dumps({"message": "User account not found"}), status=404, content_type="application/json")

    if _post_title is None:
        # error case 3
        return Response(json.dumps({"message": "Post title not found"}), status=404, content_type="application/json")

    if _post_community is None:
        # error case 4
        return Response(json.dumps({"message": "Post community not found"}), status=404, content_type="application/json")

    if login_id is not None and _post_title is not None and if _post_community is not None:
        db.execute('DELETE FROM post where title = ?', (_post_title))
        db.commit()
        return Response(json.dumps({"message": "Post deleted successfully"}), status=201, content_type="application/json")


@appmain_blueprint.route('/posts/retrieve', methods=['GET', 'POST'])
def retrieve_existing_post():
    """

    """
    db = get_db()

    _post_title = request.form['Post Title']

    if _post_title is None:
        return Response(json.dumps({"message": "Please enter post title in search"}), status=404, content_type="application/json")

    if _post_title is not None:
        db.execute('SELECT title, body, author_id, community_id, created FROM post WHERE title like '%?%', (_post_title)')
        return Response(json.dumps({"message": "Post retrieved successfully"}), status=201, content_type="application/json")


@appmain_blueprint.route('/posts/retrieve', methods=['GET', 'POST'])
def retrievePost():
    if request.method == 'POST':
        _title = request.form['title']
        _community = request.form['community']

        entry = Posts.query.filter_by(title=_title).all()
        entryCommunity = Posts.query.filter_by(community=_community).all()

        yes = Posts.query.filter(Posts.title)

        sortedCategory = Posts.query.filter(
            and_(Posts.title == _title, Posts.community == _community)).all()

        fields = ['title', 'community', 'Username']
        yes = Posts.query.options(load_only(*fields)).all()

        if _title == "" and _community == "":  # retrieve all posts
            print(yes)
            postResult = Postschema.dump(yes)
            return Response(json.dumps(postResult),
                            status=201,
                            mimetype="application/json")

        if _title == "":  # if title entry is blank look at community and output those
            print(entryCommunity)
            postResult = Postschema.dump(entryCommunity)
            return Response(json.dumps(postResult),
                            status=201,
                            mimetype="application/json")

        if _community == "":  # if community is blank output title entries
            print(entry)
            postResult = Postschema.dump(entry)
            return Response(json.dumps(postResult),
                            status=201,
                            mimetype="application/json")

        else:
            print(sortedCategory)  # else both fields are filled in
            postResult = Postschema.dump(sortedCategory)
            return Response(json.dumps(postResult),
                            status=201,
                            mimetype="application/json")

    return render_template('retrievePost.html')


@appmain_blueprint.route('/accounts/create', methods=['GET', 'POST'])
def signup():
    db = get_db()

    if request.method == 'POST':
        _username = request.form['username']
        _email = request.form['email']
        _password = request.form['password']
        _karma = 0

        if not _username:

            return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

        if not _email:

            return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

        if not _password:

            return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

        else:
            db.execute("INSERT INTO users(userName,email,password,karma) VALUES(?,?,?,?)",
                       (_username, _email, _password, _karma))
            db.commit()

            return Response(json.dumps({"message": "Success"}), status=201, content_type="application/json")


@appmain_blueprint.route('/accounts/updateEmail', methods=['GET', 'POST', 'PUT'])
def updateEmail():
    db = get_db()

    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        new_email = request.form['email']

        if not _username:

            return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

        if not _password:

            return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

        if not new_email:

            return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

        else:
            db.execute("UPDATE users SET email=? WHERE userName =? OR password=?",
                       (new_email, _username, _password))
            db.commit()

            return Response(json.dumps({"message": "Succes"}), status=201, content_type="application/json")


@appmain_blueprint.route('/accounts/delete', methods=['GET', 'POST'])
def deleteAcc():
    db = get_db()

    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']

        if not _username:
            return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

        if not _password:

            return Response(json.dumps({"message": "Provide information"}), status=404, content_type="application/json")

        else:
            db.execute("DELETE from users WHERE username=? AND password=?",
                       (_username, _password))
            db.commit()

            return Response(json.dumps({"message": "Success"}), status=201, content_type="application/json")


if __name__ == "__main__":
    app.run(debug=True, port=2015)
