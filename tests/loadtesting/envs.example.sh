#! /bin/sh
set -e
set -u

echo "Loading environment variables"

export MAX_VIRTUAL_USERS=200
export TARGET="http://localhost:5000"
export KEYCLOAK_BASE_URL="http://localhost:8085/auth"
export KEYCLOAK_REALM="servicebc-local"
export KEYCLOAK_CLIENT_ID="theq-queue-management-api"
export KEYCLOAK_CLIENT_SECRET="theq-local-dev-secret"
export KEYCLOAK_USERNAME="admin@idir"
export KEYCLOAK_PASSWORD="password"

# These IDs assume a local database seeded with `uv run python manage.py bootstrap`.
export LOADTEST_OFFICE_ID=1
export LOADTEST_CREATE_SERVICE_ID=11
export LOADTEST_UPDATE_SERVICE_ID=7
export LOADTEST_DRAFT_OFFICE_ID=2
export LOADTEST_DRAFT_SERVICE_ID=11
export LOADTEST_OFFICE_TIMEZONE="America/Vancouver"
export LOADTEST_DRAFT_OFFICE_TIMEZONE="America/Creston"
export LOADTEST_DRAFT_SLOT_WEEK_RANGE=300000

# Resolve a fresh access token after the Keycloak variables are exported.
export SERVICE_API_KEY="$(npm run get-keycloak-token --silent)"

echo "Target: $TARGET"
