<template>
  <div id="rovu-gmap-elt"></div>
</template>


<style>

#rovu-gmap-elt {
  height: 100%;
}

</style>


<script>
const GML = require('google-maps');

GML.KEY = 'AIzaSyD8oAbVWiehpO6lssOaqJXMLnLTsqtOG8M';

const center = {
  lat: 52.477564,
  lng: -2.003714
};

export default {
  name: 'rovu-map',

  mounted () {
    GML.load((google) => {
      global.google = google;
      global.map = new google.maps.Map(document.getElementById('rovu-gmap-elt'), {
        center: center,
        zoom: 11,
        clickableIcons: false,
        disableDefaultUI: true
      });
    })
  },
};
</script>
