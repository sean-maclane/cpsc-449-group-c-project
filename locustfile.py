from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """
        First task that will be executed on locust start will be the homepage
        check
        """
        self.app_homepage()

    @task
    def app_homepage(self):
        self.client.get('/')

    @task
    def votes_home(self):
        self.client.get('/votes')

    @task
    def posts_home(self):
        self.client.get('/posts')

    @task
    def registered_user(self):
        """
        Check login of registered users
        """
        self.client.post("/login",
            {"username":"existing_user1", "password":"password123"})
        self.client.post("/login",
            {"username":"existing_user2", "password":"password123"})
        self.client.post("/login",
            {"username":"existing_user2", "password":"password123"})

    @task
    def unregistered_user(self):
        """
        Negative testing of unregistered/fake users
        """
        self.client.post("/login",
            {"username":"testuser1", "password":"password123"})
        self.client.post("/login",
            {"username":"testuser2", "password":"password123"})
        self.client.post("/login",
            {"username":"testuser3", "password":"password123"})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior()
