<template>
  <div style="height: calc((var(--vh, 1vh) * 100) - 60px)">
    <LMap
      :zoom="zoom"
      ref="map"
      v-if="isReady"
      :center="center"
      @update:center="updateCenter"
      :options="{ zoomControl: false }"
    >
      <LControl position="bottomright">
        <vs-button icon @click="$store.dispatch('getCurrentLocation')"
          ><i class="bx bx-current-location"></i
        ></vs-button>
      </LControl>
      <LControlZoom position="bottomright"></LControlZoom>

      <LMarker :lat-lng="currentLocation" v-if="currentLocation">
        <LIcon>
          <div class="current-marker">
            <div class="dot"></div>
            <div class="grow"></div>
          </div>
        </LIcon>
      </LMarker>

      <LMarker
        :lat-lng="[camera.latitude, camera.longitude]"
        v-for="(camera, index) in cameras"
        :key="index"
        @click="clickCamera(camera)"
      >
        <LIcon>
          <div class="marker">
            <div
              class="dot"
              :class="camera.status == 'Disabled' ? 'disabled-dot' : 'good-dot'"
            ></div>
            <div
              class="grow"
              :class="
                camera.status == 'Disabled' ? 'disabled-grow' : 'good-grow'
              "
            ></div>
          </div>
        </LIcon>
      </LMarker>
      <LTileLayer :url="url"></LTileLayer>
    </LMap>

    <vue-bottom-sheet
      overlay
      click-to-close
      rounded
      max-height="100%"
      ref="cameraDetail"
      @closed="active = false"
    >
      <div class="model-body">
        <CameraDetail v-if="active" :camera="selectedCamera" />
      </div>
    </vue-bottom-sheet>
  </div>
</template>

<script>
import { mapState } from "vuex";
import CameraDetail from "./CameraDetail.vue";
import VueBottomSheet from "@webzlodimir/vue-bottom-sheet";
import {
  LMap,
  LTileLayer,
  LMarker,
  LIcon,
  LControl,
  LControlZoom,
} from "vue2-leaflet";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LIcon,
    LControl,
    LControlZoom,
    CameraDetail,
    VueBottomSheet,
  },
  data() {
    return {
      // url: "http://mt0.google.com/vt/hl=en&x={x}&y={y}&z={z}&s={s}",
      // url:'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    url:'https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png',
      zoom: 16,
      bounds: null,
      active: false,
      active2: false,
      selectedCamera: {},
    };
  },
  created() {},
  methods: {
    updateCenter(center) {
      this.$store.commit("setCenter", center);
    },
    clickCamera(camera) {
      this.selectedCamera = camera;
      this.$refs.cameraDetail.open();
      this.active = true;
    },
  },
  computed: {
    ...mapState(["center", "currentLocation", "cameras", "isReady"]),
  },
};
</script>
<style>
.current-marker {
  display: flex;
  justify-content: center;
  align-items: center;
}
.current-marker .grow {
  background: rgb(var(--vs-primary));
  box-shadow: 0px 4px 25px 0px rgb(var(--vs-primary), 1);
  height: 10px;
  min-width: 10px;
  z-index: 999;
  border-radius: 50%;
  animation: grow 2s ease-in infinite;
}

.current-marker .dot {
  position: absolute;
  height: 70px;
  width: 70px;
  z-index: 2;
  opacity: 0;
  border: 10px solid rgb(var(--vs-primary));
  background: rgb(var(--vs-primary), 0.6);
  border-radius: 50%;
  animation: pulse 2s ease-out;
  animation-iteration-count: infinite;
}

.marker {
  display: flex;
  justify-content: center;
  align-items: center;
}
.marker .grow {
  height: 10px;
  min-width: 10px;
  z-index: 999;
  border-radius: 50%;
  animation: grow 2s ease-in infinite;
}
.good-grow {
  background: rgb(var(--vs-success));
  box-shadow: 0px 4px 25px 0px rgb(var(--vs-success), 1);
}
.disabled-grow {
  background: rgb(var(--vs-danger));
  box-shadow: 0px 4px 25px 0px rgb(var(--vs-danger), 1);
}

.marker .dot {
  position: absolute;
  height: 20px;
  width: 20px;
  z-index: 2;
  opacity: 0;
  border-radius: 50%;
  animation: pulse 2s ease-out;
  animation-iteration-count: infinite;
}
.good-dot {
  border: 10px solid rgb(var(--vs-success));
  background: rgb(var(--vs-success), 0.6);
}
.disabled-dot {
  border: 10px solid rgb(var(--vs-danger));
  background: rgb(var(--vs-danger), 0.6);
}

@-webkit-keyframes pulse {
  0% {
    -webkit-transform: scale(0);
    opacity: 1;
  }

  100% {
    -webkit-transform: scale(2);
    opacity: 0;
  }
}
@-webkit-keyframes grow {
  0% {
    -webkit-transform: scale(1);
  }
  55% {
    -webkit-transform: scale(1.2);
  }
  65% {
    -webkit-transform: scale(0.6);
  }
  70% {
    -webkit-transform: scale(1);
  }
}
</style>