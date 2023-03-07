const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"localhost"',
  API_URL: '"http://localhost:5000/api/v1"',
  SOCKET_URL: '"http://localhost:5000"',
  KEYCLOAK_JSON_URL: '"http://localhost:8080/static/keycloak.json"',
  REFRESH_TOKEN_SECONDS_LEFT: 180
})
