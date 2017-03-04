<template>
<div class="ui top attached text menu">
  <div class="ui dropdown item">
    Show events within
    <i class="dropdown icon"></i>
    <div class="menu" id="events-within">
      <div class="item" :class="{ active: intervalName == 'h24' }"
        data-interval="h24" v-on:click="changeInterval">24hrs<div class="small-text" v-if="intervalName == 'h24'">&times; (click to remove filter)</div></div>
      <div class="item" :class="{ active: intervalName == 'd3' }"
        data-interval="d3" v-on:click="changeInterval">next 3 days<div class="small-text" v-if="intervalName == 'd3'">&times; (click to remove filter)</div></div>
      <div class="item" :class="{ active: intervalName == 'w1' }"
        data-interval="w1" v-on:click="changeInterval">the next week<div class="small-text" v-if="intervalName == 'w1'">&times; (click to remove filter)</div></div>
      <div class="item" :class="{ active: intervalName == 'wknd' }"
        data-interval="wknd" v-on:click="changeInterval">the weekend<div class="small-text" v-if="intervalName == 'wknd'">&times; (click to remove filter)</div></div>
    </div>
  </div>
  <div class="ui dropdown item">
    Show events of type
    <i class="dropdown icon"></i>
    <div class="menu" id="event-category">
      <div class="item" :class="{ active: reqArgs.category_id == cat.category_id }"
          v-bind:data-id="cat.category_id" v-for="cat in categoryFacets" v-on:click="changeCategory">
        <div>{{ cat.name }}</div>
        <div class="small-text">({{ cat.event_count }})</div>
        <div class="small-text" v-if="reqArgs.category_id == cat.category_id">&times; (click to remove filter)</div>
      </div>
    </div>
  </div>
</div>
</template>


<style>
#event-category {
  max-height: 300px;
  overflow: scroll;
}

.small-text {
  color: #888;
  font-size: 0.8em;
}
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
let move = friday - tmp.getDay();
let wkndStart = new Date(tmp.getFullYear(), tmp.getMonth(), tmp.getDate() + move);
let wkndStartISO = wkndStart.toISOString();
wkndStart.setDate(wkndStart.getDate()+3);
let wkndEndISO = wkndStart.toISOString();


export default {
  name: 'rovu-nav',

  created: function() {
    this.getCategoryFacets();
    this.intervalName = null;
  },

  data: function() {
    return {
      categoryFacets: []
    };
  },

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

  methods: {
    changeInterval: function(evt) {
      let elt = $(evt.currentTarget);
      let interval = this.intervals[elt.data('interval')];
      if(this.intervalName === elt.data('interval')) {
        elt.removeClass('active');
        this.reqArgs.event_start_after = null;
        this.reqArgs.event_end_before = null;
        this.intervalName = null;
      } else {
        this.intervalName = elt.data('interval');
        this.reqArgs.event_start_after = interval.start;
        this.reqArgs.event_end_before = interval.end;
      }
      this.getEvents();
    },

    changeCategory: function(evt) {
      let elt = $(evt.currentTarget);
      if(elt.data('id') === this.reqArgs.category_id) {
        elt.removeClass('active');
        this.reqArgs.category_id = null;
      } else {
        this.reqArgs.category_id = elt.data('id');
      }
      this.getCategoryEvents();
    },

    getCategoryFacets: function() {
      $.get('/api/v1/events/categories/facets')
        .done(this.assignFacets);
    },

    assignFacets: function(facets) {
      this.categoryFacets = facets;
    },

    getEvents: function() {
      $.getJSON('/api/v1/events', this.reqArgs, this.parseResponse);
    },

    getCategoryEvents: function() {
      $.get('/api/v1/events', this.reqArgs, this.parseResponse);
    },

    parseResponse: function(res) {
      this.assignFacets(res.facets);
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
};
</script>
