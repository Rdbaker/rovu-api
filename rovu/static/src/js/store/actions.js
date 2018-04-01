const api = require('./api')
const actionNames = require('./constants')

// actions are functions that cause side effects and can involve
// asynchronous operations.
module.exports = {
  fetchFacets: ({ commit }) => {
    commit('fetchFacetsPending')
    api.fetchFacets()
      .catch(commit('fetchFacetsFailed'))
      .then(res => {
        res.json().then(data => commit('fetchFacetsSuccess', data))
      })
  },
  fetchFacetsFailed: ({ commit }) => {
  },
  increment: ({ commit }) => commit(actionNames.INCREMENT),
  decrement: ({ commit }) => commit(actionNames.DECREMENT),
  incrementIfOdd ({ commit, state }) {
    if ((state.count + 1) % 2 === 0) {
      commit(actionNames.INCREMENT)
    }
  },
  incrementDecrement: ({ commit }) => {
    commit(actionNames.INCREMENT)
    commit(actionNames.DECREMENT)
  },
  incrementAsync ({ commit }) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commit(actionNames.INCREMENT)
        resolve()
      }, 1000)
    })
  }
}