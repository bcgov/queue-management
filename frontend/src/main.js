// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueSocketio from 'vue-socket.io'
import 'es6-promise/auto'
import App from './App'
import axios from 'axios'
import { store } from './store/'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.prototype.$axios = axios

Vue.use(BootstrapVue)
Vue.use(VueSocketio, process.env.API_URL)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  created() {
    let url  = process.env.API_URL + "/users/me/"
    this.$axios.get(url, {withCredentials: true})
      .then( () => {
        this.$store.commit('logIn')
      })
  },
  template: '<App />',
  components: { App }
})
