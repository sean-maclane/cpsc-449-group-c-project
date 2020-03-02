from flask import *
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_sqlalchemy import SQLAlchemy
import os


Base = declarative_base()

app = Flask(__name__)

db = SQLAlchemy(app)


class Users(Base):
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
            engine = create_engine('sqlite:///users.db', echo=True)
            Base.metadata.create_all(bind=engine)  # creates the table

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


@app.route('/login')
def loginpage():
    return render_template('loginpage.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
