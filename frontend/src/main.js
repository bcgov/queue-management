import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'es6-promise/auto'
import App from './App'
import axios from 'axios'
import { store } from './store/'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


const axiosInstance = axios.create({
    baseURL: process.env.API_URL,
    withCredentials: true
})

Vue.prototype.$axios = axiosInstance

Vue.use(BootstrapVue)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  created() {
    const io = require('socket.io-client')
    const socket = io(process.env.API_URL)
    let url  = "/users/me/"
    this.$axios.get(url)
      .then( () => {
        this.$store.commit('logIn')
        this.$store.commit('setUser', {
          username: response.data.username,
          office_id: response.data.office_id
        })
      })
  },
  template: '<App />',
  components: { App }
})
