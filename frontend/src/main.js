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
import App from './App'
import { store } from './store/'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)

import 'es6-promise/auto'
import axios from 'axios'
const axiosInstance = axios.create({
  baseURL: process.env.API_URL,
  withCredentials: true
})
Vue.prototype.$axios = axiosInstance

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  created() {
    let url  = "/users/me/"
    this.$axios.get(url)
      .then( response => {
        let user = {
          name: response.data.username,
          office_id: response.data.office_id
        }
        console.log(user)
        this.$store.commit('logIn')
        this.$store.commit('setUser', user)
        })
      },
  template: '<App />',
  components: { App }
})
