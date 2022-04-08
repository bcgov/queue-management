module.exports = {
  'presets': [
    [
      '@vue/cli-plugin-babel/preset',
      {
        'useBuiltIns': 'entry',
        'targets': {
          'ie': '11'
        }
      }
    ]
  ],
  'compact': true
}
