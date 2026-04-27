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

set -u

COLOR_DEFAULT='\033[0m'
COLOR_FAILURE='\033[0;31m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo_failure () {
    echo -e "$COLOR_FAILURE$*$COLOR_DEFAULT" >&2
}

copy_config () {
    SOURCE="$1"
    DESTINATION="$2"

    if [ ! -f "$SOURCE" ]; then
        echo_failure "Configuration source file $SOURCE is missing"
        return 1
    fi

    if [ -f "$DESTINATION" ]; then
        echo "Using pre-existing file $DESTINATION"
        return 0
    fi

    DIRECTORY="$(dirname "$DESTINATION")"
    if [ ! -d "$DIRECTORY" ]; then
        echo "Creating directory $DIRECTORY"
        mkdir -p "$DIRECTORY"
    fi

    echo "Copying $SOURCE to $DESTINATION"
    cp "$SOURCE" "$DESTINATION"
}

check_setting () {
    FILENAME="$1"
    KEY_NAME="$2"

    if ! grep "$KEY_NAME" "$FILENAME" > /dev/null; then
        echo_failure "Missing configuration key $KEY_NAME in $FILENAME"
        return 1
    fi
}

main () {
    cd "$REPO_ROOT" || exit 1

    copy_config "$REPO_ROOT/.devcontainer/config/api/dotenv" \
        "$REPO_ROOT/api/.env"
    check_setting "$REPO_ROOT/api/.env" JWT_OIDC_AUDIENCE
    check_setting "$REPO_ROOT/api/.env" JWT_OIDC_WELL_KNOWN_CONFIG

    copy_config "$REPO_ROOT/.devcontainer/config/api/client_secrets/secrets.json" \
        "$REPO_ROOT/api/client_secrets/secrets.json"

    copy_config "$REPO_ROOT/.devcontainer/config/frontend/public/static/keycloak/keycloak.json" \
        "$REPO_ROOT/frontend/public/static/keycloak/keycloak.json"

    copy_config "$REPO_ROOT/.devcontainer/config/frontend/public/config/configuration.json" \
        "$REPO_ROOT/frontend/public/config/configuration.json"

    copy_config "$REPO_ROOT/.devcontainer/config/appointment-frontend/dotenv.local" \
        "$REPO_ROOT/appointment-frontend/.env.local"

    copy_config "$REPO_ROOT/.devcontainer/config/appointment-frontend/public/config/kc/keycloak-public.json" \
        "$REPO_ROOT/appointment-frontend/public/config/kc/keycloak-public.json"

    copy_config "$REPO_ROOT/.devcontainer/config/appointment-frontend/public/config/configuration.json" \
        "$REPO_ROOT/appointment-frontend/public/config/configuration.json"
}

main "$@"
