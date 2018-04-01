const Vue = require('vue')
const Vuex = require('vuex')

Vue.use(Vuex)

// A Vuex instance is created by combining the state, mutations, actions,
// and getters.
module.exports = new Vuex.Store({
  state: require('./state'),
  getters: require('./getters'),
  actions: require('./actions'),
  mutations: require('./mutations'),
})