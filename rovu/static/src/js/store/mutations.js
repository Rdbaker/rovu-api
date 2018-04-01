const Immutable = require('immutable')

const actionNames = require('./constants')

// mutations are operations that actually mutates the state.
// each mutation handler gets the entire state tree as the
// first argument, followed by additional payload arguments.
// mutations must be synchronous and can be recorded by plugins
// for debugging purposes.
module.exports = {
  fetchFacetsSuccess (state, facets) {
    state.eventData.facets.data = facets
    state.eventData.facets.loading = false
  },
  fetchFacetsPending (state) {
    state.eventData.facets.loading = true
  },
  fetchFacetsFailed (state) {
    state.eventData.facets.loading = false
  },
}