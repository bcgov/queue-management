#!/bin/sh

password_nonqtxn=cfmspmnopw333
client_secret=d2adf87c-1a1b-4b4c-831c-e352b4fc9654
clientid=cfms-procurement
userid_nonqtxn=cfms-postman-non-operator
realm=sbc

curl -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=password&client_id=${clientid}&username=${userid_nonqtxn}&password=${password_nonqtxn}&client_secret=${client_secret}" https://sso-dev.pathfinder.gov.bc.ca/auth/realms/${realm}/protocol/openid-connect/token?Content-Type=application/x-www-form-urlencoded | \
    python -c "import sys, json; print json.load(sys.stdin)['access_token']" > bearer

bearer=$(cat ./bearer)

echo Bearer token is $bearer

rm bearer

curl -H "Authorization:Bearer ${bearer}" http://localhost:5000/api/v1/csrs/me/

ab -t 5 -c 20 -H "Authorization:Bearer ${bearer}" http://localhost:5000/api/v1/csrs/me/
