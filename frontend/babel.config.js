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
        '@babel/preset-env',
        {
          modules: false,
          targets: {
            browsers: ['> 1%', 'last 2 versions', 'not ie <= 10', 'IE 11']
          },
          useBuiltIns: 'usage',
          corejs: 3
        }
      ],
      [
        '@vue/cli-plugin-babel/preset',
        {
          'useBuiltIns': 'entry'
        }
      ]
    ],
    'compact': true
  };
}
