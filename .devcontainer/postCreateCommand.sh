#!/bin/bash

# Copyright 2022 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

###############################################################################
# Functions
###############################################################################

COLOR_DEFAULT='\033[0m'
COLOR_FAILURE='\033[0;31m'

# Fix Git workspace for MAC
git config --global --add safe.directory /workspace
git config --global --add safe.directory /workspace/jobs/appointment_reminder/env/src/queue-api
git status

# Echo a string in red.
#
# Parameter: string
#
echo_failure () {
    echo -e "$COLOR_FAILURE$*$COLOR_DEFAULT"
}

# If a configuration file doesn't exist then create a default file.
#
# Parameters: source_file destination_file
#
copy_config () {
    SOURCE=$1
    DESTINATION=$2

    if [ ! -f $SOURCE ]; then
        echo_failure configuration source file $(pwd)/$SOURCE is missing
    else
        if [ -f $DESTINATION ]; then
            echo Using pre-existing file $(realpath $DESTINATION)
        else
            SOURCE=$(realpath $SOURCE)

            DIRECTORY=$(dirname $DESTINATION)
            if [ ! -d $DIRECTORY ]; then
                echo Creating directory $(pwd)/$DIRECTORY
                mkdir -p $DIRECTORY
            fi

            echo Copying $SOURCE to $(pwd)/$DESTINATION
            cp $SOURCE $DESTINATION
        fi
    fi
}

# Check that a configuration value is defined in a file. As this only does a
# grep for the key, it is likely to provide false positives for comments,
# substrings of other keys, or keys defined without values.
#
# Parameters: filename key_name
#
check_setting () {
    FILENAME=$1
    KEY_NAME=$2

    grep "$KEY_NAME" $FILENAME > /dev/null

    if [ $? -ne 0 ]; then
        echo_failure Missing configuration key $KEY_NAME in \
            $(realpath $FILENAME)
    fi
}

###############################################################################
# Dependency Installations
###############################################################################

# Log the output to make it easier to find when things go wrong.
LOGDIR=.devcontainer/logs
if [ ! -d $LOGDIR ]; then
    mkdir $LOGDIR
fi

# To save time do the installations in parallel.

(
    cd api
    rm -rf env
    python -m venv env
    source env/bin/activate
    python -m pip install --upgrade pip -q
    pip install wheel
    pip install -r requirements_dev.txt --progress-bar off

    # Install newman so that the postman tests can be run on the command line.
    echo Installing newman
    cd postman
    rm -rf node_modules
    npm install newman
) |& tee $LOGDIR/api.log &

# If NPM output is piped into a commmand, it does not display any indication of
# progress. Use "script" to make NPM think it is running on a TTY.
script -fq -c "(
    cd appointment-frontend
    rm -rf node_modules
    npm install
    $(npm bin)/cypress install
)" |& tee $LOGDIR/appointment-frontend.log &

(
    cd feedback-api
    rm -rf env
    python -m venv env
    source env/bin/activate
    python -m pip install --upgrade pip -q
    pip install wheel
    pip install -r requirements.txt --progress-bar off
    python3 setup.py install
) |& tee $LOGDIR/feedback-api.log &

script -fq -c "(
    cd frontend
    rm -rf node_modules
    npm install
)" |& tee $LOGDIR/frontend.log &

(
    cd notifications-api
    rm -rf env
    python -m venv env
    source env/bin/activate
    python -m pip install --upgrade pip -q
    pip install wheel
    pip install -r requirements.txt --progress-bar off
    python3 setup.py install
) |& tee $LOGDIR/notifications-api.log &

(
    cd jobs/appointment_reminder
    rm -rf env
    python -m venv env
    source env/bin/activate
    python -m pip install --upgrade pip -q
    pip install wheel
    pip install -r requirements.txt --progress-bar off
) |& tee $LOGDIR/appointment_reminder.log 

# Wait for all the above to complete.
wait

rm typescript

###############################################################################
# Database Bootstrapping and Setup
###############################################################################

(
    cd api
    source env/bin/activate
    python manage.py db upgrade

    # If there is nothing in the CSR table, we're probably starting with a
    # clean database and need to bootstrap it with default data.
    COUNT=$(PGPASSWORD=postgres psql -h queue-management_devcontainer_db_1 \
        -U postgres -c "SELECT COUNT(*) FROM csr;" -t)
    if [ "$COUNT" -eq 0 ]; then
        python manage.py bootstrap
        python manage.py adduser
    fi
)

###############################################################################
# Configuration Files Setup and Checking
###############################################################################

echo

copy_config .devcontainer/config/api/dotenv api/.env
check_setting api/.env JWT_OIDC_AUDIENCE
check_setting api/.env JWT_OIDC_WELL_KNOWN_CONFIG

copy_config .devcontainer/config/api/client_secrets/secrets.json \
    api/client_secrets/secrets.json

copy_config .devcontainer/config/frontend/public/config/configuration.json \
    frontend/public/config/configuration.json

# Need to copy configuration.json for appointments & keycloak-public.json
# Need to add keycloak.json to frontend/static/keycloak folder
# Need to add .env to notifications-api and feedback-api