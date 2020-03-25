import pytest
from flask import g
from flask import session
from flask import *
import json

from project1.db import get_db

# Test /accounts/create
def test_accounts_create(client, app):
    url = "/accounts/create"

    # test a valid POST request
    valid_data = {"username": "accounts_create", "email": "accounts@create.com", "password": "accounts_create"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM users WHERE username = 'accounts_create'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "email", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Error in creating your account", 404),
        ("other", "accounts@create.com", "other", b"Email already in use", 404),
        ("accounts_create", "other@other.com", "other", b"Username already in use", 404),
        ("other", "bademail.com", "other", b"Not proper Email", 404),
    ),
)
def test_accounts_create_validate(client, username, email, password, message, http_status_code):
    url = "/accounts/create"
    bad_data = {"username": username, "email": email, "password": password}
    
    response = client.post(url, data=bad_data)

    assert message in response.data
    assert http_status_code == response.status_code


# Test accounts/updateEmail
def test_accounts_updateEmail(client, app):
    # Add user for delete testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("accounts_updateEmail", "accounts@updateEmail.com", "accounts_updateEmail", 0))
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("accounts_updateEmail_2", "accounts_2@updateEmail_2.com", "accounts_updateEmail_2", 0))
        get_db().commit()
    
    url = "/accounts/updateEmail"

    # test a valid POST request
    valid_data = {"username": "accounts_updateEmail", "email": "new_accounts@updateEmail.com", "password": "accounts_updateEmail"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the new email was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'test_accounts_create' and email = 'new_accounts@updateEmail.com'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "email", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Provided information", 404),
        ("nonexistant_username", "new@new.com", "nonexistant_password", b"No account to update email", 404),
        ("accounts_updateEmail", "", "accounts_updateEmail", b"Enter a new email for account", 404),
        ("accounts_updateEmail", "accounts_2@updateEmail_2.com", "accounts_updateEmail", b"Please provide a unique email", 404),
    ),
)
def test_accounts_updateEmail_validate(client, username, email, password, message, http_status_code):
    url = "/accounts/updateEmail"
    bad_data = {"username": username, "email": email, "password": password}
    
    response = client.post(url, data=bad_data)

    assert message in response.data
    assert http_status_code == response.status_code


# Test accounts/delete
def test_accounts_delete(client, app):
    # Add user for delete testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("accounts_delete", "accounts@delete.com", "accounts_delete", 0))
        get_db().commit()

    url = "/accounts/delete"

    # test a valid POST request
    valid_data = {"username": "accounts_delete", "password": "accounts_delete"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the user was deleted from the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'accounts_delete'").fetchone()
            is None
        )

@pytest.mark.parametrize(
    ("username", "password", "message", "http_status_code"),
    (
        ("", "", b"Provide Information", 404),
        ("nonexistant_username", "wrong", b"No account to delete", 404),
    ),
)
def test_accounts_delete_validate(client, username, password, message, http_status_code):
    url = "/accounts/delete"
    bad_data = {"username": username, "password": password}

    response = client.post(url, data=bad_data)

    assert message in response.data
    assert http_status_code == response.status_code


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

    assert message in response.data
    assert http_status_code == response.status_code


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
    
    assert message in response.data
    assert http_status_code == response.status_code