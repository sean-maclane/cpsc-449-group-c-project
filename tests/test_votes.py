import pytest
from flask import g
from flask import session
from flask import *
import json

from project1.db import get_db


# Test votes/upvote
def test_votes_upvote(client, app):
    # Add user for upvote testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("votes_upvote", "votes@upvote.com", "votes_upvote", 0))
        get_db().commit()

    url = "/votes/upvote"

    # test a valid POST request
    valid_data = {"username": "votes_upvote", "password": "votes_upvote"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the karma was incremented in the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM users WHERE username = 'votes_upvote' and karma = '1'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "password", "message", "http_status_code"),
    (
        ("", "", b"Provide information", 404),
        ("nonexistant_username", "nonexistant_password", b"Create an account", 404),
    ),
)
def test_votes_upvote_validate(client, username, password, message, http_status_code):
    url = "/votes/upvote"
    bad_data = {"username": username, "password": password}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data


# Test votes/downvote
def test_votes_downvote(client, app):
    # Add user for downvote testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("votes_downvote", "votes@downvote.com", "votes_downvote", 0))
        get_db().commit()
    
    url = "/votes/downvote"

    # test a valid POST request
    valid_data = {"username": "votes_downvote", "password": "votes_downvote"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the karma was decremented in the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM users WHERE username = 'votes_downvote' and karma = '-1'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "password", "message", "http_status_code"),
    (
        ("", "", b"Provide information", 404),
        ("nonexistant_username", "nonexistant_password", b"Create an account", 404),
    ),
)
def test_votes_downvote_validate(client, username, password, message, http_status_code):
    url = "/votes/downvote"
    bad_data = {"username": username, "password": password}
    
    response = client.post(url, data=bad_data)
    
    assert http_status_code == response.status_code
    assert message in response.data
    