#!/bin/bash

KEYCLOAK_URI=http://localhost:8080/auth
REALM_JSON=/opt/keycloak/registry-realm.json
JBOSS_CLI=$KEYCLOAK_HOME/bin/jboss-cli.sh

echo -e "Starting Keycloak in background..."
$KEYCLOAK_HOME/bin/standalone.sh -b 0.0.0.0 -bmanagement 0.0.0.0 &
until `$JBOSS_CLI -c "ls /deployment" &> /dev/null`; do
    sleep 1
done

ACCESS_TOKEN=$(curl -s -X POST $KEYCLOAK_URI/realms/master/protocol/openid-connect/token \
        -d grant_type=password \
        -d client_id=admin-cli \
        -d username=admin -d password=admin | jq -r '.access_token')

# Remove existing realm
curl -s -S -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" $KEYCLOAK_URI/admin/realms/registry

echo "Importing realm..."
curl -s -S -H "Content-Type: application/json" -H "Authorization: Bearer $ACCESS_TOKEN" -d @$REALM_JSON $KEYCLOAK_URI/admin/realms

# HOW TO EXPORT A REALM
# The Keycloak admin UI does not (yet) support exporting realms.
# Assuming you changed something in Keycloak admin which you would like to keep,
# first attach to the running keycloak instance like this:
#
# docker exec -it keycloak /bin/bash
#
# Next, without killing keycloak (which would stop the container), we'll run a second instance on a different port.
# This is a round-about way to start the export process, but it works.
#
# cd /opt/keycloak
# keycloak-3.0.0.Final/bin/standalone.sh \
#    -Dkeycloak.migration.action=export \
#    -Dkeycloak.migration.provider=singleFile \
#    -Dkeycloak.migration.realmName=registry \
#    -Dkeycloak.migration.file=registry-realm.json \
#    -Djboss.socket.binding.port-offset=100

echo "Shutting down..."
$JBOSS_CLI -c ':shutdown' &> /dev/null
