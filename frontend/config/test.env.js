var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"https://test-theq.pathfinder.gov.bc.ca/api/v1"',
  SOCKET_URL: '"https://test-theq.pathfinder.gov.bc.ca"',
  KEYCLOAK_JSON_URL: '"https://test-theq.pathfinder.gov.bc.ca/static/keycloak-test.json"'
})
