
<template>
  <fragment>
    <v-app>
      <div class="v-application">
        <div style="width: 100%" class="m-3">
          <!-- <v-card class="mx-auto" max-width="97%" elevation="5"> -->
          <div
            style="padding: 0; margin-top: auto; margin-left: 20px"
            class="mb-2"
          >
            <b-form inline>
              <label class="mr-2">
                Filter Appointments
                <font-awesome-icon
                  icon="filter"
                  class="m-0 p-0"
                  style="font-size: 1rem"
                />
              </label>
              <b-form-input
                v-model="searchTerm"
                size="sm"
                @input="filter"
              ></b-form-input>
            </b-form>
          </div>
          <v-sheet>
            <AppointmentsFilter :events="events" v-if="listView" />
            <!-- interval-height="24" -->
            <v-calendar
              v-else
              ref="calendar"
              color="primary"
              :now="currentDay"
              v-model="value"
              interval-height="40"
              first-time="08:30"
              interval-minutes="30"
              interval-count="17"
              :weekdays="weekday"
              :type="type"
              :events="events"
              :event-overlap-mode="mode"
              :event-overlap-threshold="30"
              :event-color="getEventColor"
              @click:event="eventSelected"
              @click:more="agendaDay"
              @change="getEvents"
              @click:time="selectEvent"
              event-text-color=""
              @click:date="switchView"
              id="appointment-calendar"
            >
              <template v-slot:event="date">
                <v-tooltip bottom class="mytooltip" v-bind:fixed="false" v-bind:nudge-top="150">
                  <template v-slot:activator="{ on }">
                    <div v-on="on" class="ml-2">
                      {{ date.event.title }} {{ date.eventParsed.start.time }} -
                      {{ date.eventParsed.end.time }}
                    </div>
                  </template>
                  <div>
                    <div>
                      {{ date.event.title }}
                      {{ date.eventParsed.start.time }} -
                      {{ date.eventParsed.end.time }}
                      <div>Service Name: {{ date.event.serviceName }}</div>
                      <div class="notes" v-if="date.event.comments !== null">
                        Notes: {{ date.event.comments }}
                      </div>
                    </div>
                  </div>
                </v-tooltip>
              </template>
            </v-calendar>
            <!-- @mouseenter:event="showData" -->
          </v-sheet>
          <!-- </v-card> -->
        </div>
      </div>
      <ApptBookingModal :clickedTime="clickedTime" :clickedAppt="clickedAppt" />
      <AppointmentBlackoutModal />
      <CheckInModal :clickedAppt="clickedAppt" />
    </v-app>
  </fragment>
</template>

<script lang="ts">
/* eslint-disable sort-imports */

import { Component, Vue } from 'vue-property-decorator'

import AddCitizen from '../AddCitizen/add-citizen.vue'

import AppointmentBlackoutModal from './appt-booking-modal/appt-blackout-modal.vue'

import ApptBookingModal from './appt-booking-modal/appt-booking-modal.vue'

import CheckInModal from './checkin-modal.vue'
import AppointmentsFilter from './appointmentsFilter.vue'

import moment from 'moment'

import { namespace } from 'vuex-class'
import { formatedStartTime } from '@/utils/helpers'

const appointmentsModule = namespace('appointmentsModule')

@Component({
  components: {
    AppointmentBlackoutModal,
    AddCitizen,
    CheckInModal,
    ApptBookingModal,
    AppointmentsFilter
  }
})
export default class Appointments extends Vue {
  public $refs: any = {
    appointments: HTMLElement
  };

  @appointmentsModule.State('apptRescheduling') private apptRescheduling!: any

  @appointmentsModule.Getter('calendar_setup') private calendar_setup!: any;
  @appointmentsModule.Getter('appointment_events') private appointment_events!: any;
  @appointmentsModule.Getter('filtered_appointment_events') private filtered_appointment_events!: any;

  @appointmentsModule.Action('getAppointments') public getAppointments: any
  @appointmentsModule.Action('getChannels') public getChannels: any
  @appointmentsModule.Action('getServices') public getServices: any

