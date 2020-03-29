def get_unique_username():
    id = 0
    base_string = "locust_username_"
    while True:
        id = id + 1
        yield base_string + str(id)

def get_unique_email():
    id = 0
    base_string = "locust@email_"
    while True:
        id = id + 1
        yield base_string + str(id)

def get_unique_password():
    id = 0
    base_string = "locust_password_"
    while True:
        id = id + 1
        yield base_string + str(id)

def get_unique_post_title():
    id = 0
    base_string = "locust_post_title_"
    while True:
        id = id + 1
        yield base_string + str(id)

def get_unique_post_text():
    id = 0
    base_string = "locust_post_text_"
    while True:
        id = id + 1
        yield base_string + str(id)

def get_unique_community():
    id = 0
    base_string = "locust_community_"
    while True:
        id = id + 1
        yield base_string + str(id)
