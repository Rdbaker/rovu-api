const fetchFacets = () => {
  return fetch(new Request('/api/v1/events/categories/facets'))
}


module.exports = {
  fetchFacets,
}