  @appointmentsModule.Action('postDraftAppointment') public postDraftAppointment: any
  @appointmentsModule.Action('deleteDraftAppointment') public deleteDraftAppointment: any

  @appointmentsModule.Mutation('setCalendarSetup') public setCalendarSetup: any
  @appointmentsModule.Mutation('setEditedStatus') public setEditedStatus: any
  @appointmentsModule.Mutation('toggleApptBookingModal') public toggleApptBookingModal: any
  @appointmentsModule.Mutation('toggleCheckInModal') public toggleCheckInModal: any
  @appointmentsModule.Mutation('setRescheduling') public setRescheduling: any

  // vuetify calender
  listView: any = false
  searchTerm: string = ''
  type: any = 'week'
  // types: any = ['month', 'week', 'day', '4day']
  mode: any = 'stack'
  // modes: any = ['stack', 'column']
  weekday: any = [1, 2, 3, 4, 5]

  value: any = ''
  // events: any = []
  currentDay: any = moment().format('YYYY-MM-DD')// new Date()

  get events () {
    if (this.searchTerm) {
      return this.filtered_appointment_events(this.searchTerm)
    }

    return this.appointment_events
  }

  // to remove
  getEvents ({ start, end }) {
    return this.appointment_events
  }

  getEventColor (event) {
    return event.color
  }

  rnd (a, b) {
    return Math.floor((b - a + 1) * Math.random()) + a
  }

  switchView ({ date }) {
    this.value = date
    if (this.type === 'day') {
      this.type = 'week'
    } else {
      this.type = 'day'
    }
    this.calendarSetup()
  }

  // vuetify calender end

  public blockEventSelect: any = false
  public clickedAppt: any = null
  public clickedTime: any = null

  agendaDay () {
    this.type = 'day'
    this.calendarSetup()
  }

  agendaWeek () {
    this.type = 'week'
    this.calendarSetup()
  }

  eventRender (event, el, view) {
    return null
  }

  eventSelected ({ nativeEvent, event }) {
    this.checkRescheduleCancel()
    if ((this.apptRescheduling && this.$store.state.rescheduling) || event.id === '_tempEvent') {
      return
    }
    let clickedEvent = event
    clickedEvent = { ...clickedEvent, ...{ start: moment(event.start) }, ...{ end: moment(event.end) } }
    this.clickedAppt = clickedEvent
    this.highlightEvent(clickedEvent)
    this.toggleCheckInModal(true)
    nativeEvent.stopPropagation()
  }

  // goToDate (date) {
  //   this.$refs.appointments.fireMethod('gotoDate', date)
  //   this.calendarSetup()
  // }
  goToDate (date) {
    if (date) {
      this.listView = false
      this.type = 'day'
      // this.categoryDays = 1
      this.value = new Date(date)
    }
    this.calendarSetup()
  }

  month () {
    this.type = 'month'
    this.calendarSetup()
  }

  next () {
    this.$refs.calendar.next()
    this.calendarSetup()
  }

  options (option) {
    this.$refs.appointments.fireMethod('option', option.name, option.value)
  }

  prev () {
    this.$refs.calendar.prev()
    this.calendarSetup()
  }

  // renderEvent (event) {
  //   this.$refs.appointments.fireMethod('renderEvent', event)
  // }

  checkRescheduleCancel () {
    if (this.$store.state.apptRescheduleCancel) {
      this.removeTempEvent()
      this.clearClickedTime()
      this.clearClickedAppt()
      this.setRescheduling(false)
      this.toggleApptBookingModal(false)
      this.$store.commit('toggleApptRescheduleCancel', false)
    }
  }

  filter (event) {
    if (event) {
      this.listView = true
    } else {
      this.listView = false
      this.calendarSetup()
    }
  }

  selectEvent (event) {
    this.checkRescheduleCancel()
    this.blockEventSelect = true
    // this.unselect()

    const start = formatedStartTime(event.date, event.time)// event.start.clone()
    let end
    for (const l of [15, 30, 45, 60]) {
      const testEnd = moment(start).clone().add(l, 'minutes')
      if (this.appointment_events.find(event => moment(event.start).isBetween(start, testEnd))) {
        break
      }
      end = testEnd
    }
    const e = {
      start,
      end,
      title: event.title
    }
    this.clickedTime = e
    this.setTempEvent(e)
    this.toggleApptBookingModal(true)
    this.blockEventSelect = false
  }

