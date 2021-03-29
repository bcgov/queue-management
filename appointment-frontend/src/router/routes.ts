import AccountSettingsView from '@/views/AccountSettingsView.vue'
import AppointmentBookingView from '@/views/AppointmentBookingView.vue'
import BookedAppointmentsView from '@/views/BookedAppointmentsView.vue'
import LoginSelectorView from '@/views/LoginSelectorView.vue'
import NoContentView from '@/views/NoContentView.vue'
import SigninView from '@/views/SigninView.vue'
import SignoutView from '@/views/SignoutView.vue'
import WalkinQ from '@/views/WalkinQ.vue'

export const routes = [
  {
    path: '/',
    redirect: '/appointment'
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
      requiresAuth: true
    }
  },
  {
    path: '/account-settings',
    name: 'account-settings',
    component: AccountSettingsView,
    meta: {
      requiresAuth: true
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
    path: '/signout',
    name: 'signout',
    component: SignoutView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginSelectorView,
    props: true,
    meta: { requiresAuth: false }
  },
  {
    path: '/no-content/:msgType',
    name: 'no-content',
    component: NoContentView,
    props: true,
    meta: { requiresAuth: false, skipNoContent: true }
  },
  {
    // default/fallback route
    path: '*',
    redirect: '/appointment'
  },
  {
    path: '/walk-in-Q/:uniqueId',
    name: 'walk-in-Q',
    component: WalkinQ,
    props: true,
    meta: { requiresAuth: false, skipNoContent: true }
  }
]
