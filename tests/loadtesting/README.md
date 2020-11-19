# Load testing

- [Load testing](#load-testing)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Configuration](#configuration)
    - [Running Load Tests](#running-load-tests)
    - [Python Profiling](#python-profiling)
      - [Python Profiling on OpenShift](#python-profiling-on-openshift)
    - [Example Load Testing Report](#example-load-testing-report)
      - [Understanding a Load Testing Report](#understanding-a-load-testing-report)
  - [Report + Recommendations](#report--recommendations)
  - [Resources](#resources)
  - [FAQ / Troubleshooting](#faq--troubleshooting)
    - [Verify IDs are correct](#verify-ids-are-correct)
    - [Verify the "admin" user is assigned to correct office](#verify-the-admin-user-is-assigned-to-correct-office)
    - [I get errors when testing locally, but not when testing OpenShift dev](#i-get-errors-when-testing-locally-but-not-when-testing-openshift-dev)

## Installation

```bash
# Make sure to be in `tests/loadtesting` folder
cd tests/loadtesting

npm install

# Make bash scripts executable
chmod +x profile-python.sh
cp envs.example.sh envs.sh
chmod +x envs.sh

# py-spy is only necessary if are profiling python (`npm run python:*`)
# if you are JUST doing load testing (`npm run tests:*`), you can skip this.
pip install py-spy
```

## Usage

We have created a number of npm scripts in `package.json` that expose the functionality we worked on.  For example, `npm run tests:all` runs all loadtesting - websocket and HTTP.  There is also `tests:http` and `tests:socket`.


Quick reference:

```bash
# just runs load testing - no python profiling
npm run tests:all 

# run both load testing and python profiling:
npm run python:profile # in one terminal, start profiling
npm run tests:all # in separate terminal, run load tests
# after load testing is complete, press CTR+C in the python:profile terminal
```

More details can be found [in python profiling](#python-profiling)


### Configuration

Configuration of varables is done in `envs.sh`.  The main variables that will be used are

* `MAX_VIRTUAL_USERS` - determines the maximum amount of concurrent virtual users that are accessing the system at once
* `TARGET` - the endpoint being load tested.  This is configured to use the dev OIDC keycloak, so it can freely be changed between localhost and OpenShift dev.


### Running Load Tests

To run all load tests:

  npm run tests:all


You can see a [Example Load Testing Report](#example-load-testing-report) below, where we also discuss how to read and understand a load testing report.

### Python Profiling

```bash
# Main profile command, generates flame graph report, useful for analyzing performance
npm run python:profile

# Creates interactive terminal UI similar to "top", useful for local development.
npm run python:top
```

Python profiling allows us to get an in-depth look at where the Python API process is spending it's time. We have written some scripts that will automatically find the running gunicorn process and profile it, including subprocesses, and then create a flamegraph report.

All Python commands must be run on the same machine that already has the API running.  Additionally, they cannot be run in OpenShift itself due to security constraints [(see more)](#python-profiling-on-openshift)

These commands must be run on the same machine that already has the API running. It will ask for `sudo` password. It will scan for the parent gunicorn process by name and profile it.  Let this command run for the durattion of the profiling.  Typically, you start profiling, then run load testing, then exit profiling.  

**Why sudo?** *The profiler we use, `pyspy` can profile already running Python processes.  This is great for profiling  real world performance, but sudo is required in order to spy on another process. This is Linux security to stop a non-sudo process from inspecting/modifying other processes which should not be allowed.*

In the same terminal that you started `npm run python:profile`, press "CTRL+C" to exit profiling.  Only press it once.  It will then write the report as a svg file.  (If you press it twice quickly you can cancel out of it creating the report.)

So, to put the whole process together, typically to combine profiling with load testing, you would...

  1. Start the API like normal
  2. In a new terminal, run `npm run python:profile`
  3. In a new terminal, start loadtesting with `npm run tests:all`
  4. After #3 is complete, you can then end profling (select terminal for #2 and press CTRL+C)

This command outputs a `profile-12345.svg` file, with `12345` being the pid of the parent python process running gunicorn. The file is a [flamegraph](http://www.brendangregg.com/flamegraphs.html), an interactive graph that shows what processes took the most time.

We have included an example report, called `profile-demo-withloadtesting.svg`

#### Python Profiling on OpenShift

Summary - we cannot run this profiling on OpenShift due to BCGov specific security configurations.

In order to profile another process on OpenShift, we need to make the below change and add `SYS_PTRACE`. 

```yaml
securityContext:
  capabilities:
    add:
    - SYS_PTRACE
```

Unfortunately, the OpenShift 4 environment does not allow us to do this.  This is likely by design security options that have been enabled by the BC DevOps platform.  We could ask for an exception and see if they're willing.  Below is the error we get: `pods "queue-management-api-21-fc82h" is forbidden: unable to validate against any security context constraint: [capabilities.add: Invalid value: "SYS_PTRACE": capability may not be added]`

Even without OpenShift, this Python profiling is still valuable to run on locally.  While a developer's machine won't be as powerful as OpenShift, the underlying relationships between what takes time on Python will hold the same.   A developer could thus profile locally to identify and fix performance issues.  Put simply, even if their local  laptop is 20% weaker across the board, profiling will still let the developer find what's slow and fix it.


* https://github.com/benfred/py-spy#how-do-i-run-py-spy-in-docker
* https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#set-capabilities-for-a-container
* https://docs.openshift.com/container-platform/4.4/authentication/managing-security-context-constraints.html

### Example Load Testing Report

These are the results from running `npm run tests:all`

After running load tests, you'll see a report (example provided):

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

#### Understanding a Load Testing Report

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




## Report + Recommendations

* Load balancing on OpenShift pods doesn't seem to be working.
* Auth taking up 42.25% of all requests. Only ~12% of CPU spent on business logic.
* Send emails on separate pod

**Load Balancing not working** - it appears that load balancing between API pods is not working. Generally speaking (depending on load balancing config), when a new request comes in it should be distributed equally between all available pods.  This is not happening.  Instead, even though we have 2 API pods, all of the traffic is going to 1 pod.  This is a huge problem, as it means none of the horizontal scaling on OpenShift is working. There may be some technical hurdles, for example, there have been discussions before that perhaps load balancing would split the websocket sessions. 

**Recommendation Enable load balancing so that load is distributed equally among pods:** i.e. `roundrobin` [load balancing strategy - OpenShift docs link](https://docs.openshift.com/container-platform/3.5/architecture/core_concepts/routes.html#load-balancing).  

**Authentication taking up 42.25% of CPU on every request** - If we look at the flamegraph, for example, `profile-demo-withloadtesting.svg`, we can see that 36.75% of the CPU was spent on just parsing the OIDC token from Keycloak, and another 5.5% was spent in our `auth_util`.  Only 12% was for actual busienss logic. Another ~10% for JSON encoding, and the remaining ~35% for threading, eventlet, and gunicorn. 

**Recommendation: Refactor the `has_any_role`** function in `auth_util.py`, as it is in the hot path for basically every single request. Profile changes before and after to measure impact. While it's only 5% of CPU, it's 5% of CPU for _every request_, so any improvements here will benefit across the board.

**Recommendation: Investigate if there are gains to be made with Keycloak OIDC token parsing.**  We are currently using the [`flask_oidc` third party package.](https://flask-oidc.readthedocs.io/en/latest/).  If there are any gains to be made here, such as a new package, or writing it in house, they are worth looking into.  OIDC parsing takes 42% of every request, and is much higher impact than the `has_any_role` recommendation above.  One possibility would be to re-rewrite token parsing in another language faster than Python (e.g. C++ or Rust), and have Python call it via a foreign function interface.  The [Python CFFI](https://cffi.readthedocs.io/en/latest/overview.html) does exactly this.  One of Python's main strengths is it's fantastic foreign function interface, so that when a performance critical hot path is detected it can be re-written in another faster language.  This comes with operational overhead but is worth investigating.

**Recommendation: Send emails in a separate pod.** Sending emails is one of the most CPU intensive tasks that the API pod is responsible for.  When a pod has to bulk send emails (e.g. after creating a blackout), this can result in CPU spikes which cause other requests to timeout. We recommend spinning up a queue and a separate pod responsible for sending emails.  Instead of the main API pod sending emails, it would instead add a record to the queue indicating the email hadn't been sent.  The new email-pod would be programmed to always listen to the pod, and when emails come in it would send them and then update their status in the queue to sent.  Another benefit of this approach is it's more resiliant.  If a pod crashes when halfway through sending emails, the queue will still have the correct list of what needs to be sent.  In the current system if a pod crashes while sending emails, those emails are lost. Relatedly, having load-balancing working should ameliorate this issue of CPU load from emails.  So, we recommend you investigate load balancing first as it may improve it enough to not be an issue.

[OpenShift 4 also has specific patterns to deal with this, called Jobs.](https://docs.openshift.com/container-platform/4.1/nodes/jobs/nodes-nodes-jobs.html)  A queue would still be necessary, but then one could configure an "email job" to only spawn when there are emails to send.  This would reduce overall resources spent and increase resiliancy if things go down.

## Resources

* PySpy https://github.com/benfred/py-spy


## FAQ / Troubleshooting

### Verify IDs are correct

The first thing to check when trouble shooting is that the IDs in `csr-test-all.yaml` are correct.  For example, `service_id` and `office_id` we have hardcoded to 7 and 1 respectively.

### Verify the "admin" user is assigned to correct office

The admin user must be assigned to the same office that the tests try to use.

For example, if you set `office_id` to 1, then admin must be assigned to Test Office (assuming 1 = Test Office).


### I get errors when testing locally, but not when testing OpenShift dev

This is normal.  You run into performance limits quicker on a weaker local machine.

OpenShift dev can support 200 concurrent users, but my laptop can support far less than that.