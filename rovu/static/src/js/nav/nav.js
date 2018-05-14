import { mapActions, mapGetters } from 'vuex';
import FontAwesomeIcon from '@fortawesome/vue-fontawesome';
import { Datetime } from 'vue-datetime';
import { merge } from 'lodash';

const $ = require('jquery');

export default {
  name: 'rovu-nav',

  created: function() {
    this.$store.dispatch('fetchFacets')
    this.markers = []
  },

  data: function() {
    return {
      searchEventStartDate: this.$store.getters.searchEventStart,
      searchEventEndDate: this.$store.getters.searchEventEnd,
    }
  },

  watch: {
    searchEventStartDate: function(val) {
      this.setSearchStart(val);
    },
    searchEventEndDate: function(val) {
      this.setSearchEnd(val);
    },
  },

  components: {
    FontAwesomeIcon,
    Datetime,
  },

  computed: merge(
    {
      events: function() {
        this.markEvents(this.eventsData)
        return this.eventsData
      },
    },
    mapGetters([
      'eventFacets',
      'eventsData',
      'searchFacetId',
      'searchEventStart',
      'fetchEventsPending',
      'searchEventEnd',
    ])
  ),

  mounted: function() {
    $('.ui.dropdown').dropdown();
    this.markers = [];
  },

  methods: merge(
    mapActions(['openMobileSearchDrawer', 'fetchEvents', 'setSearchStart', 'setSearchEnd']),
    {
      changeCategory: function(evt) {
        let elt = $(evt.currentTarget);
        if(elt.data('id') === this.searchFacetId) {
          this.$store.dispatch('setSearchFacet', null)
        } else {
          this.$store.dispatch('setSearchFacet', elt.data('id'))
        }
      },

      clearEvents: function() {
        for(var i=0; i<this.markers.length; i++) {
          this.markers[i].setMap(null);
        }
      },

      markEvents: function(events) {
        this.clearEvents();
        for(var i=0; i<events.length; i++) {
          this.markEvent(events[i]);
        }
      },

      markEvent: function(ev) {
        var marker = new google.maps.Marker({
          position: {lat: Number(ev.venue.latitude), lng: Number(ev.venue.longitude)},
          map: map,
          title: ev.name
        });
        var start_date = new Date(ev.start_datetime);
        var end_date = new Date(ev.end_datetime);
        var addr = (!!ev.venue.address && !!ev.venue.address.address_1) ? ev.venue.address.address_1 : "Address Unknown";
        var windowContent = ('<div class="event-content ui card">' +
            '<div class="event-title content"><div class="header">' + ev.name + '</div></div>' +
            '<div class="ui sub header"><div class="event-venue">' + ev.venue.name + '</div></div>' +
            '<div class="event-addr">' + addr + '</div>' +
            '<div class="event-date">' + start_date.toDateString() + '</div>' +
            '<div class="event-start-time">From: ' + start_date.toLocaleTimeString() + '</div>' +
            '<div class="event-end-time">To: ' + end_date.toLocaleTimeString() + '</div>' +
            '</div>'
        );
        var infowindow = new google.maps.InfoWindow({
          content: windowContent
        });
        marker.addListener('click', function() {
          //mixpanel.track('marker.click');
          infowindow.open(map, marker);
        });
        this.markers.push(marker);
      }

    },
  )
};
