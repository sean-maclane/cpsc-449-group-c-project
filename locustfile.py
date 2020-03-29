from locust import HttpLocust, TaskSet, task, between
from generators import *

username_generator = get_unique_username()
email_generator = get_unique_email()
password_generator = get_unique_password()
post_title_generator = get_unique_post_title()
post_text_generator = get_unique_post_text()
community_generator = get_unique_community()


class UserBehavior(TaskSet):
    def on_start(self):
        """
        First task that will be executed on locust start will be the homepage
        check
        """
        self.username = next(username_generator)
        self.email = next(email_generator)
        self.password = next(password_generator)
        self.post_title = next(post_title_generator)
        self.post_body = next(post_text_generator)
        self.community = next(community_generator)

        self.hello_world()
        self.create_account()
    
    def on_stop(self):
        self.delete_account()

    def hello_world(self):
        url = "/hello"
        self.client.get(url)

    def create_account(self):
        url = "/accounts/create"
        data = {"username": self.username, "password": self.password, "email": self.email}
        self.client.post(url, data)

    def delete_account(self):
        url = "/accounts/delete"
        data = {"username": self.username , "password": self.password}
        self.client.post(url, data)

    @task(1)
    def update_email(self):
        self.email = next(email_generator)
        
        url = "/accounts/updateEmail"
        data = {"username": self.username , "password": self.password, "email": self.email}
        self.client.post(url, data)

    @task
    def upvote(self):
        upvote_url = '/votes/upvote'
        upvote_data = {'username': self.username, 'password': self.password}
        self.client.post(upvote_url, upvote_data)
        
    @task
    def downvote(self):
        downvote_url = '/votes/downvote'
        downvote_data = {'username': self.username, 'password': self.password}
        self.client.post(downvote_url, downvote_data)

    @task(1)
    def retrieve_post(self):
        retrieve_url = '/posts/retrieve'
        retrieve_data = {'title': self.post_title, 'community': self.community}
        self.client.post(retrieve_url, retrieve_data)

    @task
    def create_post(self):
        createpost_url = '/posts/create'
        createpost_data = {
            'title': self.post_title,
            'community': self.community,
            'text': self.post_body,
            'username': self.username,
            'url': 'posts_create.com'
        }
        self.client.post(createpost_url, createpost_data)
        
    @task
    def delete_post(self):
        deletepost_url = '/posts/delete'
        deletepost_data = {
            'title': self.post_title,
            'username': self.username,
            'password': self.password
        }
        self.client.post(deletepost_url, deletepost_data)
    

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)
