
### NOTE: Navigate to the PROJECT_ROOT directory and follow the setup instructions in README.md before testing. You will need to be in the virtual env and have run the given pip command.

-------------------------
API Specification Testing
-------------------------
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
In these tests, the dots indicate failure, F's indicade the API was not followed, and E's indicate a critical error.

------------
Load Testing
------------
Before load testing, open a separate terminal and follow the instructions in the runbook for starting a server. The load test will run until you press ctr+c.

```
$ locust -f locustfile.py --host=http://localhost:2015 --no-web -c 100 -r 10
```
where:

+ `f` — Path to the file
+ `no-web` — Run the simulation without web interface
+ `c` — Number of users to simulate
+ `r` — Hatch rate (users spawned per second)
