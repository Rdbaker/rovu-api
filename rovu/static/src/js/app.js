global.jQuery = require('jquery');
global.$ = jQuery;

require('semantic-ui/dist/semantic');
const Vue = require('vue');

const App = require('./app.vue');


var app = new Vue({
  el: '#rovu-app',
  template: '<app></app>',
  render: (h) => h(App)
});

function getEvents(callback) {
  let now = new Date();
  let nowISO = now.toISOString();
  now.setDate(now.getDate()+2);
  let tomorrowISO = now.toISOString();
  $.getJSON('/api/v1/events', {
    event_start_after: nowISO,
    event_end_before: tomorrowISO
  }, callback);
}

function markEvent(ev) {
  var marker = new google.maps.Marker({
    position: {lat: Number(ev.venue.latitude), lng: Number(ev.venue.longitude)},
    map: window.map,
    title: ev.name
  });
  var start_date = new Date(ev.start_datetime);
  var end_date = new Date(ev.end_datetime);
  var addr = !!ev.venue.address ? ev.venue.address.address_1 : "Address Unknown";
  var windowContent = ('<div class="event-content">' +
      '<div class="event-title">' + ev.name + '</div>' +
      '<div class="event-venue">' + ev.venue.name + '</div>' +
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
    infowindow.open(window.map, marker);
  });
}

function markEvents() {
  getEvents(function(events) {
    for(var i=0; i<events.length; i++) {
      markEvent(events[i]);
    }
  });
}
