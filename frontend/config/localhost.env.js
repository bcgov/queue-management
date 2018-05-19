var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"localhost"',
  API_URL: '"http://localhost:8000/"'
})
