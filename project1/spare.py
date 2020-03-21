from flask import *
from datetime import datetime
from marshmallow import Schema, fields, pprint
import os

from project1.db import get_db

bp = Blueprint("spare", __name__)


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


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/account')
def account():
    return render_template('signup.html')


@bp.route('/json/posts')
def jsonf():
    return jsonify(postResult)


@bp.route('/json/users')
def jsonUsers():
    return jsonify(userResult)


@bp.route('/votes/upvote', methods=['GET', 'POST', 'PUT'])
def incrementKarma():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        userExists = Users.query.filter_by(userName=_username).first()

        if userExists is not None:
            if userExists.userName == _username and userExists.password == _password:
                userExists.karma += 1
                db.session.commit()
                print("SUCCESS")
                print(userExists.karma)

                schema = UserSchema()
                result = schema.dump(Users.query.filter_by(
                    userName=_username).first())

                return Response(json.dumps(result),
                                status=201,
                                mimetype="application/json")
        else:
            print("USER doesnt exists")
            return Response('ERROR 404', status=404, mimetype="application/json")

    return render_template('incrementKarma.html')


@bp.route('/votes/downvote', methods=['GET', 'POST', 'PUT'])
def decrementKarma():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        userExists = Users.query.filter_by(userName=_username).first()

        if userExists is not None:
            if userExists.userName == _username and userExists.password == _password:
                userExists.karma -= 1
                db.session.commit()
                print("SUCCESS")
                print(userExists.karma)

                schema = UserSchema()
                result = schema.dump(Users.query.filter_by(
                    userName=_username).first())

                return Response(json.dumps(result),
                                status=201,
                                mimetype="application/json")
        else:
            print("USER doesnt exists")
            return Response('ERROR 404', status=404, mimetype="application/json")

    return render_template('decrementKarma.html')


@bp.route('/posts/create', methods=['GET', 'POST'])
def createPost():
    postform = Posts()
    if request.method == 'POST':
        _title = request.form['title']
        _community = request.form['community']
        _text = request.form['text']
        _username = request.form['username']
        _url = request.form['url']
        holder = datetime.now()
        timeCreated = datetime.strftime(
            holder, '%Y/%m/%d %H.%M%p')  # creates time as string

        new_post = Posts(title=_title, community=_community,
                         text=_text, Username=_username, url=_url, dt=timeCreated)
        Account = Users.query.filter_by(userName=_username).first()
        if Account is not None:
            db.session.add(new_post)
            db.session.commit()
            postResult = Postschema.dump(Posts.query.all())
            print("SUCCESS")

            # return jsonify(result), 201

            return Response(json.dumps(postResult),
                            status=201,
                            mimetype="application/json")

            # return Response(status=201, mimetype='application/json')

        else:
            return Response('ERROR 404', status=404, mimetype="application/json")

        return render_template('home.html')

    return render_template('createPost.html')


@bp.route('/posts/delete', methods=['GET', 'POST', 'DELETE'])
def deletePost():
    if request.method == 'POST':
        _title = request.form['title']  # title to be deleted
        _username = request.form['username']  # validate info
        _password = request.form['password']  # validate info

        # retrieves all posts relative to the user
        entry = Posts.query.filter_by(Username=_username, title=_title).first()

        userExists = Users.query.filter_by(userName=_username).first()

        if userExists is not None:  # checks if user exists helps redirect 404 error
            if userExists.userName == _username and userExists.password == _password:  # validate
                db.session.delete(entry)
                db.session.commit()
                print("POST HAS BEEN DELETED")
                postResult = Postschema.dump(
                    Posts.query.order_by(Posts.title).all())
                return Response(json.dumps(postResult),
                                status=201,
                                mimetype="application/json")
            else:
                return Response('ERROR 404', status=404, mimetype="application/json")

        else:
            print("User does not exist")
            return Response('ERROR 404', status=404, mimetype="application/json")
            return render_template('signup.html')

    return render_template('deletepost.html')


@bp.route('/posts/retrieve', methods=['GET', 'POST'])
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


@bp.route('/accounts/create', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        _username = request.form['username']
        _email = request.form['email']
        _password = request.form['password']

        try:
            # connects to sqlite.db file in current folder
            engine = create_engine('sqlite:///users.db', echo=True)
            db.metadata.create_all(bind=engine)  # creates the Users schema

            # creates a object to store info into the database
            Session = sessionmaker(bind=engine)
            session = Session()

            new_user = Users(userName=_username,
                             email=_email, password=_password, karma=0)

            session.add(new_user)
            session.commit()
            session.close()
            schema = UserSchema()
            result = schema.dump(Users.query.filter_by(
                userName=_username).first())
            return Response(json.dumps(result),
                            status=201,
                            mimetype="application/json")

        except:
            print("Error in creating your acount, please try again")
            return Response('ERROR 404', status=404, mimetype="application/json")

    return render_template('home.html')


@bp.route('/accounts/login', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']

        try:
            # retrieves row of info to look at
            userExists = Users.query.filter_by(userName=_username).first()

            if userExists.userName == _username and userExists.password == _password:
                print("Login validated")

                return Response('Login validated',
                                status=201,
                                mimetype="application/json")

            else:
                return Response('ERROR 404', status=404, mimetype="application/json")
                print("User not valid")

        except:
            return Response('ERROR 404', status=404, mimetype="application/json")
            print('ERROR ERRROR')

    return render_template('loginpage.html')


@bp.route('/accounts/updateEmail', methods=['GET', 'POST', 'PUT'])
def updateEmail():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        new_email = request.form['email']

        userExists = Users.query.filter_by(userName=_username).first()
        if userExists.userName == _username and userExists.password == _password:
            userExists.email = new_email
            db.session.commit()
            print('Email has been updated')
            schema = UserSchema()
            result = schema.dump(Users.query.filter_by(
                userName=_username).first())

            return Response(json.dumps(result),
                            status=201,
                            mimetype="application/json")

        else:
            print(
                "Username and password not found or do not match please check credentials")
            return Response('ERROR 404', status=404, mimetype="application/json")

    return render_template('updateEmail.html')


@bp.route('/accounts/delete', methods=['GET', 'POST', 'DELETE'])
def deleteAcc():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        try:
            userExists = Users.query.filter_by(userName=_username).first()
            if userExists.userName == _username and userExists.password == _password:
                db.session.delete(userExists)
                db.session.commit()
                print('Account has been deleted')
                schema = UserSchema()
                result = schema.dump(Users.query.filter_by(
                    userName=_username).first())
                return Response(json.dumps(result),
                                status=201,
                                mimetype="application/json")

        except:
            print(
                'Error in deleting your account please use a valid username and password')
            return Response('ERROR 404', status=404, mimetype="application/json")

    return render_template('deleteAcc.html')


if __name__ == "__main__":
    app.run(debug=True, port=2015)
