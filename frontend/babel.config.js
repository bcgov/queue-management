module.exports = function (api) {
  if (api.env('test')) {
    return {
      presets: [
        [
          '@babel/preset-env',
          {
            targets: {
              browsers: [
                'last 10 Chrome versions',
                'ie >= 11'
              ]
            },
            useBuiltIns: 'usage',
            corejs: 3
          }
        ]
      ]
    }
  }
  return {
    'presets': [
      [
        '@vue/app',
        {
          'useBuiltIns': 'entry'
        }
      ]
    ],
    'compact': true
  }
}
