/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/

import Vue from 'vue'
import 'es6-promise/auto'
import { store } from './store/'
import BootstrapVue from 'bootstrap-vue'
import Router from './router'
import Fragment from 'vue-fragment'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
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
  faClock,
  faShippingFast,
  faExclamation,
  faExclamationTriangle,
  faFilter,
  faLifeRing,
  faMinus,
  faPlus,
  faSort,
  faStopwatch,
  faWindowMaximize,
  faWindowRestore,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VDragged from 'v-dragged'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/css/q.css'
import './assets/css/bc-gov-style.css'
require('es6-shim')
require('Keycloak')

Vue.use(VDragged)
Vue.use(Fragment.Plugin)
library.add(
  faClock,
  faAngleLeft,
  faAngleRight,
  faBars,
  faCalendar,
  faCaretLeft,
  faCaretRight,
  faCaretDown,
  faCheck,
  faCheckSquare,
  faClipboardCheck,
  faShippingFast,
  faExclamation,
  faExclamationTriangle,
  faFilter,
  faLifeRing,
  faMinus,
  faPlus,
  faSort,
  faStopwatch,
  faWindowMaximize,
  faWindowRestore,
)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(BootstrapVue)

var keycloak = Keycloak(process.env.KEYCLOAK_JSON_URL)
Vue.prototype.$keycloak = keycloak
Vue.config.productionTip = false

/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  store,
  router: Router,
  template: '<router-view></router-view>',
})
