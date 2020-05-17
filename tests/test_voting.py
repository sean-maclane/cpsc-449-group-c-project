import pytest
from flask import g
from flask import session
from flask import *
from datetime import datetime
import json

from project.db import get_db


# Test voting/upvote
def test_voting_upvote(client, app):
    # Add users and posts before testing upvote
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("voting_upvote", "voting@upvote.com", "voting_upvote", 0))
        get_db().execute('INSERT INTO posts (title, community, text, username, url, dt, upvotes, downvotes) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', ("voting_upvote", "voting_upvote", "voting_upvote", "voting_upvote", "voting_upvote.com", datetime.now(), 0, 0))
        get_db().commit()

    url = "/voting/upvote"

    # test a valid POST request
    valid_data = {"username": "voting_upvote", "password": "voting_upvote", "title": "voting_upvote", "id": "voting_upvote"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the upvote was incremented in the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM posts WHERE username = 'voting_upvote' and upvotes = '1'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "password", "message", "http_status_code"),
    (
        ("", "", b"Provide information", 404),
        ("nonexistant_username", "nonexistant_password", b"Create an account", 404),
    ),
)
def test_voting_upvote_validate(client, username, password, message, http_status_code):
    url = "/voting/upvote"
    bad_data = {"username": username, "password": password}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data


# Test voting/downvote
def test_voting_downvote(client, app):
    # Add users and posts before testing downvote
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("voting_downvote", "voting@downvote.com", "voting_downvote", 0))
        get_db().execute('INSERT INTO posts (title, community, text, username, url, dt, upvotes, downvotes) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', ("voting_downvote", "voting_downvote", "voting_downvote", "voting_downvote", "voting_downvote.com", datetime.now(), 0, 0))
        get_db().commit()

    url = "/voting/downvote"

    # test a valid POST request
    valid_data = {"username": "voting_downvote", "password": "voting_downvote", "title": "voting_downvote", "id": "voting_downvote"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the upvote was incremented in the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM posts WHERE username = 'voting_downvote' and downvotes = '1'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "message", "http_status_code"),
    (
        ("", "", b"Provide information", 404),
        ("nonexistant_username", "nonexistant_password", b"Create an account", 404),
    ),
)
def test_voting_downvote_validate(client, username, password, message, http_status_code):
    url = "/voting/downvote"
    bad_data = {"username": username, "password": password}
    
    response = client.post(url, data=bad_data)
    
    assert http_status_code == response.status_code
    assert message in response.data


# Test voting/voteSegregation
def test_voting_voteSegregation(client, app):
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("voteSegregation", "vote@segregation.com", "voteSegregation", 0))
        get_db().execute('INSERT INTO posts (title, community, text, username, url, dt, upvotes, downvotes) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', ("voteSegregation", "voteSegregation", "voteSegregation", "voteSegregation", "voteSegregation.com", datetime.now(), 0, 0))
        get_db().commit()

    url = '/voting/voteSegregation'

    valid_data = {"title": "voteSegregation", "community": "voteSegregation"}
    vote_segregation = client.post(url, data=valid_data)
    assert vote_segregation.status_code == 201
    #assert client.post(url, data=valid_data).status_code == 201

    # test vote segregation in the database
    # with app.app_context():
    #     assert (
    #         get_db().execute("SELECT upvotes, downvotes FROM posts WHERE title = 'voteSegregation' and community = 'voteSegregation'").fetchone()
    #         is not None
    #     )


@pytest.mark.parametrize(
    ("title", "community", "message", "http_status_code"),
    (
        ("", "", b"Provide information", 404),
        ("nonexistant_title", "nonexistant_community", b"Create an account", 404),
    ),
)
def test_voting_voteSegregation_validate(client, title, community, message, http_status_code):
    url = "/voting/voteSegregation"
    bad_data = {"title": title, "community": community}
    
    response = client.post(url, data=bad_data)
    
    assert http_status_code == response.status_code
    assert message in response.data

