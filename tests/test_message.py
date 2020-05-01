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
        get_db().execute('INSERT INTO messages (userfrom, userto, messagecontent,flag) VALUES (?, ?, ?, ?);',
                         ("bob", "mary", "hello", 0))
        get_db().commit()

    url = "/message/send"

    # test a valid POST request
    valid_data = {"userfrom": "bob",
                  "userto": "mary", "messagecontent": "hello", "flag": 0}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM messages WHERE userfrom = 'bob'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("userfrom", "userto", "messagecontent",
     "flag", "message", "http_status_code"),
    (
        ("", "mary", "hello", 0, b"No user from", 404),
        ("bob", "", "hello", 0, b"No user to", 404),
        ("bob", "mary", "", 0, b"No message", 404),

    ),
)
def test_message_send_validate(client, userfrom, userto, messagecontent, flag, message, http_status_code):
    url = "/message/send"
    bad_data = {"userfrom": userfrom, "userto": userto,
                "messagecontent": messagecontent, "flag": flag}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data


# Test message/delete
def test_message_delete(client, app):
    # Add user for delete testing
    with app.app_context():
        get_db().execute('INSERT INTO messages (userfrom, userto, messagecontent, flag) VALUES (?, ?, ?, ?);',
                         ("accounts_updateEmail", "accounts@updateEmail.com", "accounts_updateEmail", 0))
        get_db().execute('INSERT INTO messages (userfrom, userto, messagecontent, flag) VALUES (?, ?, ?, ?);',
                         ("accounts_updateEmail_2", "accounts_2@updateEmail_2.com", "accounts_updateEmail_2", 0))
        get_db().commit()

    url = "/message/delete"

    # test a valid POST request
    valid_data = {"userfrom": "accounts_updateEmail",
                  "messagecontent": "new_accounts@updateEmail.com"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the new email was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM messages WHERE userfrom = 'accounts_updateEmail' and email = 'new_accounts@updateEmail.com'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("userfrom", "messagecontent", "message", "http_status_code"),
    (
        ("", "", "", b"Provided information", 404),
        ("nonexistant_username", "new@new.com",
         "nonexistant_password", b"No account to update email", 404),
        ("accounts_updateEmail", "", "accounts_updateEmail",
         b"Enter a new email for account", 404),
    ),
)
def test_message_delete_validate(client, userfrom, messagecontent, message, http_status_code):
    url = "/message/delete"
    bad_data = {"userfrom": userfrom, "messagecontent": messagecontent}

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
    ("username", "message", "message", "http_status_code"),
    (
        ("", "", b"Provide Information", 404),
        ("nonexistant_username", "wrong", b"No account to delete", 404),
    ),
)
def test_message_favorite_validate(client, username, messagecontent, message, http_status_code):
    url = "/message/favorite"
    bad_data = {"username": username, "password": password}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data
