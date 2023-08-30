import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    cameras: [],
    isReady: false,
    center: [16.819814400000002, 96.1511424], //yangon
    currentLocation: [16.819814400000002, 96.1511424],
    filter: {
      type: ["Dome", "Bullet"],
      status: ["Good", "Disabled"],
    },
    isNeededGPS: false,
  },
  mutations: {
    setCameras: (state, data) => {
      state.cameras = data;
      state.isReady = true;
    },
    setFilter: (state, data) => {
      state.filter = data;
    },
    setIsNeededGPS: (state, data) => {
      state.isNeededGPS = data;
    },
    setCenter: (state, data) => {
      state.center = data;
    },
    setCurrentLocation: (state, data) => {
      state.currentLocation = data;
    },
    addNewCamera: (state, data) => {
      state.cameras = [...state.cameras, data];
    },
  },
  actions: {
    getCameras: ({ state, commit }) => {
      var status = "";
      var type = "";
      if (state.filter.status.length !== 2) {
        status = state.filter.status[0];
      }
      if (state.filter.type.length !== 2) {
        type = state.filter.type[0];
      }
      const queries = `?status=${status}&type=${type}`;
      axios.get("api/getCameras/" + queries).then((response) => {
        commit("setCameras", response.data);
      });
    },
    getCurrentLocation: ({ commit }) => {
      const oldLatlng = localStorage.getItem("latlng");
      if (oldLatlng) {
        commit("setCenter", JSON.parse(oldLatlng));
        commit("setCurrentLocation", JSON.parse(oldLatlng));
      }
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const latlng = [position.coords.latitude, position.coords.longitude];
          commit("setCurrentLocation", JSON.parse(oldLatlng));
          commit("setCenter", JSON.parse(oldLatlng));
          commit("setIsNeededGPS", false);
          const newLatlng = JSON.stringify(latlng);
          localStorage.setItem("latlng", newLatlng);
        },
        (error) => {
          commit("setIsNeededGPS", true);
          window.alert(`ERROR(${error.code}): ${error.message}`);
        }
      );
    },
  },
  getters: {},
});
