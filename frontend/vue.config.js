const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  transpileDependencies: ['vuetify'],

  configureWebpack: {

    devtool: 'source-map',
    // process: {env: {}},
    plugins: [
      // fix "process is not defined" error:
      // (do "npm install process" before running the build)
      new webpack.ProvidePlugin({
        process: 'process/browser'
      }),
      new webpack.ProvidePlugin({
        Buffer: ['buffer', 'Buffer']
      })
    ],
    resolve: {
      fallback: {
        crypto: require.resolve('crypto-browserify'),
        buffer: require.resolve('buffer'),
        util: require.resolve('util'),
        stream: require.resolve('stream-browserify')
      }
    }
  },
  runtimeCompiler: true

})
