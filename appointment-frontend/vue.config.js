var path = require('path')
module.exports = {
  configureWebpack: {
    devtool: 'source-map',
    resolve: {
      alias: {
        'vue': path.resolve('./node_modules/vue'),
        '$assets': path.resolve('./src/assets/')
      }
    }
  },
  // publicPath: process.env.VUE_APP_PATH,
  transpileDependencies: ['vuetify', 'vuex-persist'],
  devServer: {
    overlay: {
      warnings: true,
      errors: true
    },
    // Configure local API calls to hit OpenShift dev
    proxy: {
      '/api/v1': {
        target: 'https://dev-theq.pathfinder.gov.bc.ca',
        changeOrigin: true,
        logLevel: 'debug'
      }
    }
  }
}
