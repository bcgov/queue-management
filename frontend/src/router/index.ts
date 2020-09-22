
import Vue from 'vue'
import VueRouter from 'vue-router'

import { routes } from './routes'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// router.beforeEach(async (to, from, next) => {
//   // Detecting IE version and showing not available message if its less than 11
//   if (CommonUtils.isAllowedIEVersion() && !(to.name === 'no-content')) {
//     return next('/no-content/unavailable')
//   }
//   if (to.path === '/signout') {
//     return next()
//   }
//   const isOnlineAppointmentUser = (ConfigHelper.getFromSession(SessionStorageKeys.KeyCloakToken))
//     ? await keycloakServices.isRolesAvailable([Role.OnlineAppointmentUser]) : true
//   if (!isOnlineAppointmentUser && !(to.name === 'no-content')) {
//     return next('/no-content/unauthorized')
//   }
//   next()
// })

export default router
