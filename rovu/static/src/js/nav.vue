<template>
<div class="ui top attached text menu">
  <div class="ui dropdown item">
    Show events within
    <i class="dropdown icon"></i>
    <div class="menu" id="events-within">
      <div class="item" data-interval="h24" v-on:click="changeInterval">24hrs</div>
      <div class="item" data-interval="d3" v-on:click="changeInterval">next 3 days</div>
      <div class="item" data-interval="w1" v-on:click="changeInterval">the next week</div>
      <div class="item" data-interval="wknd" v-on:click="changeInterval">the weekend</div>
    </div>
  </div>
</div>
</template>


<style>
</style>


<script>
$ = require('jquery');

let now = new Date();
let nowISO = now.toISOString();
now.setDate(now.getDate()+1);
let tomorrowISO = now.toISOString();
now.setDate(now.getDate()+2);
let in3DaysISO = now.toISOString();
now.setDate(now.getDate()+4);
let in7DaysISO = now.toISOString();
let tmp = new Date();
let friday = 5;
let sunday = 0;
let moveForward = Math.abs(tmp.getDay() - friday);
let wkndStart = new Date(tmp.getYear(), tmp.getMonth(), tmp.getDate()+moveForward);
let wkndStartISO = wkndStart.toISOString();
wkndStart.setDate(wkndStart.getDate()+3);
let wkndEndISO = wkndStart.toISOString();


export default {
  name: 'rovu-nav',

  mounted: function() {
    $('.ui.dropdown').dropdown();
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

  methods: {
    changeInterval: function(evt) {
      this.getEvents(this.intervals[$(evt.currentTarget).data('interval')]);
    },

    getEvents: function(interval) {
      $.getJSON('/api/v1/events', {
        event_start_after: interval.start,
        event_end_before: interval.end
      }, this.markEvents);
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
      var addr = !!ev.venue.address ? ev.venue.address.address_1 : "Address Unknown";
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
        mixpanel.track('marker.click');
        infowindow.open(map, marker);
      });
      this.markers.push(marker);
    }

  },
};
</script>
