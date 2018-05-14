import { mapActions, mapGetters } from 'vuex';
import { Datetime } from 'vue-datetime';
import FontAwesomeIcon from '@fortawesome/vue-fontawesome';
import { merge } from 'lodash';


export default {
  name: 'rovu-drawer',

  components: {
    FontAwesomeIcon,
    Datetime,
  },

  watch: {
    searchEventStartDate: function(val) {
      this.setSearchStart(val);
    },
    searchEventEndDate: function(val) {
      this.setSearchEnd(val);
    },
  },

  computed: mapGetters({
    isActive: 'mobileSearchDrawerOpen',
    startDate: 'searchEventStart',
    endDate: 'searchEventEnd',
  }),

  methods: merge(
    mapActions(['closeMobileSearchDrawer', 'fetchEvents', 'setSearchStart', 'setSearchEnd']),
    {
      setStartDate: function(date) {
        this.$store.dispatch('setSearchStart', !!date ? date.toISOString() : date)
        this.$store.dispatch('fetchEvents')
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


    }
  ),
}