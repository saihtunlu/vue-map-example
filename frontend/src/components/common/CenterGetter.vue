<template>
  <div class="map-box">
    <LMap
      :zoom="zoom"
      ref="map"
      :center="center"
      @update:center="updateCenter"
      :options="{ zoomControl: false }"
    >
      <LControl position="bottomright">
        <vs-button
          :loading="isLoading"
          icon
          @click="$store.dispatch('getCurrentLocation')"
          ><i class="bx bx-current-location"></i
        ></vs-button>
      </LControl>
      <LControlZoom position="bottomright"></LControlZoom>

      <LMarker :lat-lng="center">
        <LIcon>
          <div class="current-marker">
            <div class="dot"></div>
            <div class="grow"></div>
          </div>
        </LIcon>
      </LMarker>
      <LTileLayer :url="url"></LTileLayer>
    </LMap>
  </div>
</template>

<script>
import { mapState } from "vuex";
import {
  LMap,
  LTileLayer,
  LMarker,
  LControl,
  LControlZoom,
  LIcon,
} from "vue2-leaflet";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LControl,
    LControlZoom,
    LIcon,
  },
  props: {
    center: null,
  },
  data() {
    return {
      // url: "http://mt0.google.com/vt/hl=en&x={x}&y={y}&z={z}&s={s}",
      // url:'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',  
       url:'https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png',
           zoom: 16,
      bounds: null,
      isLoading: false,
    };
  },
  watch: {},
  created() {},
  methods: {
    updateCenter(center) {
      this.$emit("getCenter", center);
    },
  },
  computed: {
    ...mapState(["isReady"]),
  },
};
</script>
<style>
.map-box {
  height: 200px;
  border-radius: 10px;
  overflow: hidden !important;
}
</style>