  clearClickedAppt () {
    this.clickedAppt = null
  }

  clearClickedTime () {
    this.clickedTime = null
  }

  today () {
    this.value = ''
    this.calendarSetup()
  }

  removeTempEvent () {
    this.deleteDraftAppointment().then((resp) => {

      // this.getAppointments().then(() => {
      //   // finish()
      //   // this.$store.commit('toggleServeCitizenSpinner', false)
      //   // setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
      // })
    })

    // this.$refs.appointments.fireMethod('removeEvents', ['_tempEvent'])
  }

  highlightEvent (event) {
    const e = event
    e.color = 'pink'
    // this.$refs.appointments.fireMethod('updateEvent', e)
  }

  setTempEvent (event) {
    this.removeTempEvent()
    // const start = moment(event.start).clone()
    const start = moment(event.start).clone()
    const end = moment(event.end).clone()
    const e: any = {
      start,
      end,
      title: 'Unconfirmed Booking',
      color: 'pink',
      id: '_tempEvent'
    }

    // for draft
    const data: any = {
      start_time: moment.utc(start).format(),
      // setting end time aftger 15 min of start to fix over appoinment time
      end_time: moment(start).clone().add(15, 'minutes')// moment.utc(end).format()
      // service_id: 27,
      // is_draft: true
    }

    // this.postDraftAppointment(data)
    this.postDraftAppointment(data).then((resp) => {
      // this.getAppointments().then(() => {
      //   // finish()
      //   // this.$store.commit('toggleServeCitizenSpinner', false)
      //   // setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
      // })
    })
  }

  unselect () {
    this.$refs.appointments.fireMethod('unselect')
  }

  // viewRender (view, el) {
  //   let { title, name } = view
  //   title = `The Q Appointments: ${title}`
  //   if (view.name === 'agendaDay') {
  //     title = moment(view.intervalStart).format('dddd MMMM D, YYYY')
  //   }
  //   this.setCalendarSetup({ title, name })
  // }

  calendarSetup () {
    const title = 'Appointments:'
    const name = this.type
    this.setCalendarSetup({ title, name, titleRef: this.$refs.calendar })
  }

  mounted () {
    this.getAppointments()
    this.getServices()
    this.getChannels()

    this.$root.$on('clear-clicked-appt', () => { this.clearClickedAppt() })
    this.$root.$on('clear-clicked-time', () => { this.clearClickedTime() })
    this.$root.$on('agendaDay', () => { this.agendaDay() })
    this.$root.$on('agendaWeek', () => { this.agendaWeek() })
    this.$root.$on('month', () => { this.month() })
    this.$root.$on('next', () => { this.next() })
    this.$root.$on('options', (option) => { this.options(option) })
    this.$root.$on('prev', () => { this.prev() })
    this.$root.$on('today', () => { this.today() })
    this.$root.$on('removeTempEvent', () => { this.removeTempEvent() })
    this.$root.$on('goToDate', (date) => { this.goToDate(date) })
    this.calendarSetup()
  }
}

</script>

<style scoped>
.btn {
  border: none !important;
}
.label-text {
  font-size: 0.9rem;
}
.btn {
  border: none !important;
  box-shadow: none !important;
  transition: none !important;
}
.btn:active,
.btn.active {
  background-color: whitesmoke !important;
  color: darkgrey !important;
}
.exam-table-holder {
  border: 1px solid dimgrey;
}
</style>
<style >
.v-calendar .v-event-timed-container {
  margin-right: 20px !important;
}
/* .theme--light.v-calendar-events .v-event-timed {
  border: none !important;
} */
.v-tooltip--attached {
  display: block;
  position: fixed;
  z-index: 100;
}
.notes {
  white-space: pre-wrap;
}
tr.fc-list-item {
  border-top: 1px solid gray;
  border-bottom: 1px solid gray;
}
</style>
