/*
 * Copyright 2015 Province of British Columbia
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import Vue from 'vue'
import Router from 'vue-router'
import App from './App'
import Dash from './serve-citizen/dash.vue'
import ButtonsDash from '@/serve-citizen/dash-buttons'
import Smartboard from './smartboard/'
import ButtonsAdmin from './buttons-admin'
import Admin from './admin'
import Exams from './exams/exams'
import ButtonsExams from './exams/buttons-exams'
import Agenda from './agenda/agenda'
import ButtonsAgenda from './agenda/buttons-agenda'
import Calendar from './booking/calendar'
import ButtonsCalendar from './booking/buttons-calendar'
import Appointments from './appointments/appointments'
import ButtonsAppointments from './appointments/buttons-appointments'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: App,
      redirect: '/queue',
      children: [
        {
          path: 'queue',
          components: {
            default: Dash,
            buttons: ButtonsDash,
          },
        },
        {
          path: 'admin',
          components: {
            default: Admin,
            buttons: ButtonsAdmin
          }
        },
        {
          path: 'exams',
          components: {
            default: Exams,
            buttons: ButtonsExams
          }
        },
        {
          path: 'agenda',
          components: {
            default: Agenda,
            buttons: ButtonsAgenda,
          }
        },
        {
          path: 'appointments',
          components: {
            default: Appointments,
            buttons: ButtonsAppointments,
          }
        },
        {
          path: 'booking',
          components: {
            default: Calendar,
            buttons: ButtonsCalendar,
          }
        },
      ]
    },
    {
      path:'/smartboard/:office_number',
      component: Smartboard,
      props: true,
    },
    {
      path:'/smartboard/',
      component: Smartboard,
    },
  ]
})
