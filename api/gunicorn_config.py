import cProfile
import pstats
from io import StringIO
import logging
import os
import time
import dotenv

# Load all the environment variables from a .env file located in some directory above.
dotenv.load_dotenv(dotenv.find_dotenv())

PROFILE_LIMIT = int(os.environ.get("PROFILE_LIMIT", 20))
PROFILER = bool(int(os.environ.get("PROFILER", 0)))
workers = int(os.environ.get('GUNICORN_PROCESSES', '1'))
threads = int(os.environ.get('GUNICORN_THREADS', '1'))

worker_class = 'eventlet'
worker_connections = 500
timeout = 10
keepalive = 20

def profiler_enable(worker, req):
    worker.profile = cProfile.Profile()
    worker.profile.enable()
    worker.log.info("PROFILING %d: %s" % (worker.pid, req.uri))

def profiler_summary(worker, req):
    s = StringIO()
    worker.profile.disable()
    ps = pstats.Stats(worker.profile, stream=s).sort_stats('time', 'cumulative')
    ps.print_stats(PROFILE_LIMIT)

    logging.info("[%d] [%s] URI %s" % (worker.pid, req.method, req.uri))
    logging.info("[%d] %s" % (worker.pid, s.getvalue()))

def pre_request(worker, req):
    worker.start_time = time.time()
    if PROFILER is True:
        profiler_enable(worker, req)

def post_request(worker, req, *args):
    total_time = time.time() - worker.start_time
    logging.info("[%d] [%s] URI %s Load Time: %.3fs" % (worker.pid, req.method, req.uri, total_time))

    if PROFILER is True:
        profiler_summary(worker, req)
