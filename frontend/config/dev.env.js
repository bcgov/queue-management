var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
<<<<<<< HEAD
  API_URL: '"https://servicebc-cfms-api-dev.pathfinder.gov.bc.ca/api/v1"',
  SOCKET_URL: '"https://servicebc-cfms-api-dev.pathfinder.gov.bc.ca"'
=======
  API_URL: '"https://servicebc-cfms-api-dev.pathfinder.gov.bc.ca/api/v1"'
>>>>>>> upstream/proof-of-concept
})
