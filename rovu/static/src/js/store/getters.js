const Immutable = require('immutable')

// getters are functions
module.exports = {
  eventFacets: state => {
    return state.eventData.facets.data || []
  },
  eventsData: state => {
    state.eventData.facets.data || []
    return state.eventData.events.data || []
  },
  searchFacetId: state => state.eventData.search.facetId,
  searchEventStart: state => state.eventData.search.startDate,
  searchEventEnd: state => state.eventData.search.endDate,
  mobileSearchDrawerOpen: state => state.ui.mobileSearchDrawer.open,
  fetchEventsPending: state => state.eventData.events.loading,
}