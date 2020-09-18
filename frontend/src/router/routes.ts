
import App from '../App.vue'
import Dash from '@/components/ServeCitizen/dash.vue'
import ButtonsDash from '@/components/ServeCitizen/dash-buttons'
import Smartboard from '../smartboard/'
import ButtonsAdmin from '../buttons-admin'
import Admin from '../admin'
import Exams from '../components/exams/exams'
import ButtonsExams from '../components/exams/buttons-exams'
import Agenda from '../agenda/agenda'
import ButtonsAgenda from '../agenda/buttons-agenda'
import Calendar from '../components/Booking/calendar'
import ButtonsCalendar from '../components/Booking/buttons-calendar'
import Appointments from '../components/Appointments/appointments.vue'
import ButtonsAppointments from '../components/Appointments/buttons-appointments'
import Upload from '../upload/upload'
import ButtonsUpload from '../upload/buttons-upload'

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
