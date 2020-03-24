import pytest
from flask import g
from flask import session

from project1.db import get_db

# Test /accounts/create
def test_accounts_create(client, app):
    # test that GET returns the create page
    assert client.get("/accounts/create").status_code == 200

    # test a valid create acocunt with POST
    assert client.post("/accounts/create", data={"username": "a", "email": "a@a.com", "password": "a"}).status_code == 201

    # A second time for future tests
    assert client.post("/accounts/create", data={"username": "c", "email": "c@c.com", "password": "c"}).status_code == 201

    # A third time for delete tests
    assert client.post("/accounts/create", data={"username": "delete", "email": "delete@delete.com", "password": "delete"}).status_code == 201

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'a'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "email", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Error in creating your account", 404),
        ("b", "a@a.com", "b", b"Email already in use", 404),
        ("a", "b@b.com", "a", b"Username already in use", 404),
        ("b", "noat.com", "b", b"Not proper Email", 404),
    ),
)
def test_accounts_create_validate(client, username, email, password, message, http_status_code):
    response = client.post(
        "/accounts/create", data={"username": username, "email": email, "password": password}
    )
    assert message in response.data
    assert http_status_code == response.status_code


# Test accounts/updateEmail
def test_accounts_updateEmail(client, app):
    # test that GET returns the create page
    assert client.get("/accounts/updateEmail").status_code == 200

    # test a valid create acocunt with POST
    assert client.post("/accounts/updateEmail", data={"username": "a", "email": "new_a@a.com", "password": "a"}).status_code == 201

    # test that the new email was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'a' and email = 'new_a@a.com'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "email", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Provided information", 404),
        ("nonexistant_username", "new_a@a.com", "wrong", b"No account to update email", 404),
        ("a", "", "a", b"Enter a new email for account", 404),
        ("a", "c@c.com", "c", b"Please provide a unique email", 404),
    ),
)
def test_accounts_updateEmail_validate(client, username, email, password, message, http_status_code):
    response = client.post(
        "/accounts/updateEmail", data={"username": username, "email": email, "password": password}
    )
    assert message in response.data
    assert http_status_code == response.status_code


# Test accounts/delete
def test_accounts_delete(client, app):
    # test that GET returns the create page
    assert client.get("/accounts/delete").status_code == 200

    # test a valid create acocunt with POST
    assert client.post("/accounts/create", data={"username": "to_delete", "email": "to@delete.com", "password": "to_delete"}).status_code == 201
    assert client.post("/accounts/delete", data={"username": "to_delete", "password": "to_delete"}).status_code == 201

    # test that the user was deleted from the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'to_delete'").fetchone()
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
    response = client.post(
        "/accounts/delete", data={"username": username, "password": password}
    )
    assert message in response.data
    assert http_status_code == response.status_code


# Test votes/upvote
def test_votes_upvote(client, app):
    # test that GET returns the create page
    assert client.get("/votes/upvote").status_code == 200

    # test a valid create acocunt with POST
    assert client.post("/votes/upvote", data={"username": "a", "password": "a"}).status_code == 201

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'a' and karma = '1'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "password", "message", "http_status_code"),
    (
        ("", "", b"Provide information", 404),
        ("nonexistant_username", "wrong", b"Create an account", 404),
    ),
)
def test_votes_upvote_validate(client, username, password, message, http_status_code):
    response = client.post(
        "/votes/upvote", data={"username": username, "password": password}
    )
    assert message in response.data
    assert http_status_code == response.status_code


# Test votes/downvote
def test_votes_downvote(client, app):
    # test that GET returns the create page
    assert client.get("/votes/downvote").status_code == 200

    # test a valid create acocunt with POST
    assert client.post("/votes/downvote", data={"username": "a", "password": "a"}).status_code == 201

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("select * from users where username = 'a' and karma = '0'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("username", "password", "message", "http_status_code"),
    (
        ("", "", b"Provide information", 404),
        ("nonexistant_username", "wrong", b"Create an account", 404),
    ),
)
def test_votes_downvote_validate(client, username, password, message, http_status_code):
    response = client.post(
        "/votes/downvote", data={"username": username, "password": password}
    )
    assert message in response.data
    assert http_status_code == response.status_code