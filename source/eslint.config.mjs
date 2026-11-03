import globals from 'globals';

export default [
  {ignores:['node_modules/**','dist/**','playwright-report/**','test-results/**']},
  {
    files:['assets/js/**/*.js','tools/**/*.js','tools/**/*.mjs','deploy/**/*.mjs','tests/**/*.mjs','*.mjs'],
    languageOptions:{ecmaVersion:'latest',sourceType:'module',globals:{...globals.browser,...globals.node}},
    rules:{'no-undef':'error','no-unused-vars':['error',{args:'none',caughtErrors:'none'}],'no-unreachable':'error','no-dupe-args':'error','no-dupe-keys':'error','valid-typeof':'error','constructor-super':'error'},
  },
];
