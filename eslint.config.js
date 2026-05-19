import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'

export default [
  // Base JS rules
  js.configs.recommended,

  // Vue 3 recommended rules — in v10 the vue3- prefix was dropped
  ...pluginVue.configs['flat/recommended'],

  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.es2022,
      },
      parserOptions: {
        ecmaVersion: 2022,
        sourceType: 'module',
      },
    },

    rules: {
      // Islands have single-word names by design (ThemeSwitcher, SearchBar)
      'vue/multi-word-component-names': 'off',

      // Allow defineProps without destructuring in <script setup>
      'vue/no-setup-props-destructure': 'off',
    },
  },

  {
    ignores: [
      'static_compiled/**',
      'static/**',
      'node_modules/**',
      'scripts/**',
    ],
  },
]
