from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os


Base = declarative_base()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db' #if added breaks program users arent registered
app.config['SQLALCHEMY_BINDS'] = {'posts': 'sqlite:///posts.db'}
db = SQLAlchemy(app)

db.create_all('__all__')

# current issues, can only make one post per account


class Users(db.Model):
    __tablename__ = "users"

    id = Column('id', db.Integer, primary_key=True)
    userName = Column('username', db.String(100), unique=True)
    email = Column('email', db.String(100), unique=True)
    password = Column('password', db.String(100), unique=True)
    karma = Column('Karma', db.Integer)


class Posts(db.Model):
    __bind_key__ = 'posts'
    __tablename__ = 'posts'

    id = Column('id', db.Integer, primary_key=True)
    title = Column('title', db.String(100), unique=True)
    community = Column('community', db.String(100), unique=True)
    text = Column('text', db.String(100))
    username = Column('username', db.String(100), unique=True)
    url = Column('url', db.String(100),  nullable=True)

    # date = Column(datetime.time()(timezone=True), default=func.now())
    # time_created = Column(datetime(timezone=True), server_default=func.now())


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/account')
def account():
    return render_template('signup.html')


@app.route('/createPost', methods=['GET', 'POST'])
def createPost():
    if request.method == 'POST':
        _title = request.form['title']
        _community = request.form['community']
        _text = request.form['text']
        _username = request.form['username']
        _url = request.form['url']

        validUser = Users.query.filter_by(userName=_username).first()
        if validUser.userName == _username:
            #postEngine = create_engine('sqlite:///posts.db', echo=True)

            new_post = Posts(title=_title, community=_community,
                             text=_text, username=_username, url=_url)

            db.session.add(new_post)
            db.session.commit()
            db.session.close()
            print("SUCCESSSSS")
            return render_template('home.html')
        else:
            print("User does not exist please make an account")
            return render_template(url_for('createPost'))

    return render_template('createPost.html')


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

        except:
            print("Error in creating your acount, please try again")
            return redirect(url_for('signup'))

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

        try:
            userExists = Users.query.filter_by(userName=_username).first()
            if userExists.userName == _username and userExists.password == _password:
                userExists.email = new_email
                db.session.commit()
                print('Email has been updated')
                return render_template('home.html')

        except:
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
                return render_template('home.html')

        except:
            print(
                'Error in deleting your account please use a valid username and password')

    return render_template('deleteAcc.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
