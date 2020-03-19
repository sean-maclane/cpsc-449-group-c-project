To avoid problems, delete users.db and posts.db before each test.

Also, run the posts test after the user accounts test.


Windows PowerShell specific instructions to prepare application:

    $env:FLASK_ENV = "development"
    $env:FLASK_APP = "main.py" 
    flask run
      
Test application using:

    tavern-ci test_user_account.tavern.yaml
    tavern-ci test_posts.tavern.yaml
