
/* tslint-disable */
import Admin from '../views/admin.vue'
import Agenda from '@/components/Agenda/Agenda.vue'
import App from '../views/App.vue'
import Appointments from '../components/Appointments/appointments.vue'

import ButtonsAdmin from '../views/buttons-admin.vue'
import ButtonsAgenda from '@/components/Agenda/buttons-agenda.vue'
import ButtonsAppointments from '../components/Appointments/buttons-appointments.vue'
import ButtonsCalendar from '../components/Booking/buttons-calendar.vue'
import ButtonsDash from '@/components/ServeCitizen/dash-buttons.vue'
import ButtonsExams from '../components/exams/buttons-exams.vue'
import ButtonsUpload from '@/components/upload/buttons-upload.vue'

import Calendar from '../components/Booking/calendar.vue'
import Dash from '@/components/ServeCitizen/dash.vue'
import Exams from '../components/exams/exams.vue'
import Smartboard from '@/components/smartboard/index.vue'

import Upload from '@/components/upload/upload.vue'
import Tasklist from '@/views/TaskList.vue'
import ButtonTasklist from '@/components/TaskList/ButtonTasklist.vue'

import FormView from '@/views/FormView.vue'

export const routes = [
  {
    path: '/',
    component: App,
    redirect: '/queue',
    children: [
      {
        path: 'queue',
        components: {
          default: Dash,
          buttons: ButtonsDash
        },
        meta: { hideCitizenWaiting: true }
      },
      {
        path: 'admin',
        components: {
          default: Admin,
          buttons: ButtonsAdmin
        },
        meta: { hideCitizenWaiting: true }
      },
      {
        path: 'exams',
        components: {
          default: Exams,
          buttons: ButtonsExams
        },
        meta: { hideCitizenWaiting: false }
      },
      {
        path: 'agenda',
        components: {
          default: Agenda,
          buttons: ButtonsAgenda
        },
        meta: { hideCitizenWaiting: true }
      },
      {
        path: 'appointments',
        components: {
          default: Appointments,
          buttons: ButtonsAppointments
        },
        meta: { hideCitizenWaiting: true }
      },
      {
        path: 'booking',
        components: {
          default: Calendar,
          buttons: ButtonsCalendar
        },
        meta: { hideCitizenWaiting: false }
      },
      {
        path: 'upload',
        components: {
          default: Upload,
          buttons: ButtonsUpload
        },
        meta: { hideCitizenWaiting: false }
      },
      {
        path: 'service-flow/:taskId?',
        components: {
          default: Tasklist,
          buttons: ButtonTasklist
        },
        props: true,
        meta: { hideCitizenWaiting: false }
      },
      {
        path: 'form/:form_id/submission/:submission_id',
        components: {
          default: FormView,
          buttons: ButtonTasklist
        },
        meta: { hideCitizenWaiting: false }
      },
      {
        path: 'form/:form_id/submission/:submission_id',
        components: {
          default: FormView,
          buttons: ButtonTasklist
        },
        meta: { hideCitizenWaiting: false }
      }
    ]
  },
  {
    path: '/smartboard/:office_number',
    component: Smartboard,
    props: true
  },
  {
    path: '/smartboard/',
    component: Smartboard
  }
]
