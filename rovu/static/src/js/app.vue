<template>
  <div id="app-container">
    <rovu-nav></rovu-nav>
    <rovu-map></rovu-map>
  </div>
</template>

<style>

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app-container {
  height: 100%;
}

</style>

<script>

import RovuMap from './map.vue'
import RovuNav from './nav.vue'

export default {
  name: 'app',
  components: {
    RovuMap,
    RovuNav
  }
}

</script>
