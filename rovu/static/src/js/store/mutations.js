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
  setSearchFacet (state, facetId) {
    state.eventData.search.facetId = facetId
  },
  setSearchStart (state, startDate) {
    state.eventData.search.startDate = startDate
  },
  setSearchEnd (state, endDate) {
    state.eventData.search.endDate = endDate
  },
  fetchEventsPending (state) {
    state.eventData.events.loading = true
    state.eventData.facets.loading = true
  },
  fetchEventsFailed (state) {
    state.eventData.events.loading = false
    state.eventData.facets.loading = false
  },
  fetchEventsSuccess (state, events) {
    state.eventData.events.data = events
    state.eventData.events.loading = false
  },
  setMobileSearchDrawerOpen (state, isOpen) {
    state.ui.mobileSearchDrawer.open = isOpen
  },
}