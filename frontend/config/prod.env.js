const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"production"',
  API_URL: '"/api/v1"',
  SOCKET_URL: '""',
  KEYCLOAK_JSON_URL: '"/static/keycloak/keycloak.json"',
  REFRESH_TOKEN_SECONDS_LEFT: 1700
})
