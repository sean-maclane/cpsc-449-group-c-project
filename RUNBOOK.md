
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
$ git remote add origin https://github.com/sean-maclane/cpsc-449-group-c-project
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
$ pip install -e .
```

------------------------
Operational Dependencies
------------------------

```
$ sudo apt install gunicorn3
$ curl https://getcaddy.com | bash -s personal
$ sudo apt install ruby-foreman
```

----------------------------
Setting up project variables
----------------------------

```
$ cd project_root/
$ export FLASK_APP=project
$ export FLASK_ENV=development
$ export FLASK_RUN_HOST=127.0.0.1
$ export FLASK_RUN_PORT=2015
$ flask init-db
```

--------------
Project Sanity
--------------

Check whether the below command works:

```
$ ulimit -n 8192 && caddy
```

The output should be:
```
Activating privacy features... done.

Serving HTTP on port 2015 
http://:2015

```

If you get the above output, press `Ctrl-c` and go to the next section; If not follow the below process to modify ulimit:

Step 1: Check current soft limit:
```
$ ulimit -n
```

Step 2: Check current hard limit
```
$ ulimit -Hn
```

Step 3: Add the below lines in `/etc/security/limits.conf` at the end:
```
your_username hard nofile 16384
your_username soft nofile 16384
```

Step 4: Set (or uncomment and set) `DefaultLimitNOFILE=16384` in files:
```
/etc/systemd/user.conf
/etc/systemd/system.conf
```

Step 5: Add line `session required pam_limits.so` to files:
```
/etc/pam.d/common-session
/etc/pam.d/common-session-noninteractive
```

Step 6: Restart PC

-------------
Orchestration
-------------

```
$ foreman start -m posts_test=3,votes_test=3,accounts_test=3,message_test=3,caddy_lbt=1 --port 3000
``` 

-------------------------
API Specification Testing
-------------------------
Follow the setup instructions above before testing. You will need to be in the virtual env and have run the given pip command.

These tests automatically create their own server instance and database, and remove them when complete. You do not need to be running an existing server for them to work.

Standard `pytest` run:

```
$ pytest
```

Redirect the output of `pytest` to `error.log` file:

```
$ pytest >error.log
```

Enable traceback for one line per failure:

```
$ pytest --tb=line
```
In these tests, the dots indicate sucess, F's indicade the API was not followed, and E's indicate a critical error.

------------
Load Testing
------------
Before load testing, open a separate terminal and follow the instructions in the runbook for starting a server under orchestration. The load test will run until you press ctr+c.

Please note that this generates so much data that it overwhelms the SQLite database, and eventualy the db locks up. This would not happen if we were running a database such as MySQL, but that is out of the scope of this project.

```
$ locust -f locustfile.py --host=http://localhost:2015 --no-web -c 100 -r 10
```
where:

+ `f` — Path to the file
+ `no-web` — Run the simulation without web interface
+ `c` — Number of users to simulate
+ `r` — Hatch rate (users spawned per second)
