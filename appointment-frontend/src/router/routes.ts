import AppointmentBookingView from '@/views/AppointmentBookingView.vue'
import BookedAppointmentsView from '@/views/BookedAppointmentsView.vue'
import Home from '@/views/Home.vue'
import MixinExample from '@/views/MixinExample.vue'
import SigninView from '@/views/SigninView.vue'
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
    path: '/appointment',
    name: 'appointment',
    component: AppointmentBookingView,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/booked-appointments',
    name: 'booked-appointments',
    component: BookedAppointmentsView,
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
    path: '/signin/:idpHint',
    name: 'signin',
    component: SigninView,
    props: true,
    meta: { requiresAuth: false }
  },
  {
    // default/fallback route
    path: '*',
    redirect: '/'
  }
]
