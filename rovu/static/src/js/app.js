global.jQuery = require('jquery');
global.$ = jQuery;

require('semantic-ui/dist/semantic');
const Vue = require('vue');

const App = require('./app.vue');

var app = new Vue({
  el: '#rovu-app',
  template: '<app></app>',
  render: (h) => h(App)
});
