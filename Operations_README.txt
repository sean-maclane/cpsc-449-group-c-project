-----------------
GitHub Operations
-----------------

$ git --version                         # Check current git version
$ git config --global user.name "Firstname Lastname"
$ git config --global user.email "username@domain.com"
$ git config --global core.autocrlf     # Unix line endings
$ git config --list                     # Verify all configurations

$ cd project_directory
$ git init
$ git remote add origin https://github.com/sean-maclane/cpsc-449-group-c-project-1
$ git pull origin master
<<Enter github username and password>>


-----------------------------------
Python and Application Dependencies
-----------------------------------
$ sudo apt install python3-pip
$ pip3 install flask
$ pip3 install marshmallow
$ python3 -m flask --version


-------------------
Running the Project
-------------------

$ cd project_directory/reddit-like/dev1-Preston/
$ export FLASK_ENV=development
$ export FLASK_APP=app3.py
$ flask run

<<Open the web browser and go to URL>>
http://localhost:5000/


------------------------
Operational Dependencies
------------------------

$ sudo apt install gunicorn3
$ curl https://getcaddy.com | bash -s personal
$ sudo apt install ruby-foreman


----------------------
WSGI Server Deployment
----------------------

Test gunicorn3 - (gunicorn3 py3_filename:app) :
$ gunicorn3 main:app

Run a Flask application with 4 worker processes binding to localhost port 8000 (-b 127.0.0.1:8000)
$ gunicorn3 -w 4 -b 127.0.0.1:8000 main:app

<<Open the web browser and go to URL>>
127.0.0.1:8000

These instructions can be put in a PROCFILE, which has the following format:
process1_nickname: shell_command_to_run_process1
process2_nickname: shell_command_to_run_process2

Actual contents of the PROCFILE:
main_test: gunicorn3 -w 4 -b 127.0.0.1:8000 --access-logfile gunicorn3_main main:app

Start 3 instances of each microservice (Procfile has to be present):
$ foreman start -c


--------------
Load Balancing
--------------

To perform the below operations:
    Requests for http://localhost:2015/posts to be redirected to the Posting microservice, and 
    Requests for http://localhost:2015/votes to be redirected to the Voting microservice

A CADDYFILE would have to be created and the content would look like:
    
    localhost:8000/votes {
        proxy / localhost:8100 localhost:8200 localhost:8300 {
            policy least_conn
            transparent
        }        
    }
    
    localhost:8000/posts {
        proxy / localhost:8101 localhost:8201 localhost:8301 {
            policy least_conn
            transparent
        }
    }

Explanation:
All reqests coming to the application's votes page will be redirected to a proxies localhost:8100 localhost:8200 localhost:8300
The policy of those redirects would be to the server which has the least number of connections. Host information from the original request will be passed, similar to backend app.

Once the CADDYFILE (with the above content) is in the $APPHOME directory, it can be started with the following command:
$ ulimit -n 8192 && caddy


Modifying ulimit (in case the above command gives an error on Linux):

    Check current soft limit
    $ ulimit -n
    
    Check current hard limit
    $ ulimit -Hn
    
    Add the below lines in /etc/security/limits.conf at the end:
    your_username hard nofile 16384
    your_username soft nofile 16384
    
    Set (or uncomment and set) DefaultLimitNOFILE=16384 in files:
    /etc/systemd/user.conf
    /etc/systemd/system.conf
    
    Add the line:
    session required pam_limits.so
    to files:
    /etc/pam.d/common-session
    /etc/pam.d/common-session-noninteractive
    
    Restart PC


-------------
Orchestration
-------------

Orchestration will be carries out with foreman.

Before carrying out orchestration, the PROCFILE has to be updated with the caddy command.

Contents of the PROCFILE:
main_test: gunicorn3 -w 4 -b 127.0.0.1:8000 --access-logfile gunicorn3_main main:app
caddy: ulimit -n 8192 && caddy

Orchestration can now be run like, which starts all processes
$ foreman start -m all=1
