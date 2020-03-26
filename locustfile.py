from locust import HttpLocust, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        """
        First task that will be executed on locust start will be the homepage
        check
        """
        self.app_homepage()

    @task
    def app_homepage(self):
        response = self.client.get('/')
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
    
    '''
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

	@task
    def create_account(self):
        self.client.get('/accounts/create')

	@task
    def update_email(self):
        self.client.get('/accounts/updateEmail')

	@task
    def delete_account(self):
        self.client.get('/accounts/delete')
    '''

    @task
    def unregistered_user(self):
        """
        Negative testing of unregistered/fake users
        """
        self.client.post("/accounts/delete",
            {"username":"testuser1", "password":"password123"})
        self.client.post("/accounts/delete",
            {"username":"testuser2", "password":"password123"})
        self.client.post("/accounts/delete",
            {"username":"testuser3", "password":"password123"})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)
