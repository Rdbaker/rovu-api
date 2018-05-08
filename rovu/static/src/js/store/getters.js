const Immutable = require('immutable')

// getters are functions
module.exports = {
  eventFacets: state => state.eventData.facets.data || [],
  eventList: state => state.eventData.events.data || [],
  searchFacetId: state => state.eventData.search.facetId,
  searchEventStart: state => state.eventData.search.startDate,
  searchEventEnd: state => state.eventData.search.endDate,
  mobileSearchDrawerOpen: state => state.ui.mobileSearchDrawer.open,
}