
-----------------
GitHub Operations
-----------------

```
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
```

----------------------------------------------------------------
Python package management, virtual enviornment, and dependencies
----------------------------------------------------------------

```
$ sudo apt install python3-pip
$ sudo apt install python3-venv
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -e .
$ pip3 install '.[test]'
```

------------------------
Operational Dependencies
------------------------
```
$ sudo apt install gunicorn3
$ curl https://getcaddy.com | bash -s personal
$ sudo apt install ruby-foreman
```

-------------------
Running the Project
-------------------

Setup environment variables:

```
$ cd project_root/
$ export FLASK_APP=project1
$ export FLASK_ENV=development
$ export FLASK_RUN_HOST=127.0.0.1
$ export FLASK_RUN_PORT=2015
$ flask init-db
$ flask run
```

Open the web browser and go to URL:

http://localhost:2015/


-------------------
Running the tests
-------------------
Run these commands in the root directory of the project
Standard:
```
$ pytest
```
To file:
```
$ pytest >error.log
```
Less output:
```
$ pytest --tb=line
```


----------------------
WSGI Server Deployment
----------------------

Create WSGI python entrypoint of the application for gunicorn, on port `2015`:

	from python_file import flask_variable

	if __name__ == '__main__':
		flask_variable.run(host='127.0.0.1', port=2015)

Test gunicorn3 - (gunicorn3 py3_filename:app) :

    $ gunicorn3 main:app

Run a Flask application with 4 worker processes binding to localhost port 8000 (-b 127.0.0.1:8000)

    $ gunicorn3 -w 4 -b 127.0.0.1:8000 main:app

Open the web browser and go to URL:

http://127.0.0.1:8000

These instructions can be put in a PROCFILE, which has the following format:

    process1_nickname: shell_command_for_process1
    process2_nickname: shell_command_for_process2

Contents of the PROCFILE:

    main_test: gunicorn3 --bind 127.0.0.1:$PORT --access-logfile - --error-logfile - --log-level debug wsgi:app

**NOTE**: As per the [foreman documentation][1] if multiple instances of the same process are assigned `$PORT`, then each of them increments by 1, and the variable increments by 100 for each new process line in the `Procfile`

  [1]: https://ddollar.github.io/foreman/

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

**Explanation**:
All reqests coming to the application's votes page will be redirected to a proxies localhost:8100 localhost:8200 localhost:8300
The policy of those redirects would be to the server which has the least number of connections. Host information from the original request will be passed, similar to backend app.

Once the `caddyfile` (with the above content) is in the $APPHOME directory, it can be started with the following command:
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

Orchestration will be carried out with foreman. Before carrying out orchestration, the `Procfile` has to be updated with the caddy command.

Contents of the PROCFILE:

    main_test: gunicorn3 -w 4 -b 127.0.0.1:8000 --access-logfile gunicorn3_main main:app
    caddy_lbt: ulimit -n 8192 && caddy

Orchestration can now be run like, which starts all processes:

    $ foreman start -m main_test=3,caddy_lbt=1 --port 3000

**NOTE**: Worker processes will start with 3000, so if `main_test` has three worker processes, they will be bound to `3000`, `3001`, and `3002`.
The process (votes) will run on `3100`, `3101`, and `3102`, if it has 3 worker processes.
