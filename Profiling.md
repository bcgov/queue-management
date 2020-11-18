Profiling

http://localhost:8080/appointments


Convert below into script.
- Get PID of gunicorn by name 
  - run on for loop ( can handle multiple, including sub process)

## Python Profiling


```bash

# Get PID of process
pgrep -f gunicorn


sudo py-spy record -o profile.svg --pid 37477


# use  lowest pid to  find parent
sudo py-spy record -o profile.svg --subprocesses --pid 43069
sudo py-spy record -o profile.svg --subprocesses --pid 37055

```


#### Postgres

Patroni - set
 changed `PATRONI_LOG_LEVEL` from `WARNING` to `INFO`
 added `PATRONI_LOG_DIR` set to `/var/log/postgresql/` - note folder already exists but was empty
```

```


## Observations

On `profile-withloadtesting.svg` - should run again with higher levels of load testing.

Preliminary Observations:
- 36% of time spent on validating tokens
- json is 11%, 2% for marshalling and 9% for encoding
- non-framework  controller code is around 11%, all of that is basically just orm requests




## References
https://docs.sqlalchemy.org/en/13/faq/performance.html

### Handover

After running tests, you'll see a report (example provided):

    All virtual users finished
    Summary report @ 12:02:42(-0800) 2020-11-09
    Scenarios launched:  619
    Scenarios completed: 618
    Requests completed:  3953
    Mean response/sec: 28.49
    Response time (msec):
        min: 0
        max: 30051.4
        median: 3412
        p95: 11993.4
        p99: 17865.3
    Scenario counts:
        CSR – Login, load data, idle: 200 (32.31%)
        CSR - Websockets: 206 (33.279%)
        CSR – Create and delete appointments: 213 (34.41%)
    Codes:
        0: 412
        200: 2690
        201: 425
        204: 425
        504: 1

Some notes:

Scenarios launched is 619, which means it simulated 619 CSRs load. We ensure that the maximum concurrent users never surpasses `maxVusers` (in .yaml).   So, there are never more than 200 users _at once_, but as those users complete their load-testing tasks they are replaced with more virtual users (419 more, to be exact).


The results are mostly under "Codes".   The `0: 412` line means 412 websocket connections were made.  We can also see that for all but 1 request, we got status codes in the 200s (success).

There was one 504 error.  In order to see errors, you must monitor the pods in OpenShift.  Artillery does not expose errors.

In this case, the error was related to greenlet.

```
        [2020-11-09 19:57:08,715] ERROR    (socketio.server) <kombu_manager.py>._listen: Connection error while reading from queue
    Traceback (most recent call last):
    File "/opt/app-root/lib/python3.6/site-packages/socketio/kombu_manager.py", line 118, in _listen
        message.ack()
    File "/opt/app-root/lib/python3.6/site-packages/kombu/message.py", line 126, in ack
        self.channel.basic_ack(self.delivery_tag, multiple=multiple)
    File "/opt/app-root/lib/python3.6/site-packages/amqp/channel.py", line 1394, in basic_ack
        spec.Basic.Ack, argsig, (delivery_tag, multiple),
    File "/opt/app-root/lib/python3.6/site-packages/amqp/abstract_channel.py", line 59, in send_method
        conn.frame_writer(1, self.channel_id, sig, args, content)
    File "/opt/app-root/lib/python3.6/site-packages/amqp/method_framing.py", line 189, in write_frame
        write(view[:offset])
    File "/opt/app-root/lib/python3.6/site-packages/amqp/transport.py", line 305, in write
        self._write(s)
    File "/opt/app-root/lib/python3.6/site-packages/eventlet/greenio/base.py", line 402, in sendall
        tail = self.send(data, flags)
    File "/opt/app-root/lib/python3.6/site-packages/eventlet/greenio/base.py", line 396, in send
        return self._send_loop(self.fd.send, data, flags)
    File "/opt/app-root/lib/python3.6/site-packages/eventlet/greenio/base.py", line 383, in _send_loop
        return send_method(data, *args)
    TimeoutError: [Errno 110] Connection timed out

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
    File "/opt/app-root/lib/python3.6/site-packages/socketio/kombu_manager.py", line 119, in _listen
        yield message.payload
    File "/opt/app-root/lib/python3.6/site-packages/kombu/simple.py", line 24, in __exit__
        self.close()
    File "/opt/app-root/lib/python3.6/site-packages/kombu/simple.py", line 92, in close
        self.consumer.cancel()
    File "/opt/app-root/lib/python3.6/site-packages/kombu/messaging.py", line 488, in cancel
        cancel(tag)
    File "/opt/app-root/lib/python3.6/site-packages/amqp/channel.py", line 1440, in basic_cancel
        wait=None if nowait else spec.Basic.CancelOk,
    File "/opt/app-root/lib/python3.6/site-packages/amqp/abstract_channel.py", line 59, in send_method
        conn.frame_writer(1, self.channel_id, sig, args, content)
    File "/opt/app-root/lib/python3.6/site-packages/amqp/method_framing.py", line 189, in write_frame
        write(view[:offset])
    File "/opt/app-root/lib/python3.6/site-packages/amqp/transport.py", line 305, in write
        self._write(s)
    File "/opt/app-root/lib/python3.6/site-packages/eventlet/greenio/base.py", line 402, in sendall
        tail = self.send(data, flags)
    File "/opt/app-root/lib/python3.6/site-packages/eventlet/greenio/base.py", line 396, in send
        return self._send_loop(self.fd.send, data, flags)
    File "/opt/app-root/lib/python3.6/site-packages/eventlet/greenio/base.py", line 383, in _send_loop
        return send_method(data, *args)
    BrokenPipeError: [Errno 32] Broken pipe
```

