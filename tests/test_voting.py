import pytest
from flask import g
from flask import session
from flask import *
import json

from project.db import get_db


# Test voting/upvote
def test_voting_upvote(client, app):
    # Test increment
    with app.app_context():
        get_db().execute("UPDATE posts SET upvotes=upvotes+1 WHERE title = ?;", ("voting_upvote"))
        get_db().commit()

    url = "/voting/upvote"

    # test a valid POST request
    valid_data = {"username": "voting_upvote", "password": "voting_upvote", "title": "voting_upvote"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the upvote was incremented in the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM voting WHERE title = 'voting_upvote'").fetchone()
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
    # test decrement
    with app.app_context():
        get_db().execute("UPDATE posts SET downvotes=downvotes+1 WHERE title = ?;", ("voting_downvote"))
        get_db().commit()

    url = "/voting/downvote"

    # test a valid POST request
    valid_data = {"username": "voting_downvote", "password": "voting_downvote", "title": "voting_downvote"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the upvote was incremented in the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM voting WHERE title = 'voting_downvote'").fetchone()
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
        get_db().execute("SELECT upvotes, downvotes FROM posts WHERE title = ? AND community = ?;", ("voteSegregation", "voteSegregation"))
        get_db().commit()

    url = '/voting/voteSegregation'

    valid_data = {"title": "voting_downvote", "community": "voteSegregation"}
    assert client.post(url, data=valid_data).status_code == 201

    # test vote segregation in the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM voting WHERE title = 'voteSegregation' and community = 'voteSegregation'").fetchone()
            is not None
        )