import 'core-js/stable' // to polyfill ECMAScript features
import '@mdi/font/css/materialdesignicons.min.css' // icon library (https://materialdesignicons.com/)
import 'regenerator-runtime/runtime' // to use transpiled generator functions
import * as VueGoogleMaps from 'vue2-google-maps'
import App from './App.vue'
import ConfigHelper from '@/utils/config-helper'
import TokenService from '@/services/token.services'
import Vue from 'vue'
import i18n from './plugins/i18n'
import router from './router'
import { store } from './store'
import vuetify from './plugins/vuetify'

require('date-time-format-timezone') // IE 11 polyfill to work with timezones

Vue.config.productionTip = false
Vue.prototype.$tokenService = new TokenService()

Vue.use(VueGoogleMaps, {
  load: {
    key: process.env.GOOGLE_MAP_API_KEY || '',
    libraries: 'places'
  }
})
/**
 * The server side configs are necessary for app to work , since they are reference in templates and all
 *  Two ways , either reload Vue after we get the settings or load vue after we get the configs..going for second
 */
ConfigHelper.fetchConfig().then((_data: any) => {
  renderVue()
})

function renderVue () {
  new Vue({
    router,
    vuetify,
    i18n,
    store,
    render: (h) => h(App)
  }).$mount('#app')
}