Running with 400 conurrent users caused many more errors:

    All virtual users finished
    Summary report @ 14:25:35(-0800) 2020-11-09
    Scenarios launched:  859
    Scenarios completed: 836
    Requests completed:  5263
    Mean response/sec: 32.75
    Response time (msec):
        min: 0
        max: 31556.1
        median: 6828.8
        p95: 22619.4
        p99: 30031
    Scenario counts:
        CSR – Login, load data, idle: 277 (32.247%)
        CSR - Websockets: 305 (35.506%)
        CSR – Create and delete appointments: 277 (32.247%)
    Codes:
        0: 610
        200: 3503
        201: 530
        204: 527
        504: 93
    Errors:
        ECONNRESET: 1

#### Report Example




#### Scrap


###### pgbench

```bash
# initialize?
pgbench -i -s 70 queue_management -U postgres


pgbench -c 4 -j 2 -T 600 -S queue_management -U postgres
output (on local)
    starting vacuum...end.
    transaction type: <builtin: select only>
    scaling factor: 70
    query mode: simple
    number of clients: 4
    number of threads: 2
    duration: 600 s
    number of transactions actually processed: 8862272
    latency average = 0.271 ms
    tps = 14770.399581 (including connections establishing)
    tps = 14770.461611 (excluding connections establishing)


```

##### Runs

First load testing error, 500s only occur after 50 seconds/506 requests.

Report @ 11:06:26(-0800) 2020-11-09
Elapsed time: 50 seconds
  Scenarios launched:  500
  Scenarios completed: 221
  Requests completed:  506
  Mean response/sec: 75.08
  Response time (msec):
    min: 0
    max: 30182.5
    median: 0.1
    p95: 30136.2
    p99: 30153.9
  Codes:
    0: 410
    200: 21
    504: 75

    ....

All virtual users finished
Summary report @ 11:09:04(-0800) 2020-11-09
  Scenarios launched:  3919
  Scenarios completed: 3133
  Requests completed:  13880
  Mean response/sec: 68.02
  Response time (msec):
    min: 0
    max: 51296.5
    median: 10877.4
    p95: 38124.1
    p99: 46053.6
  Scenario counts:
    CSR - Websockets: 1978 (50.472%)
    CSR – Login, load data, idle: 1941 (49.528%)
  Codes:
    0: 2864
    200: 3675
    503: 3970
    504: 3371
  Errors:
    Error: websocket error: 539
    timeout: 7
    ECONNRESET: 240

--

All virtual users finished
Summary report @ 11:57:53(-0800) 2020-11-09
  Scenarios launched:  202
  Scenarios completed: 202
  Requests completed:  2194
  Mean response/sec: 27.18
  Response time (msec):
    min: 0
    max: 21191.9
    median: 3544.9
    p95: 10306
    p99: 14659.4
  Scenario counts:
    CSR – Create and delete appointments.: 198 (98.02%)
    CSR – Login, load data, idle: 2 (0.99%)
    CSR - Websockets: 2 (0.99%)
  Codes:
    0: 4
    200: 1398
    201: 396
    204: 396


##### Errors / Logs


