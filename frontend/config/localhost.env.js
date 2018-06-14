var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"localhost"',
  API_URL: '"http://localhost:8088/api/v1"',
  SOCKET_URL: '"http://localhost:8088"'
})
