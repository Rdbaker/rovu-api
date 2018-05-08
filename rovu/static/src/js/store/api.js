const fetchFacets = () => {
  return fetch(new Request('/api/v1/events/categories/facets'))
}

const fetchEvents = (query) => {
  return fetch(new Request(`/api/v1/events?${query}`))
}

module.exports = {
  fetchFacets,
  fetchEvents,
}