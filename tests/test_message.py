import pytest
from flask import g
from flask import session
from flask import *
import json

from project1.db import get_db


# Test /message/send
def test_message_send(client, app):
    # Add existing message for error testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);',
                         ("existing_accounts_create", "existing_accounts@create.com", "existing_accounts_create", 0))
        get_db().commit()

    url = "/message/send"

    # test a valid POST request
    valid_data = {"username": "accounts_create",
                  "email": "accounts@create.com", "password": "accounts_create"}
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
        ("other2", "bademail.com", "other2", b"Not proper Email", 404),
    ),
)
def test_message_send_validate(client, username, email, password, message, http_status_code):
    url = "/message/send"
    bad_data = {"username": username, "email": email, "password": password}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data


# Test message/delete
def test_message_delete(client, app):
    # Add user for delete testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);',
                         ("accounts_updateEmail", "accounts@updateEmail.com", "accounts_updateEmail", 0))
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);',
                         ("accounts_updateEmail_2", "accounts_2@updateEmail_2.com", "accounts_updateEmail_2", 0))
        get_db().commit()

    url = "/message/delete"

    # test a valid POST request
    valid_data = {"username": "accounts_updateEmail",
                  "email": "new_accounts@updateEmail.com", "password": "accounts_updateEmail"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the new email was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM users WHERE username = 'accounts_updateEmail' and email = 'new_accounts@updateEmail.com'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "email", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Provided information", 404),
        ("nonexistant_username", "new@new.com",
         "nonexistant_password", b"No account to update email", 404),
        ("accounts_updateEmail", "", "accounts_updateEmail",
         b"Enter a new email for account", 404),
    ),
)
def test_message_delete_validate(client, username, email, password, message, http_status_code):
    url = "/message/delete"
    bad_data = {"username": username, "email": email, "password": password}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data


# Test message/favorite
def test_message_favorite(client, app):
    # Add user for delete testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);',
                         ("accounts_delete", "accounts@delete.com", "accounts_delete", 0))
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
def test_message_favorite_validate(client, username, password, message, http_status_code):
    url = "/message/favorite"
    bad_data = {"username": username, "password": password}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data
