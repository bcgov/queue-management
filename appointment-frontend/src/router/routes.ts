import Home from '@/views/Home.vue'
import MixinExample from '@/views/MixinExample.vue'
import StateExample from '@/views/StateExample.vue'

export const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/MixinExample',
    name: 'mixinExample',
    component: MixinExample,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/StateExample',
    name: 'stateExample',
    component: StateExample,
    meta: {
      requiresAuth: false
    }
  },
  {
    // default/fallback route
    path: '*',
    redirect: '/'
  }
]
