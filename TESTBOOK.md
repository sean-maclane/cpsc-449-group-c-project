
### NOTE: Navigate to the PROJECT_ROOT directory and setup environment variables before testing

------------------
Functional Testing
------------------

Standard `pytest` run:

```
$ pytest
```

Redirect the output of `pytest` to `error.log` file:

```
$ pytest > error.log
```

Enable traceback for one line per failure:

```
$ pytest --tb=line
```


------------
Load Testing
------------

$ locust -f locustfile.py --host=http://localhost:2015 --no-web -c 100 -r 10

where:

+ `f` — Path to the file
+ `no-web` — Run the simulation without web interface
+ `c` — Number of users to simulate
+ `r` — Hatch rate (users spawned per second)
