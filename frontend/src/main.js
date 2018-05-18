// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import VueSocketio from 'vue-socket.io'
import 'es6-promise/auto'
import App from './App'
import Login  from './Login'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from 'axios'
import { store } from './store/'
Vue.prototype.$axios = axios

Vue.use(BootstrapVue)
Vue.use(VueSocketio, 'http://qsystem-dev.apps.olivewoodsoftware.com/')
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  created() {
    let url  = 'http://qsystem-dev.apps.olivewoodsoftware.com/api/v1/users/me/'
    this.$axios.get(url, {withCredentials: true})
      .then( () => {
        this.$store.commit('logIn')
      })
  },
  template: '<div><Login/></div>',
  components: { Login }
})
