#!/bin/bash

###############################################################################
# Functions
###############################################################################

COLOR_DEFAULT='\033[0m'
COLOR_FAILURE='\033[0;31m'

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
        echo_failure configuration source file `pwd`/$SOURCE is missing
    else
        if [ -f $DESTINATION ]; then
            echo Using pre-existing file `realpath $DESTINATION`
        else
            SOURCE=`realpath $SOURCE`

            DIRECTORY=`dirname $DESTINATION`
            if [ ! -d $DIRECTORY ]; then
                echo Creating directory `pwd`/$DIRECTORY
                mkdir -p $DIRECTORY
            fi

            echo Copying $SOURCE to `pwd`/$DESTINATION
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
        echo_failure Missing configuration key $KEY_NAME in `realpath $FILENAME`
    fi
}

###############################################################################
# Setup
###############################################################################

# To save time do the pip and npm installs in parallel.

(
    cd api
    python -m venv env
    source env/bin/activate
    python -m pip install --upgrade pip -q
    pip install -r requirements.txt --progress-bar off
    python manage.py db upgrade

    # If there is nothing in the CSR table, we're probably starting with a
    # clean database and need to bootstrap it with default data.
    COUNT=`PGPASSWORD=postgres psql -h queue-management_devcontainer_db_1 \
        -U postgres -c "SELECT COUNT(*) FROM csr;" -t`
    if [ "$COUNT" -eq 0 ]; then
        env/bin/python manage.py bootstrap
    fi
) &

(
    cd appointment-frontend
    npm install
) &

#(
#    cd feedback-api
#    python -m venv env
#    source env/bin/activate
#    python -m pip install --upgrade pip -q
#    pip install -r requirements.txt --progress-bar off
#) &

(
    cd frontend
    npm install
) &

#(
#    cd notifications-api
#    python -m venv env
#    source env/bin/activate
#    python -m pip install --upgrade pip -q
#    pip install -r requirements.txt --progress-bar off
#) &

# Wait for the above to complete, and then do the filesystem setup. If anything
# fails we won't have to hunt for error messages.
wait

echo

copy_config .devcontainer/config/api/dotenv api/.env
check_setting api/.env JWT_OIDC_AUDIENCE
check_setting api/.env JWT_OIDC_WELL_KNOWN_CONFIG

copy_config .devcontainer/config/api/client_secrets/secrets.json \
    api/client_secrets/secrets.json

copy_config .devcontainer/config/frontend/public/config/configuration.json \
    frontend/public/config/configuration.json
