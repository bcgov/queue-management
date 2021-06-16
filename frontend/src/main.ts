/* Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */

/*eslint-disable */
/*tslint-disable */
import "babel-polyfill"; // For IE11 compat
import "./router/componentHooks"; // <-- Needs to be first to work beforeRouteLeave
import "core-js/stable"; // For IE11 compat

import Vue from "vue";
import vuetify from "./plugins/vuetify";
import Buefy from "buefy";
import "es6-promise/auto";
import store from "./store/index";
import BootstrapVue from "bootstrap-vue";
import router from "./router";
import { Plugin } from "vue-fragment";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faAngleLeft,
  faAngleRight,
  faBars,
  faCalendar,
  faCalendarAlt,
  faCaretDown,
  faCaretLeft,
  faCaretRight,
  faCheck,
  faCheckSquare,
  faClipboardCheck,
  faClock,
  faDollarSign,
  faEdit,
  faEraser,
  faExclamation,
  faExclamationTriangle,
  faFileAlt,
  faFilter,
  faHandsHelping,
  faLifeRing,
  faMinus,
  faPhone,
  faPlus,
  faShareSquare,
  faShippingFast,
  faSort,
  faStopwatch,
  faTrashAlt,
  faUserAlt,
  faUserCheck,
  faUserCircle,
  faWalking,
  faWindowMaximize,
  faWindowRestore
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import VDragged from "v-dragged";
import "buefy/dist/buefy.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "./assets/css/q.css";
import "./assets/css/bc-gov-style.css";
import MainApp from "./MainApp.vue";

import ConfigHelper from "@/utils/config-helper";

import FormsFlowStore from "camunda-formio-tasklist-vue/src/store/index";
Vue.use(FormsFlowStore, { store });

require("es6-shim");
// require('Keycloak')
require("../static/keycloak.js");
// import * as Keycloak from "../static/keycloak.js";
const Keycloak = window && (window as any).Keycloak;
Vue.use(Buefy);
Vue.use(VDragged);
Vue.use(Plugin);
library.add(
  faAngleLeft,
  faAngleRight,
  faBars,
  faCalendar,
  faCaretDown,
  faCaretLeft,
  faCaretRight,
  faCheck,
  faCheckSquare,
  faClipboardCheck,
  faHandsHelping,
  faShippingFast,
  faClock,
  faDollarSign,
  faEraser,
  faExclamation,
  faExclamationTriangle,
  faFileAlt,
  faFilter,
  faLifeRing,
  faMinus,
  faPlus,
  faShareSquare,
  faSort,
  faStopwatch,
  faUserCheck,
  faTrashAlt,
  faUserAlt,
  faUserCircle,
  faWindowMaximize,
  faWindowRestore,
  faEdit,
  faPhone,
  faCalendarAlt,
  faWalking
);
Vue.component("font-awesome-icon", FontAwesomeIcon);
Vue.use(BootstrapVue);
var keycloak = Keycloak(process.env.KEYCLOAK_JSON_URL);
Vue.prototype.$keycloak = keycloak;
Vue.config.productionTip = false;

/* eslint-disable no-new */
// const app = new Vue({
//   el: "#app",
//   store,
//   router: Router,
//   template: "<router-view></router-view>"
// });
/* eslint-disable no-new */

ConfigHelper.fetchConfig();

new Vue({
  router,
  store,
  vuetify,
  render: h => h(MainApp)
}).$mount("#app");
