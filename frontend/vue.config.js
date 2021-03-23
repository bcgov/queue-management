var path = require('path')
module.exports = {
  configureWebpack: {
    devtool: process.env.NODE_ENV === 'production' ? false : 'source-map',
    resolve: {
      alias: {
        vue: path.resolve('./node_modules/vue'),
        $assets: path.resolve('./src/assets/')
      }
    }
  },
  // publicPath: process.env.VUE_APP_PATH,
  runtimeCompiler: true,

  // Necessary for IE11 compat
  transpileDependencies: ['vuetify'],

}
