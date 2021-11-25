#!/bin/bash

# Do the setups for the container in parallel and then wait for the jobs.

(
    cd api
    python -m venv env
    source env/bin/activate
    python -m pip install --upgrade pip -q
    pip install -r requirements.txt --progress-bar off
    python manage.py db upgrade
) &

#(
#    cd appointment-frontend
#    npm ci --no-progress
#) &

#(
#    cd feedback-api
#    python -m venv env
#    source env/bin/activate
#    python -m pip install --upgrade pip -q
#    pip install -r requirements.txt --progress-bar off
#) &

(
    cd frontend
    npm ci #--no-progress
) &

#(
#    cd notifications-api
#    python -m venv env
#    source env/bin/activate
#    python -m pip install --upgrade pip -q
#    pip install -r requirements.txt --progress-bar off
#) &

wait
