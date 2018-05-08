<template>
  <div id="rovu-gmap-elt"></div>
</template>


<style>

#rovu-gmap-elt {
  height: calc(100% - 60px);
}

@media screen and (max-width: 500px){
  #rovu-gmap-elt {
    height: 100%;
  }
}

</style>


<script>
const GML = require('google-maps');

GML.KEY = 'AIzaSyD8oAbVWiehpO6lssOaqJXMLnLTsqtOG8M';

const center = {
  lat: 42.3617131,
  lng: -71.0921,
};

export default {
  name: 'rovu-map',

  mounted () {
    GML.load((google) => {
      global.google = google;
      global.map = new google.maps.Map(document.getElementById('rovu-gmap-elt'), {
        center: center,
        zoom: 14,
        clickableIcons: false,
        disableDefaultUI: true
      });
    })
  },
};
</script>
