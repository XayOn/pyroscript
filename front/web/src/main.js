import Vue from "vue";
import "./plugins/axios";
import "./plugins/vuetify";

import ListWifis from "./components/ListWifis";
import ListTargets from "./components/ListTargets";
import App from "./App.vue";

import VueRouter from "vue-router";

Vue.use(VueRouter);
Vue.config.productionTip = false;

const router = new VueRouter({
  routes: [
    { path: "/", component: ListWifis },
    { path: "/targets", component: ListTargets }
  ]
});

new Vue({ el: "#app", router: router, render: h => h(App) }).$mount("#app");
