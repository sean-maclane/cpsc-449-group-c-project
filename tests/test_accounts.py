import pytest
from flask import g
from flask import session

from project1.db import get_db

# Test /accounts/create
def test_accounts_create(client, app):
    url = "/accounts/create"

    # test a valid POST request
    valid_data = {"username": "test_accounts_create", "email": "test_accounts_create@test_accounts_create.com", "password": "test_accounts_create"}
    assert client.post(url, data=valid_data).status_code == 201

    # make a second test account, for future tests
    valid_data = {"username": "test_accounts_create_2", "email": "test_accounts_create_2@test_accounts_create_2.com", "password": "test_accounts_create_2"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'test_accounts_create'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "email", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Error in creating your account", 404),
        ("other", "test_accounts_create@test_accounts_create.com", "other", b"Email already in use", 404),
        ("test_accounts_create", "other@other.com", "other", b"Username already in use", 404),
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
    url = "/accounts/updateEmail"

    # test a valid POST request
    valid_data = {"username": "test_accounts_create", "email": "new_test_accounts_create@test_accounts_create.com", "password": "test_accounts_create"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the new email was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'test_accounts_create' and email = 'new_test_accounts_create@test_accounts_create.com'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "email", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Provided information", 404),
        ("nonexistant_username", "new@new.com", "nonexistant_password", b"No account to update email", 404),
        ("test_accounts_create", "", "test_accounts_create", b"Enter a new email for account", 404),
        ("test_accounts_create", "test_accounts_create_2@test_accounts_create_2.com", "test_accounts_create", b"Please provide a unique email", 404),
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
    url = "/accounts/delete"

    # test a valid POST request
    valid_data = {"username": "test_accounts_create_2", "password": "test_accounts_create_2"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the user was deleted from the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'test_accounts_create_2'").fetchone()
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
    url = "/votes/upvote"

    # test a valid POST request
    valid_data = {"username": "test_accounts_create", "password": "test_accounts_create"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the karma was incremented in the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'test_accounts_create' and karma = '1'").fetchone()
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
    url = "/votes/downvote"

    # test a valid POST request
    valid_data = {"username": "test_accounts_create", "password": "test_accounts_create"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the karma was decremented in the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'test_accounts_create' and karma = '0'").fetchone()
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