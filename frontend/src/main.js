import Vue from "vue";
import {API_URL} from './assets/constants/data'
import App from "./App.vue";
import router from "./core/router";
import store from "./core/store";
import Notification from "./services/notification";
import Vuesax from "vuesax";
import "vuesax/dist/vuesax.css"; //Vuesax styles
import i18n from "./core/i18n";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import axios from 'axios';
axios.defaults.baseURL = API_URL;
import VueLazyload from "vue-lazyload";
Vue.use(VueLazyload, {
  error: "image/error.png",
  loading: "image/loader.svg",
});


//import css
import "./assets/fonts/boxIcon/css/boxicons.min.css";
import "./assets/css/main.css";

import "leaflet/dist/leaflet.css";
import { Icon } from "leaflet";
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

Vue.use(Vuesax, {
  colors: {
    primary: "#6751B0",
  },
});
Vue.use(ElementUI);
Vue.use(require("vue-moment"));

Vue.config.productionTip = false;
new Vue({
  created() {
    Vue.prototype.$noti = new Notification(this.$vs.notification);
    this.$store.dispatch("getCameras");
    this.$store.dispatch("getCurrentLocation");
  },
  render: (h) => h(App),
  i18n,
  router,
  store,
}).$mount("#app");
