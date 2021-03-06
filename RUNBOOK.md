----------------
Operating System
----------------
The preferred OS for this project is Tuffix 2020, details can be found on it at https://github.com/kevinwortman/tuffix .


As the current release (2020) seems to still be under development, we will include here the setup steps we followed:
1. Make a clean install of Ubunu 20.04 (we used a virtual machine)
2. run the following command in a terminal `wget https://csufcs.com/tuffixize -O - | bash`


While using Tuffix would ensure the best combatibility, we have comfirmed that the project runs just the same on a
plain Ubuntu 20.04 release as well.

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
$ sudo apt update
$ sudo apt install python3-pip
$ sudo apt install python3-venv
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install wheel
$ python setup.py bdist_wheel 
$ pip install -e .
```

------------------------
Operational Dependencies
------------------------

```
$ deactivate            # leave the virtual environment, if it is activated
$ pip3 install flask
$ pip3 install locust
$ . venv/bin/activate   # re-enter the virtual environment, if deactivated
$ sudo apt install gunicorn
$ curl https://getcaddy.com | bash -s personal
$ sudo apt install ruby-foreman
```

**Note**: When running the `foreman` command, packages _flask_ and _locust_ are picked up from the system's python3 site-packages directory.


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

-------------------------
Project Sanity (optional)
-------------------------

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


-------------------------
API Specification Testing
-------------------------
Follow the setup instructions above before testing. You will need to be in the virtual env and have run the given pip command.

Our API tests automatically create their own server instance and database, and remove them when complete. You do not need to be running an existing server for them to work.

Several command variants are provided below, each of them run the same tests but give output in different formats. Any or all of them can be used.

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

----------------------------
Orchestration & Load Testing
----------------------------

In a terminal tab, run the below **orchestration** command:

```
$ foreman start -m posts_test=3,votes_test=3,accounts_test=3,message_test=3,caddy_lbt=1 --port 3000
``` 

(**Note**: The load test will run until you press `Ctrl+c`.)


In another new terminal tab, run the below command for **synthetic load testing**:

```
$ locust -f locustfile.py --host=http://localhost:3000 --headless -u 100 -r 10
```

(**Note**: The locust test will run until you press `Ctrl+c`.)

where:

+ `f` — Path to the file
+ `headless` — Run the simulation without web interface
+ `u` — Number of users to simulate
+ `r` — Hatch rate (users spawned per second)
