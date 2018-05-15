const qs = require('qs')
const _ = require('lodash')

const api = require('./api')
const actionNames = require('./constants')

// actions are functions that cause side effects and can involve
// asynchronous operations.
module.exports = {
  fetchFacets: ({ commit }) => {
    commit('fetchFacetsPending')
    api.fetchFacets()
      .catch(commit('fetchFacetsFailed'))
      .then(res => res.json().then(data => commit('fetchFacetsSuccess', data)))
  },
  setSearchFacet: ({ commit }, payload) => {
    commit('setSearchFacet', payload)
  },
  setSearchStart: ({ commit }, payload) => {
    commit('setSearchStart', payload)
  },
  setSearchEnd: ({ commit }, payload) => {
    commit('setSearchEnd', payload)
  },
  fetchEvents: ({ commit, state }) => {
    commit('fetchEventsPending')
    api.fetchEvents(qs.stringify(_.pickBy({
      event_start_after: _.get(state, 'eventData.search.startDate'),
      event_end_before: _.get(state, 'eventData.search.endDate'),
      category_id: _.get(state, 'eventData.search.facetId'),
    }, _.identity)))
      .catch((err) => commit('fetchEventsFailed', err))
      .then(res => res.json().then(data => {
        commit('fetchEventsSuccess', data.events)
        commit('fetchFacetsSuccess', data.facets)
        commit('setMobileSearchDrawerOpen', false)
      }))
  },
  openMobileSearchDrawer: ({ commit }) => {
    commit('setMobileSearchDrawerOpen', true)
  },
  closeMobileSearchDrawer: ({ commit }) => {
    commit('setMobileSearchDrawerOpen', false)
  },
}