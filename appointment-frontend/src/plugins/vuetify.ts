import 'vuetify/dist/vuetify.min.css'
import '$assets/scss/base.scss'
import '$assets/scss/layout.scss'
import '$assets/scss/overrides.scss'

import Vue from 'vue'
import Vuetify from 'vuetify'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: {
        grey: {
          base: '#adb5bd',
          lighten5: '#f8f9fa',
          lighten4: '#f1f3f5',
          lighten3: '#e9ecef',
          lighten2: '#dee2e6',
          lighten1: '#ced4da',
          darken1: '#868e96',
          darken2: '#495057',
          darken3: '#343a40',
          darken4: '#212529'
        },
        navBg: '#003366',
        navMenuBg: '#26527d',
        primary: '#003366',
        success: '#3a833c', // Darkened for accessibility w/ white text
        info: '#1274c4' // Darken for accessibility with white text on it,
      },
      dark: {}
    }
  }
})
