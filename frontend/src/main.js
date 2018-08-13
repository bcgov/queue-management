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
import App from './App'
import Smartboard from './smartboard/'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/css/bc-gov-style.css'
Vue.use(BootstrapVue)

require('es6-shim')
require('Keycloak')
var keycloak = Keycloak(process.env.KEYCLOAK_JSON_URL)
Vue.prototype.$keycloak = keycloak
Vue.config.productionTip = false

const routes = {
  '/': App,
  'smartboard': Smartboard
}

/* eslint-disable no-new */
const app = new Vue({
  el: '#app',
  store,
  components: { App, Smartboard },
  computed: {
    currentRoute() {
      let path = window.location.pathname
      let pathspl = path.split('/')
      if ( path === '/') {
        return '/'
      } else if (pathspl.length >= 2) {
        return pathspl[1]
      } else {
        return '/'
      }
    },
    ViewComponent () {
      return routes[this.currentRoute]
    }
  },

  render (h) { return h(this.ViewComponent) }
})
