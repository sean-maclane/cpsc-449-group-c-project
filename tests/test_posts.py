import pytest
from flask import g
from flask import session

from project1.db import get_db

test_data_1 = {
    "title": "test_posts_1",
    "community": "test_posts_1",
    "text": "test_posts_1",
    "username": "test_posts_1",
    "email": "test_posts_1@test_posts_1.com",
    "password": "test_posts_1",
    "url": "test_posts_1"
}

test_data_2 = {
    "title": "test_posts_2",
    "community": "test_posts_2",
    "text": "test_posts_2",
    "username": "test_posts_2",
    "email": "test_posts_2@test_posts_2.com",
    "password": "test_posts_2",
    "url": "test_posts_2"
}

# Test /posts/create
def test_posts_create(client, app):
    url = "/posts/create"

    # Create the account we will be testing posts with
    post_account_data = {"username": test_data_1['username'], "email": test_data_1['email'], "password": test_data_1['password']}
    client.post("/accounts/create", data=post_account_data)
    
    # Create a second account for testing
    post_account_data = {"username": test_data_2['username'], "email": test_data_2['email'], "password": test_data_2['password']}
    client.post("/accounts/create", data=post_account_data)

    # test a valid POST request
    valid_data = {"title": test_data_1['title'], "community": test_data_1['community'], "text": test_data_1['text'], "username": test_data_1['username'], "url": test_data_1['url']}
    assert client.post(url, data=valid_data).status_code == 201

    # create a second post for testing
    valid_data = {"title": test_data_2['title'], "community": test_data_2['community'], "text": test_data_2['text'], "username": test_data_2['username'], "url": test_data_2['url']}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the post was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("select * from posts where title = ?", (test_data_1['title'])).fetchone()
            is not None
        )

@pytest.mark.parametrize(
    ("title", "community", "text", "username", "url", "message", "http_status_code"),
    (
        ("", "", "", "", "", b"Please fill out information", 404),
        (test_data_1['title'], test_data_1['community'], test_data_1['text'], "bad_username", test_data_1['url'], b"Please make an account to post", 404),
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
    url = "/posts/retrieve"

    # test a valid POST request, CASE 1 retrieve all posts
    valid_data = {"title": "", "community": ""}
    assert client.post(url, data=valid_data).status_code == 201

    # test a valid POST request, CASE 2 retrieve all posts with title
    valid_data = {"title": test_data_1['title'], "community": ""}
    assert client.post(url, data=valid_data).status_code == 201

    # test a valid POST request, CASE 3 retrieve all posts from community
    valid_data = {"title": "", "community": test_data_1['community']}
    assert client.post(url, data=valid_data).status_code == 201

    # test a valid POST request, CASE 4 retrieve all posts from title and community
    valid_data = {"title": test_data_1['title'], "community": test_data_1['community']}
    assert client.post(url, data=valid_data).status_code == 201

@pytest.mark.parametrize(
    ("title", "community", "message", "http_status_code"),
    (
        ("bad_title", test_data_1['community'], b"Please provide a correct title", 404),
        (test_data_1['community'], "bad_community", b"Please make a community that exists", 404),
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
    url = "/posts/delete"

    # test a valid POST request
    valid_data = {"title": test_data_1['title'], "username": test_data_1['username'], "password": test_data_1['password']}
    assert client.post(url, data=valid_data).status_code == 201

    # test that the post was deleted from the database
    with app.app_context():
        assert (
            get_db().execute("select * from posts where title = ?", (test_data_1['title'])).fetchone()
            is None
        )

@pytest.mark.parametrize(
    ("title", "username", "password", "message", "http_status_code"),
    (
        ("", "", "", b"Please provide information", 404),
        ("", test_data_1['username'], test_data_1['password'], b"Please provide title", 404),
        (test_data_1['title'], "", "", b"Please provide account info", 404),
        ("bad_title", test_data_1['username'], test_data_1['password'], b"Provide the correct post by the correct user", 404),
        (test_data_2['title'], "bad_username", "bad_password", b"Please provide correct use info", 404),
    ),
)
def test_posts_delete_validate(client, title, username, password, message, http_status_code):
    url = "/posts/delete"
    bad_data = {"title": title, "username": username, "password": password}

    response = client.post(url, data=bad_data)

    assert message in response.data
    assert http_status_code == response.status_code
