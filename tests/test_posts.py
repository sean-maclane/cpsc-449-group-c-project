import pytest
from flask import g
from flask import session
from datetime import datetime

from project1.db import get_db


# Test /posts/create
def test_posts_create(client, app):
    # Add user for posts/create testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("posts_create", "posts@create.com", "posts_create", 0))
        get_db().commit()

    url = "/posts/create"

    # test a valid POST request
    valid_data = {"title": "posts_create", "community": "posts_create", "text": "posts_create", "username": "posts_create", "url": "posts_create.com"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the post was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM posts WHERE title = 'posts_create'").fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("title", "community", "text", "username", "url", "message", "http_status_code"),
    (
        ("", "", "", "", "", b"Please fill out information", 404),
        ("posts_create", "posts_create", "posts_create", "bad_username", "posts_create.com", b"Please make an account to post", 404),
    ),
)
def test_posts_create_validate(client, title, community, text, username, url, message, http_status_code):
    url = "/posts/create"
    bad_data = {"title": title, "community": community, "text": text, "username": username, "url": url}
    
    response = client.post(url, data=bad_data)

    assert message in response.data
    assert http_status_code == response.status_code


# Test /posts/retrieve
def test_posts_retrieve(client, app):
    # Add user and post for posts/retrieve testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("posts_retrieve", "posts@retrieve.com", "posts_retrieve", 0))
        get_db().execute('INSERT INTO posts (title, community, text, username, url, dt) VALUES (?, ?, ?, ?, ?, ?);', ("posts_retrieve", "posts_retrieve", "posts_retrieve", "posts_retrieve", "posts_retrieve.com", datetime.now()))
        get_db().commit()

    url = "/posts/retrieve"

    # test a valid POST request, CASE 1 retrieve all posts
    valid_data = {"title": "", "community": ""}
    case1_response = client.post(url, data=valid_data)
    assert case1_response.status_code == 201
    """ unstable section
    num_posts_retrieved = len(case1_response.data)
    with app.app_context():
        all_post_count = get_db().execute('SELECT COUNT(*) FROM posts')
        assert num_posts_retrieved == all_post_count
    """


    # test a valid POST request, CASE 2 retrieve all posts with title
    valid_data = {"title": "posts_retrieve", "community": ""}
    case2_response = client.post(url, data=valid_data)
    assert case2_response.status_code == 201
    """ unstable section
    num_posts_retrieved = len(case2_response.data)
    with app.app_context():
        all_post_count = get_db().execute("SELECT COUNT(*) FROM posts WHERE title = 'posts_retrieve'")
        assert num_posts_retrieved == all_post_count
    """

    # test a valid POST request, CASE 3 retrieve all posts from community
    valid_data = {"title": "", "community": "posts_retrieve"}
    case3_response = client.post(url, data=valid_data)
    assert case3_response.status_code == 201
    """ unstable section
    num_posts_retrieved = len(case3_response.data)
    with app.app_context():
        all_post_count = get_db().execute("SELECT COUNT(*) FROM posts WHERE community = 'posts_retrieve'")
        assert num_posts_retrieved == all_post_count
    """

    # test a valid POST request, CASE 4 retrieve all posts from title and community
    valid_data = {"title": "posts_retrieve", "community": "posts_retrieve"}
    case4_response = client.post(url, data=valid_data)
    assert case4_response.status_code == 201
    """ unstable section
    num_posts_retrieved = len(case4_response.data)
    with app.app_context():
        all_post_count = get_db().execute("SELECT COUNT(*) FROM posts WHERE title = 'posts_retrieve' AND community = 'posts_retrieve'")
        assert num_posts_retrieved == all_post_count
    """

@pytest.mark.parametrize(
    ("title", "community", "message", "http_status_code"),
    (
        ("bad_title", "posts_retrieve", b"Please provide a correct title", 404),
        ("posts_retrieve", "bad_community", b"Please make a community that exists", 404),
        ("bad_title", "bad_community", b"Check information", 404),
    ),
)
def test_posts_retrieve_validate(client, title, community, message, http_status_code):
    url = "/posts/retrieve"
    bad_data = {"title": title, "community": community}
    
    response = client.post(url, data=bad_data)

    assert message in response.data
    assert http_status_code == response.status_code


# Test posts/delete
def test_posts_delete(client, app):
    # Add user and post for posts/delete testing
    with app.app_context():
        get_db().execute('INSERT INTO users (username, email, password, karma) VALUES (?, ?, ?, ?);', ("posts_delete", "posts@delete.com", "posts_delete", 0))
        get_db().execute('INSERT INTO posts (title, community, text, username, url, dt) VALUES (?, ?, ?, ?, ?, ?);', ("posts_delete", "posts_delete", "posts_delete", "posts_delete", "posts_delete.com", datetime.now()))
        get_db().commit()

    url = "/posts/delete"

    # test a valid POST request
    valid_data = {"title": "posts_delete", "username": "posts_delete", "password": "posts_delete"}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the post was deleted from the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM posts where title = 'posts_delete'").fetchone()
            is None
        )

@pytest.mark.parametrize(
    ("title", "username", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Please provide information", 404),
        ("", "posts_delete", "posts_delete", b"Please provide title", 404),
        ("posts_delete", "", "", b"Please provide account info", 404),
        ("bad_title", "posts_delete", "posts_delete", b"Provide the correct post by the correct user", 404),
        ("posts_delete", "bad_username", "bad_password", b"Please provide correct user info", 404),
    ),
)
def test_posts_delete_validate(client, title, username, password, message, http_status_code):
    url = "/posts/delete"
    bad_data = {"title": title, "username": username, "password": password}

    response = client.post(url, data=bad_data)

    assert message in response.data
    assert http_status_code == response.status_code
