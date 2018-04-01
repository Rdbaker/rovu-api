const Immutable = require('immutable')

const Address = Immutable.Record({
  address_1: null,
  address_2: null,
  city: null,
  country: null,
  latitude: null,
  longitude: null,
  localized_address_display: null,
  localized_area_display: null,
  localized_multi_line_address_display: Immutable.List(),
  postal_code: null,
  region: null,
})

const Venue = Immutable.Record({
  id: null,
  latitude: null,
  longitude: null,
  resource_url: null,
  address: new Address(),
})

const Event = Immutable.Record({
  id: null,
  name: null,
  end_datetime: null,
  start_datetime: null,
  category_id: null,
  raw_data: Immutable.Map(),
  venue: new Venue(),
})


module.exports = {
  Event
}