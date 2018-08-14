var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"production"',
  API_URL: '"/api/v1"',
  SOCKET_URL: '""',
  KEYCLOAK_JSON_URL: '"/static/keycloak.json"'
})
