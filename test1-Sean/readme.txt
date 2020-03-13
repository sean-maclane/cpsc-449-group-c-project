It is assumed for this guide that you have all the correct dependencies installed (python, etc)  

To run the tests, first start up the server (instructions for windows at this time):
    1. Change your working directory do dev1-Preston
    2. in powershell, run:
        $env:FLASK_ENV = "development"
        $env:FLASK_APP = "backup.py" 
        flask run
    3. Change your working directory to test1-Sean in another powershell instance
    4. in powershell, run:
        tavern-ci test_user_account.tavern.yaml
        tavern-ci test_posting.tavern.yaml
