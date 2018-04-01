const Immutable = require('immutable')

// getters are functions
module.exports = {
  eventFacets: state => state.eventData.facets.data || []
}