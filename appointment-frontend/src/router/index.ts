import Vue from 'vue'
import VueRouter from 'vue-router'
import { routes } from './routes'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior (to, from, savedPosition) {
    // see https://router.vuejs.org/guide/advanced/scroll-behavior.html
    return { x: 0, y: 0 }
  }
})

export default router
