import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '1'))
threads = int(os.environ.get('GUNICORN_THREADS', '1'))

worker_class = 'eventlet'
worker_connections = 200
timeout = 60
keepalive = 20
