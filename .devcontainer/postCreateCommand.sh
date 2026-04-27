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

set -euo pipefail

###############################################################################
# Logging
###############################################################################

LOGDIR=".devcontainer/logs"
LOGFILE="$LOGDIR/error.log"

if [ ! -d $LOGDIR ]; then
    mkdir -p $LOGDIR
fi

touch $LOGFILE

# Redirect stderr to both the logfile and terminal using tee
exec 2> >(tee -a $LOGFILE >&2)

echo_failure () {
    echo "$*" | tee -a "$LOGFILE" >&2
}

run_setup_local_config () {
    /bin/bash scripts/setup-local-config.sh
}

###############################################################################
# Dependency Installations
###############################################################################

install_api_deps () {
    (
        cd api
        export UV_PROJECT_ENVIRONMENT="$(pwd)/.venv"
        # Ensure the environment directory is owned by the current user
        if [ -d .venv ]; then
            sudo chown -R $(id -u):$(id -g) .venv
        fi
        python3 -m pip install --upgrade pip -q
        python3 -m pip install uv -q
        uv sync --group dev
    )
}

install_notifications_api_deps () {
    (
        cd notifications-api
        export UV_PROJECT_ENVIRONMENT="$(pwd)/.venv"
        # Ensure the environment directory is owned by the current user
        if [ -d .venv ]; then
            sudo chown -R $(id -u):$(id -g) .venv
        fi
        python3 -m pip install --upgrade pip -q
        python3 -m pip install uv -q
        uv sync --group dev
    )
}

# If NPM output is piped into a commmand, it does not display any indication of
# progress. Use "script" to make NPM think it is running on a TTY.
install_appointment_frontend_deps () {
    (
        cd appointment-frontend
        # Ensure the node_modules directory is owned by the current user
        if [ -d node_modules ]; then
            sudo chown -R $(id -u):$(id -g) node_modules
        fi
        npm install
        npx cypress install
    )
}

install_frontend_deps () {
    (
        cd frontend
        # Ensure the node_modules directory is owned by the current user
        if [ -d node_modules ]; then
            sudo chown -R $(id -u):$(id -g) node_modules
        fi
        npm install
    )
}

get_admin_csr_count () {
    local table_exists
    local count

    table_exists=$(PGPASSWORD=postgres psql -h localhost -U postgres -d postgres \
        -tA -c "SELECT to_regclass('public.csr') IS NOT NULL;")

    if [ "$table_exists" != "t" ]; then
        echo_failure "The csr table is missing after migrations; aborting bootstrap."
        return 1
    fi

    count=$(PGPASSWORD=postgres psql -h localhost -U postgres -d postgres \
        -tA -c "SELECT COUNT(*) FROM csr WHERE username = 'admin';")

    case "$count" in
        ''|*[!0-9]*)
            echo_failure "Unexpected csr count result: '$count'"
            return 1
            ;;
    esac

    echo "$count"
}

echo
run_setup_local_config

install_api_deps
install_notifications_api_deps
install_appointment_frontend_deps
install_frontend_deps

###############################################################################
# Database Bootstrapping and Setup
###############################################################################

bootstrap_database () {
    (
        cd api
        export UV_PROJECT_ENVIRONMENT="$(pwd)/.venv"
        local count

        # Bootstrap runs inside the devcontainer, so it needs
        # container-reachable Keycloak metadata even though the copied
        # local .env remains host-friendly for non-container use.
        export JWT_OIDC_WELL_KNOWN_CONFIG="http://keycloak:8080/auth/realms/servicebc-local/.well-known/openid-configuration"
        export JWT_OIDC_JWKS_URI="http://keycloak:8080/auth/realms/servicebc-local/protocol/openid-connect/certs"
        export JWT_OIDC_ISSUER="http://localhost:8085/auth/realms/servicebc-local"

        uv run python manage.py db upgrade

        # If the default bootstrap admin CSR is missing, we're probably
        # starting with a clean database and need to bootstrap it.
        uv run python manage.py migrate_db
        count=$(get_admin_csr_count)
        if [ "$count" -eq 0 ]; then
            uv run python manage.py bootstrap
        fi
    )
}

bootstrap_database

###############################################################################
# Configuration Files Setup
###############################################################################

echo
run_setup_local_config
