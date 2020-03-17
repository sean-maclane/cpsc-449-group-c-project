It is assumed for this guide that you have all the correct dependencies installed (python, etc)  

To avoid problems, delete users.db and posts.db before each test

To run the tests, first start up the server (instructions for windows at this time):
    1. in powershell, run:
        $env:FLASK_ENV = "development"
        $env:FLASK_APP = "main.py" 
        flask run
    2. in powershell, run:
        tavern-ci test_user_account.tavern.yaml
        tavern-ci test_posting.tavern.yaml
