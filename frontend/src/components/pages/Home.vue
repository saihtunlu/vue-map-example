<template>
  <div class="row">
    <div class="col-12 px-0">
      <Nav />
    </div>
    <div class="col-12 px-0">
      <Map />
    </div>
  </div>
</template>

<script>
import Map from "../common/Map.vue";
import Nav from "../common/Nav.vue";
import { mapState } from "vuex";
export default {
  components: {
    Map,
    Nav,
  },
  created() {},

  computed: {
    ...mapState(["isReady"]),
  },
};
</script>

<style scoped>
</style>