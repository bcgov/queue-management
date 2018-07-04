var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"https://servicebc-cfms-dev.pathfinder.gov.bc.ca/api/v1"',
  SOCKET_URL: '"https://servicebc-cfms-dev.pathfinder.gov.bc.ca"',
  KEYCLOAK_JSON_URL: '"https://servicebc-cfms-dev.pathfinder.gov.bc.ca/static/keycloak-dev.json"'
})
