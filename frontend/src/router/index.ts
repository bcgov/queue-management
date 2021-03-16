import Vue from 'vue'
import VueRouter from 'vue-router'
import config from '../../config'
import { routes } from './routes'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: config.BASE_URL,
  routes
})

export default router
