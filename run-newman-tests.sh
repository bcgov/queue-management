#!/bin/sh

./node_modules/newman/bin/newman.js run ./api/postman/postman_tests.json \
  -e ./api/postman/postman_env.json \
  --global-var password=cfmspmopw333 \
  --global-var password_nonqtxn=cfmspmnopw333 \
  --global-var client_secret=d2adf87c-1a1b-4b4c-831c-e352b4fc9654 \
  --global-var url=http://localhost:5000/api/v1/ \
  --global-var auth_url=https://sso-dev.pathfinder.gov.bc.ca \
  --global-var clientid=cfms-procurement \
  --global-var realm=sbc

