let path = require('path')
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
    client: {
      overlay: {
        warnings: false,
        errors: true
      }
    },
    // Configure local API calls to hit OpenShift dev
    proxy: {
      '/api/v1': {
        target: 'https://test-theq-public.apps.silver.devops.gov.bc.ca',
        changeOrigin: true,
        secure: true,
        logLevel: 'debug'
      }
    },
    // Allow using the local proxy across other devices on LAN
    headers: { 'Access-Control-Allow-Origin': '*' }
  }
}
