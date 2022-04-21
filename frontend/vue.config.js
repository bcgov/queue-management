var path = require('path')
module.exports = {
  configureWebpack: {
    devtool: 'source-map',
    resolve: {
      alias: {
        vue: path.resolve('./node_modules/vue'),
        $assets: path.resolve('./src/assets/')
      },
      fallback: {
        crypto: require.resolve('crypto-browserify'),
        buffer: require.resolve('buffer'),
        util: require.resolve('util'),
        stream: require.resolve('stream-browserify')
      }
    }
  },

  // publicPath: process.env.VUE_APP_PATH,
  runtimeCompiler: true,

  // Necessary for IE11 compat
  transpileDependencies: ['vuetify'],

}
