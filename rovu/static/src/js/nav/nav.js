import { mapActions, mapGetters } from 'vuex';
import FontAwesomeIcon from '@fortawesome/vue-fontawesome';
import { merge } from 'lodash';

const $ = require('jquery');

const now = new Date();
const nowISO = now.toISOString();
now.setDate(now.getDate()+1);
const tomorrowISO = now.toISOString();
now.setDate(now.getDate()+2);
const in3DaysISO = now.toISOString();
now.setDate(now.getDate()+4);
const in7DaysISO = now.toISOString();
const tmp = new Date();
const friday = 5;
const sunday = 0;
const move = friday - tmp.getDay();
const wkndStart = new Date(tmp.getFullYear(), tmp.getMonth(), tmp.getDate() + move);
const wkndStartISO = wkndStart.toISOString();
wkndStart.setDate(wkndStart.getDate()+3);
const wkndEndISO = wkndStart.toISOString();


export default {
  name: 'rovu-nav',

  created: function() {
    this.intervalName = null;
    this.reqArgs = {}
    this.$store.dispatch('fetchFacets')
  },

  components: {
    FontAwesomeIcon,
  },

  computed: mapGetters([
    'eventFacets',
    'eventList',
    'searchFacetId',
    'searchEventStart',
    'searchEventEnd',
  ]),

  mounted: function() {
    $('.ui.dropdown').dropdown();
    this.reqArgs = {
      event_start_after: null,
      event_end_before: null,
      category_id: null
    };
    this.markers = [];
    this.intervals = {
      h24: {
        start: nowISO,
        end: tomorrowISO
      },
      d3: {
        start: nowISO,
        end: in3DaysISO
      },
      w1: {
        start: nowISO,
        end: in7DaysISO
      },
      wknd: {
        start: wkndStartISO,
        end: wkndEndISO
      }
    }
  },

  methods: merge(
    mapActions(['openMobileSearchDrawer']),
    {
      changeInterval: function(evt) {
        let elt = $(evt.currentTarget);
        let interval = this.intervals[elt.data('interval')];
        if(this.intervalName === elt.data('interval')) {
          elt.removeClass('active');
          this.reqArgs.event_start_after = null;
          this.$store.dispatch('setSearchStart', null)
          this.reqArgs.event_end_before = null;
          this.$store.dispatch('setSearchEnd', null)
          this.intervalName = null;
        } else {
          this.intervalName = elt.data('interval');
          this.$store.dispatch('setSearchStart', interval.start)
          this.reqArgs.event_start_after = interval.start;
          this.$store.dispatch('setSearchEnd', interval.end)
          this.reqArgs.event_end_before = interval.end;
        }
        this.$store.dispatch('fetchEvents')
        this.getEvents();
      },

      changeCategory: function(evt) {
        let elt = $(evt.currentTarget);
        if(elt.data('id') === this.reqArgs.category_id) {
          elt.removeClass('active');
          this.$store.dispatch('setSearchFacet', null)
          this.reqArgs.category_id = null;
        } else {
          this.$store.dispatch('setSearchFacet', elt.data('id'))
          this.reqArgs.category_id = elt.data('id');
        }
        this.$store.dispatch('fetchEvents')
        this.getCategoryEvents();
      },

      getEvents: function() {
        $.get('/api/v1/events', this.reqArgs, this.parseResponse);
      },

      getCategoryEvents: function() {
        $.get('/api/v1/events', this.reqArgs, this.parseResponse);
      },

      parseResponse: function(res) {
        this.markEvents(res.events);
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
