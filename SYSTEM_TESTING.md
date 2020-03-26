
------------
Dependencies
------------

```
$ pip3 install locustio
```

---------------------------
Test / Locust file Template
---------------------------

```

```

------------
Load Testing
------------

$ locust -f locustfile.py --host=http://localhost:2015 --no-web -c 1000 -r 100

where:

+ `f` — Path to the file
+ `no-web` — Run the simulation without web interface
+ `c` — Number of users to simulate
+ `r` — Hatch rate (users spawned per second)


----
TODO
----

Consolidate stuff from:

+ https://steelkiwi.com/blog/load-testing-python-locust-testing-and-bokeh-vis/
+ https://microsoft.github.io/PartsUnlimitedMRP/pandp/200.1x-PandP-LocustTest.html
+ https://www.promptworks.com/blog/load-testing-with-locust
+ https://www.blazemeter.com/blog/jmeter-vs-locust-which-one-should-you-choose/
+ https://medium.com/better-programming/introduction-to-locust-an-open-source-load-testing-tool-in-python-2b2e89ea1ff
+ https://blog.realkinetic.com/load-testing-with-locust-part-1-174040afdf23?gi=7c21be14aa79
+ https://www.tothenew.com/blog/performing-heavy-load-testing-on-your-website-using-python-based-tool-locust/
