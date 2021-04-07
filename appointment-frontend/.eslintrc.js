module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/essential',
    '@vue/standard',
    '@vue/typescript'
  ],
  rules: {
	strict: 'off',
    'no-console': 'warn',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'sort-imports': 'error',
    'space-before-function-paren': 1,
	'prefer-const': 'warn',
	'dot-notation': 'off',
	'no-unused-vars': 'off',
	'quote-props': 'off',
	'prefer-rest-params': 'off',
	'dot-notation': 'off',
	'no-prototype-builtins': 'off',
	'import/export': 'off',
	'lines-between-class-members': 'warn',
	'prefer-const': 'off'
  },
  parserOptions: {
    parser: '@typescript-eslint/parser'
  }
}
