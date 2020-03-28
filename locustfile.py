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

        self.create_account()
    
    def on_stop(self):
        self.delete_account()

    def create_account(self):
        url = "/accounts/create"
        data = {"username": self.username , "password": self.password, "email": self.email}
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

    '''
    @task
    def app_homepage(self):
        response = self.client.get('/')
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
    
	To be verifies with test cases GET, POST, etc.
    @task
    def upvote(self):
        self.client.get('/votes/upvote')
        
    @task
    def downvote(self):
        self.client.get('/votes/downvote')

    @task
    def create_post(self):
        self.client.get('/posts/create')
        
    @task
    def delete_post(self):
        self.client.get('/posts/delete')
        
    @task
    def retrieve_post(self):
        self.client.get('/posts/retrieve')
    '''

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)
