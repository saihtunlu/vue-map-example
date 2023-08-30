<template>
  <div id="app" class="container-fluid">
    <router-view :key="$route.fullPath" class="route-view" />
    <!-- <div v-if="isNeededGPS">
      <strong
        >We're sorry but App doesn't work properly without GPS enabled. Please
        enable it to continue.</strong
      >
    </div> -->
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      loading: null,
    };
  },
  components: {},
  computed: {
    ...mapState(["isReady", "isNeededGPS"]),
  },
  watch: {
    isReady(value) {
      if (value) {
        this.loading.close();
      }
    },
  },
  created() {
    this.loading = this.$vs.loading();
    setTimeout(() => {
      let vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty("--vh", `${vh}px`);
    }, 500);
  },
  methods: {},
};
</script>

<style >
div#app {
  max-height: calc(var(--vh, 1vh) * 100);
  overflow: hidden;
}
</style>