High load, creating/deleting records

    TypeError: Object of type 'set' is not JSON serializable
    [2020-11-09 19:53:19 +0000] [34] [ERROR] Error handling request /api/v1/appointments/
    Traceback (most recent call last):
    File "/opt/app-root/lib/python3.6/site-packages/gunicorn/workers/base_async.py", line 55, in handle
        self.handle_request(listener_name, req, client, addr)
    File "/opt/app-root/lib/python3.6/site-packages/gunicorn/workers/base_async.py", line 106, in handle_request
        respiter = self.wsgi(environ, resp.start_response)
    File "/opt/app-root/lib/python3.6/site-packages/flask/app.py", line 2464, in __call__
        return self.wsgi_app(environ, start_response)
    File "/opt/app-root/lib/python3.6/site-packages/flask_socketio/__init__.py", line 46, in __call__
        start_response)
    File "/opt/app-root/lib/python3.6/site-packages/engineio/middleware.py", line 74, in __call__
        return self.wsgi_app(environ, start_response)
    File "/opt/app-root/lib/python3.6/site-packages/flask/app.py", line 2450, in wsgi_app
        response = self.handle_exception(e)
    File "/opt/app-root/lib/python3.6/site-packages/flask_restx/api.py", line 638, in error_router
        return original_handler(f)
    File "/opt/app-root/lib/python3.6/site-packages/flask_cors/extension.py", line 165, in wrapped_function
        return cors_after_request(app.make_response(f(*args, **kwargs)))
    File "/opt/app-root/lib/python3.6/site-packages/flask/app.py", line 1867, in handle_exception
        reraise(exc_type, exc_value, tb)
    File "/opt/app-root/lib/python3.6/site-packages/flask/_compat.py", line 39, in reraise
        raise value
    File "/opt/app-root/lib/python3.6/site-packages/flask_restx/api.py", line 636, in error_router
        return self.handle_error(e)
    File "/opt/app-root/lib/python3.6/site-packages/flask/app.py", line 2447, in wsgi_app
        response = self.full_dispatch_request()
    File "/opt/app-root/lib/python3.6/site-packages/flask/app.py", line 1952, in full_dispatch_request
        rv = self.handle_user_exception(e)
    File "/opt/app-root/lib/python3.6/site-packages/flask_restx/api.py", line 638, in error_router
        return original_handler(f)
    File "/opt/app-root/lib/python3.6/site-packages/flask_cors/extension.py", line 165, in wrapped_function
        return cors_after_request(app.make_response(f(*args, **kwargs)))
    File "/opt/app-root/lib/python3.6/site-packages/flask/app.py", line 1821, in handle_user_exception
        reraise(exc_type, exc_value, tb)
    File "/opt/app-root/lib/python3.6/site-packages/flask/_compat.py", line 39, in reraise
        raise value
    File "/opt/app-root/lib/python3.6/site-packages/flask_restx/api.py", line 636, in error_router
        return self.handle_error(e)
    File "/opt/app-root/lib/python3.6/site-packages/flask/app.py", line 1950, in full_dispatch_request
        rv = self.dispatch_request()
    File "/opt/app-root/lib/python3.6/site-packages/flask/app.py", line 1936, in dispatch_request
        return self.view_functions[rule.endpoint](**req.view_args)
    File "/opt/app-root/lib/python3.6/site-packages/flask_restx/api.py", line 379, in wrapper
        return self.make_response(data, code, headers=headers)
    File "/opt/app-root/lib/python3.6/site-packages/flask_restx/api.py", line 402, in make_response
        resp = self.representations[mediatype](data, *args, **kwargs)
    File "/opt/app-root/lib/python3.6/site-packages/flask_restx/representations.py", line 25, in output_json
        dumped = dumps(data, **settings) + "\n"
    File "/opt/rh/rh-python36/root/usr/lib64/python3.6/json/__init__.py", line 238, in dumps
        **kw).encode(obj)
    File "/opt/rh/rh-python36/root/usr/lib64/python3.6/json/encoder.py", line 201, in encode
        chunks = list(chunks)
    File "/opt/rh/rh-python36/root/usr/lib64/python3.6/json/encoder.py", line 437, in _iterencode
        o = _default(o)
    File "/opt/rh/rh-python36/root/usr/lib64/python3.6/json/encoder.py", line 180, in default
        o.__class__.__name__)
    TypeError: Object of type 'set' is not JSON serializable