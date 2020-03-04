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

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"

    id = Column('id', db.Integer, primary_key=True)
    userName = Column('username', db.String(100), unique=True)
    email = Column('email', db.String(100), unique=True)
    password = Column('password', db.String(100), unique=True)
    karma = Column('Karma', db.Integer)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/account')
def account():

    return render_template('signup.html')


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
            engine = create_engine('sqlite:///users.db', echo=True)
            Base.metadata.create_all(bind=engine)  # creates the table

            # creates a object to store info into the database
            Session = sessionmaker(bind=engine)
            s = Session()

            exists = db.session.Users.query.get(_username)
            usethis = Session.query(Users).get(_username)

            test = db.session.query(Users.query.filter(
                Users.userName == _username).exists()).scalar()

            yes = db.session.query(Users).filter(
                Users.c.userName == _username).first()

            compareThis = Users.query.filter_by(_username).first()

            flash("please check login")

            """ query = s.query(Users).filter(
                Users.userName == _username, Users.password == _password) """

        except:
            print('ERROR ERRROR')
            return(500)

    return render_template('loginpage.html')


@app.route('/updateEmail', methods=['GET', 'POST'])
def updateEmail():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        new_email = request.form['email']

        try:
            entry = Users.query.filter_by(
                userName=_username).first()  # search for the correct entry
            entry.email = new_email

            db.session.commit()
            return render_template('home.html')

        except:
            print("Username and password not found please check credentials")
    return render_template('updateEmail.html')


@app.route('/deleteAccount', methods=['GET', 'POST', 'DELETE'])
def deleteAcc():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        try:
            delete_this = Users.query.filter_by(userName=_username).first()
            db.session.delete(delete_this)
            db.session.commit()
            return render_template('home.html')

        except:
            print(
                'Error in deleting your account please use a valid username and password')

    return render_template('deleteAcc.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
