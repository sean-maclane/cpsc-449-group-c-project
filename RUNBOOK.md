
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
$ export FLASK_APP=project1
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

If you get the above output, press `Ctrl-c`, and if not follow the below process to modify ulimit:

Step 1:
    Check current soft limit
    $ ulimit -n

Step 2:
    Check current hard limit
    $ ulimit -Hn

Step 3:
    Add the below lines in /etc/security/limits.conf at the end:
    your_username hard nofile 16384
    your_username soft nofile 16384

Step 4:
    Set (or uncomment and set) DefaultLimitNOFILE=16384 in files:
    /etc/systemd/user.conf
    /etc/systemd/system.conf

Step 5:
    Add the line:
    ```
    session required pam_limits.so
    ```
    to files:
    ```
    /etc/pam.d/common-session
    /etc/pam.d/common-session-noninteractive
    ```

Step 6:
    Restart PC


-------------
Orchestration
-------------

```
$ foreman start -m posts_test=3,votes_test=3,accounts_test=1,caddy_lbt=1 --port 3000
```
