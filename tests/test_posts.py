import pytest
from flask import g
from flask import session
from datetime import datetime

from project.db import get_db


# Test /posts/create
def test_posts_create(client, app):
    # Add user for posts/create testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("posts_create", "posts@create.com", "posts_create", 0))
        get_db().commit()

    url = "/posts/create"

    # test a valid POST request
    valid_data = {"title": "posts_create", "community": "posts_create", "text": "posts_create", "username": "posts_create"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the post was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM posts WHERE title = 'posts_create'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("title", "community", "text", "username", "message", "http_status_code"),
    (
        ("", "", "", "", b"Please fill out information", 404),
    ),
)
def test_posts_create_validate(client, title, community, text, username,message, http_status_code):
    url = "/posts/create"
    bad_data = {"title": title, "community": community, "text": text, "username": username}
    
    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data


# Test /posts/retrieve
def test_posts_retrieve(client, app):
    # Add user and post for posts/retrieve testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("posts_retrieve", "posts@retrieve.com", "posts_retrieve", 0))
        get_db().execute('INSERT INTO posts (title, community, text, username, url, dt, upvotes, downvotes) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', ("posts_retrieve", "posts_retrieve", "posts_retrieve", "posts_retrieve", "posts_retrieve.com", datetime.now(), 0, 0))
        get_db().commit()

    url = "/posts/retrieve"

    # test a valid POST request
    valid_data = {"title": "posts_retrieve", "community": "posts_retrieve"}
    case4_response = client.post(url, data=valid_data)
    assert case4_response.status_code == 201

@pytest.mark.parametrize(
    ("title", "community", "message", "http_status_code"),
    (
        ("", "posts_retrieve", b"Provide a title", 404),
        ("posts_retrieve", "", b"Provide a community", 404),
        ("", "", b"Provide a title and community", 404),
    ),
)
def test_posts_retrieve_validate(client, title, community, message, http_status_code):
    url = "/posts/retrieve"
    bad_data = {"title": title, "community": community}
    
    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data


# Test posts/delete
def test_posts_delete(client, app):
    # Add user and post for posts/delete testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("posts_delete", "posts@delete.com", "posts_delete", 0))
        get_db().execute('INSERT INTO posts (title, community, text, username, url, dt, upvotes, downvotes) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', ("posts_delete", "posts_delete", "posts_delete", "posts_delete", "posts_delete.com", datetime.now(), 0, 0))
        get_db().commit()

    url = "/posts/delete"

    # test a valid POST request
    valid_data = {"title": "posts_delete", "username": "posts_delete", "password": "posts_delete"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the post was deleted from the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM posts WHERE title = 'posts_delete'").fetchone()
            is None
        )

@pytest.mark.parametrize(
    ("title", "username", "password", "message", "http_status_code"),
    (
        ("posts_delete", "", "posts_delete", b"Please provide username", 404),
        ("", "posts_delete", "posts_delete", b"Please provide title", 404),
        ("posts_delete", "posts_delete", "", b"Please provide password", 404),
    ),
)
def test_posts_delete_validate(client, title, username, password, message, http_status_code):
    url = "/posts/delete"
    bad_data = {"title": title, "username": username, "password": password}

    response = client.post(url, data=bad_data)

    assert http_status_code == response.status_code
    assert message in response.data
