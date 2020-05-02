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
                         ("mary", "jane", "hello", 0))
        get_db().commit()

    url = "/message/send"

    # test a valid POST request
    valid_data = {"userfrom": "bob",
                  "userto": "ross", "messagecontent": "hola", "flag": 0}
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
        ("", "ross", "hello", 0, b"No user from", 404),
        ("bob", "", "hello", 0, b"No user to", 404),
        ("bob", "ross", "", 0, b"No message", 404),

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
                         ("delete", "message", "please", 0))
        get_db().commit()

    url = "/message/delete"

    # test a valid POST request
    valid_data = {"userfrom": "delete",
                  "messagecontent": "please"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the new email was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM messages WHERE userfrom = 'delete'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("userfrom", "messagecontent", "message", "http_status_code"),
    (
        ("", "hello", b"user doesn't exist", 404),
        ("bob", "", b"no message provided", 404),
    ),
)
def test_message_delete_validate(client, userfrom, messagecontent, message, http_status_code):
    url = "/message/delete"
    bad_data = {"userfrom": userfrom, "messagecontent": messagecontent}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data


# Test message/flag
def test_message_flag(client, app):
    # Add user for delete testing
    with app.app_context():
        get_db().execute('INSERT INTO messages (userfrom, userto, messagecontent, flag) VALUES (?, ?, ?, ?);',
                         ("flag", "this", "messagetest", 0))
        get_db().commit()

    url = "/message/flag"

    # test a valid POST request
    valid_data = {"messagecontent": "messagetest"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the user was deleted from the database
    with app.app_context():
        assert (
            get_db().execute("select * from messages where messagecontent = 'messagetest'").fetchone()
            is None
        )


@pytest.mark.parametrize(
    ("messagecontent", "message", "http_status_code"),
    (
        ("", b"message can't be found", 404),
    ),
)
def test_message_flag_validate(client, messagecontent, message, http_status_code):
    url = "/message/flag"
    bad_data = {"messagecontent": messagecontent}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data
