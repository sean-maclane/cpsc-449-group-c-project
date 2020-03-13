from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, exists, and_
from sqlalchemy.orm import sessionmaker, relationship, load_only
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import inspect
from marshmallow import Schema, fields, pprint
import os


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {'posts': 'sqlite:///posts.db'}
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"

    id = Column('id', db.Integer, primary_key=True)
    userName = Column('username', db.String(100), unique=True)
    email = Column('email', db.String(100), unique=True)
    password = Column('password', db.String(100), unique=True)
    karma = Column('Karma', db.Integer)

    def __init__(self, userName, email, password, karma):
        self.userName = userName
        self.email = email
        self.password = password
        self.karma = karma


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    userName = fields.Str()
    email = fields.Str()
    karma = fields.Int()
    # formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, Users):
        return "{},{},{}".format(Users.userName, Users.email, Users.karma)


schema = UserSchema(many=True)
userResult = schema.dump(Users.query.all())


class Posts(db.Model):
    __bind_key__ = 'posts'
    __tablename__ = 'posts'

    id = Column('id', db.Integer, primary_key=True)
    title = Column('title', db.String(100))
    community = Column('community', db.String(100))
    text = Column('text', db.String(100))
    Username = Column('Username', db.String(100))
    url = Column('url', db.String(100),  nullable=True)
    dt = Column('dateTime', db.String(100))


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    community = fields.Str()
    Username = fields.Str()

    def format_name(self, Posts):
        return "{},{},{}".format(Posts.title, Posts.community, Posts.Username)


Postschema = PostSchema(many=True)
postResult = Postschema.dump(Posts.query.all())

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/account')
def account():
    return render_template('signup.html')


@app.route('/json/posts')
def jsonPosts():
    return jsonify(postResult)


@app.route('/json/users')
def jsonUsers():
    return jsonify(userResult)


@app.route('/createPost', methods=['GET', 'POST'])
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
            return jsonify(postResult)

        else:
            print("ERROR")
            return render_template('signup.html')

        return render_template('home.html')

    return render_template('createPost.html')


@app.route('/deletePost', methods=['GET', 'POST', 'DELETE'])
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
                return jsonify(postResult)
            else:
                print("NO SUCCESFUL DELETE CHECK FIELDS")
                return render_template('deletepost.html')
        else:
            print("User does not exist")
            return render_template('signup.html')

    return render_template('deletepost.html')


@app.route('/retrievePost', methods=['GET', 'POST'])
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
            return jsonify(postResult)

        if _title == "":  # if title entry is blank look at community and output those
            print(entryCommunity)
            postResult = Postschema.dump(entryCommunity)
            return jsonify(postResult)

        if _community == "":  # if community is blank output title entries
            print(entry)
            postResult = Postschema.dump(entry)
            return jsonify(postResult)

        else:
            print(sortedCategory)  # else both fields are filled in
            postResult = Postschema.dump(sortedCategory)
            return jsonify(postResult)

    return render_template('retrievePost.html')


@app.route('/signup', methods=['GET', 'POST'])
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
            return jsonify(result)

        except:
            print("Error in creating your acount, please try again")
            return render_template('signup.html')

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']

        try:
            # retrieves row of info to look at
            userExists = Users.query.filter_by(userName=_username).first()

            if userExists.userName == _username and userExists.password == _password:
                print("Login validated")

                return render_template('home.html')

            else:
                print("User not valid")

        except:
            print('ERROR ERRROR')

    return render_template('loginpage.html')


@app.route('/updateEmail', methods=['GET', 'POST'])
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
            return jsonify(result)

        else:
            print(
                "Username and password not found or do not match please check credentials")
    return render_template('updateEmail.html')


@app.route('/deleteAccount', methods=['GET', 'POST', 'DELETE'])
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
                return jsonify(result)

        except:
            print(
                'Error in deleting your account please use a valid username and password')

    return render_template('deleteAcc.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
