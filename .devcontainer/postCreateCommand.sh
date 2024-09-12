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

# Log the output to make it easier to find when things go wrong.

LOGDIR=".devcontainer/logs"
LOGFILE="$LOGDIR/error.log"

if [ ! -d $LOGDIR ]; then
    mkdir -p $LOGDIR
fi

touch $LOGFILE

# Redirect stderr to both the logfile and terminal using tee
exec 2> >(tee -a $LOGFILE >&2)

# Echo a string in red.
#
# Parameter: string
#
echo_failure () {
    echo -e "$COLOR_FAILURE$*$COLOR_DEFAULT" | tee -a $LOGFILE >&2
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


install_api_deps () {
    (
        cd api
        # Remove old virtual environment and create a new one
        rm -rf env || handle_error "Failed to remove old virtual environment."
        sudo python3 -m venv env || handle_error "Failed to create virtual environment."

        # Activate the virtual environment and install dependencies
        source env/bin/activate || handle_error "Failed to activate virtual environment."
        sudo chown -R $USER:$USER /workspace
        python -m pip install --upgrade pip -q || handle_error "Failed to upgrade pip."
        pip install -r requirements_dev.txt --progress-bar off || handle_error "Failed to install dependencies."
    )
}

# If NPM output is piped into a commmand, it does not display any indication of
# progress. Use "script" to make NPM think it is running on a TTY.
install_appointment_frontend_deps () {
    (
        cd appointment-frontend
        rm -rf node_modules
        npm install
        npx cypress install
    )
}

install_frontend_deps () {
    (
        cd frontend
        rm -rf node_modules
        npm install
    )
}

install_api_deps
install_appointment_frontend_deps
install_frontend_deps

###############################################################################
# Database Bootstrapping and Setup
###############################################################################

bootstrap_database () {
    (
        cd api
        source env/bin/activate
        python manage.py db upgrade
        pip install -r requirements.txt

        # If there is nothing in the CSR table, we're probably starting with a
        # clean database and need to bootstrap it with default data.
        python manage.py migrate
        read -p "Enter your IDIR to check if db is bootstrapped: " SEARCH_USER
        COUNT=$(PGPASSWORD=postgres psql -h queue-management_devcontainer_db_1 \
            -U postgres -c "SELECT COUNT(*) FROM csr WHERE username = '$SEARCH_USER';" -t)
        if [ "$COUNT" -eq 0 ]; then
            python manage.py bootstrap
            echo "$SEARCH_USER" | python manage.py adduser
        fi
    )
}

bootstrap_database

###############################################################################
# Configuration Files Setup and Checking
###############################################################################

echo

copy_config .devcontainer/config/api/dotenv api/.env
check_setting api/.env JWT_OIDC_AUDIENCE
check_setting api/.env JWT_OIDC_WELL_KNOWN_CONFIG

copy_config .devcontainer/config/api/client_secrets/secrets.json \
    api/client_secrets/secrets.json

copy_config .devcontainer/config/frontend/public/static/keycloak/keycloak.json \
    frontend/public/static/keycloak/keycloak.json

copy_config .devcontainer/config/frontend/public/config/configuration.json \
    frontend/public/config/configuration.json

copy_config .devcontainer/config/appointment-frontend/dotenv.local appointment-frontend/.env.local

copy_config .devcontainer/config/appointment-frontend/public/config/kc/keycloak-public.json \
    appointment-frontend/public/config/kc/keycloak-public.json

copy_config .devcontainer/config/appointment-frontend/public/config/configuration.json \
    appointment-frontend/public/config/configuration.json
