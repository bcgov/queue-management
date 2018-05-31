var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"https://servicebc-cfms-test.pathfinder.gov.bc.ca/api/v1"'
})
