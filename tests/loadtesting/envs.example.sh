#! /bin/sh
set -e
set -u

# Set environment variables below.
echo "Loading environment variables"

# We update the API key from keycloak 
export SERVICE_API_KEY=$(npm run get-keycloak-token --silent)
export MAX_VIRTUAL_USERS=200

# Note - Changing target may require additional keycloak changes, depending on setup.
# Currently this is configured to work with Keycloak/OIDC dev in OpenShifit DEV 
# and even localhost if your loaclhost uses OIDC dev.
# Load-testing logs into keycloak via `admin:admin`.
# Implementation details, including Keycloak URI, are in `function.js`
export TARGET="http://localhost:5000"
# export TARGET="https://dev-theq.pathfinder.gov.bc.ca"
export KEYCLOAK_USERNAME='admin'
export KEYCLOAK_PASSWORD='admin'

echo "Target: $TARGET\n"