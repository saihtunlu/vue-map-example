import Vue from "vue";
import VueRouter from "vue-router";
Vue.use(VueRouter);

import Home from "../../components/pages/Home.vue";
const routes = [
  {
    path: "*",
    name: "Home",
    component: Home,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
  linkActiveClass: "active",
  linkExactActiveClass: "exact-active",
});

export default router;
