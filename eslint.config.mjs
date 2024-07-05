// eslint.config.js

import globals from 'globals';

export default [
  {
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        myCustomGlobal: 'readonly',
      },
    },
    // ...other config
  },
];
