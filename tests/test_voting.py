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
    ("username", "password", "title", "message", "http_status_code"),
    (
        ("", "", "voting_upvote", b"Provide login information", 404),
    ),
)
def test_voting_upvote_validate(client, username, password, title, message, http_status_code):
    url = "/voting/upvote"
    bad_data = {"username": username, "password": password, "title": title}

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
        ("", "", b"Provide login information", 404),
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


@pytest.mark.parametrize(
    ("title", "community", "message", "http_status_code"),
    (
        ("", "", b"Provide a title and community", 404),
        ("", "voteSegregation", b"Provide a title", 404),
        ("voteSegregation", "", b"Provide a community", 404),
    ),
)
def test_voting_voteSegregation_validate(client, title, community, message, http_status_code):
    url = "/voting/voteSegregation"
    bad_data = {"title": title, "community": community}
    
    response = client.post(url, data=bad_data)
    
    assert http_status_code == response.status_code
    assert message in response.data


# Test voting/topScoring
def test_voting_topScoring(client, app):
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("topScoring", "topScoring@topScoring.com", "topScoring", 0))
        get_db().execute('INSERT INTO posts (title, community, text, username, url, dt, upvotes, downvotes) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', ("topScoring", "topScoring", "topScoring", "topScoring", "topScoring.com", datetime.now(), 0, 0))
        get_db().commit()

    url = '/voting/topScoring'

    valid_data = {"community": "topScoring"}
    top_scoring = client.post(url, data=valid_data)
    assert top_scoring.status_code == 201


@pytest.mark.parametrize(
    ("community", "message", "http_status_code"),
    (
        ("", b"Provide a community", 404),
    ),
)
def test_voting_topScoring_validate(client, community, message, http_status_code):
    url = "/voting/topScoring"
    bad_data = {"community": community}
    
    response = client.post(url, data=bad_data)
    
    assert http_status_code == response.status_code
    assert message in response.data
