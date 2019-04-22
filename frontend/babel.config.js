module.exports = function(api) {
  api.cache.using( () => process.env.NODE_ENV !== 'test')
  const isTest = api.env('test')
  if (isTest) {
    return {
      presets: [
        [
          '@babel/preset-env',
          {
            useBuiltIns: "usage",
            corejs: "3",
            targets: {
              ie: "11"
            }
          },
        ]
      ],
    }
  }
  return {
    presets: [
      '@vue/app',
      [
          '@babel/preset-env',
          {
            useBuiltIns: "usage",
            corejs: "3",
            targets: {
              ie: "11"
          }
        },
      ]
    ]
  }
}
