<template>
  <fragment>
    <div>
      <v-sheet tile height="54" class="d-flex">
        <v-btn icon class="ma-2" @click="$refs.calendar.prev()">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>

        <v-spacer></v-spacer>
        <v-btn icon class="ma-2" @click="$refs.calendar.next()">
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-sheet>
      <v-sheet height="600">
        <!-- {{ events }} -->
        <keep-alive>
          <v-calendar
            ref="calendar"
            v-model="value"
            first-time="08:30"
            interval-minutes="30"
            :weekdays="weekday"
            :type="type"
            :events="appointment_events"
            :event-overlap-mode="mode"
            :event-overlap-threshold="30"
            :event-color="getEventColor"
            @click:event="eventSelected"
            @click:more="eventSelected"
            @change="getEvents"
            @click:time="selectEvent"
          ></v-calendar>
          <!-- @click:event="showEvent"
            @click:more="viewDay"
            @click:date="viewDay"
            @change="updateRange"
            @click:time="test" -->
          <!-- @change="getEvents" -->
        </keep-alive>
      </v-sheet>
    </div>

    <!-- {{ appointment_events }} -->
    <ApptBookingModal :clickedTime="clickedTime" :clickedAppt="clickedAppt" />
    <AppointmentBlackoutModal />
    <CheckInModal :clickedAppt="clickedAppt" />
    <!-- <keep-alive>
      <full-calendar
        ref="appointments"
        key="appointments"
        id="appointments"
        class="q-calendar-margins"
        @event-selected="eventSelected"
        @view-render="viewRender"
        @event-created="selectEvent"
        @event-render="eventRender"
        :events="appointment_events"
        :config="config"
      ></full-calendar>
    </keep-alive> -->
  </fragment>
</template>

<script lang="ts">

import 'fullcalendar-scheduler'
import 'fullcalendar/dist/fullcalendar.css'
import { Component, Vue } from 'vue-property-decorator'
import AddCitizen from '../AddCitizen/add-citizen.vue'

import AppointmentBlackoutModal from './appt-booking-modal/appt-blackout-modal.vue'
import ApptBookingModal from './appt-booking-modal/appt-booking-modal.vue'
import CheckInModal from './checkin-modal.vue'

import { FullCalendar } from 'vue-full-calendar'
import moment from 'moment'
import { namespace } from 'vuex-class'

const appointmentsModule = namespace('appointmentsModule')

@Component({
  components: {
    AppointmentBlackoutModal,
    AddCitizen,
    CheckInModal,
    ApptBookingModal,
    FullCalendar
  }
})
export default class Appointments extends Vue {
  public $refs: any = {
    appointments: HTMLElement
  };

  @appointmentsModule.State('apptRescheduling') private apptRescheduling!: any

  @appointmentsModule.Getter('calendar_setup') private calendar_setup!: any;
  @appointmentsModule.Getter('appointment_events') private appointment_events!: any;

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

  type: any = 'week'
  types: any = ['month', 'week', 'day', '4day']
  mode: any = 'stack'
  modes: any = ['stack', 'column']
  weekday: any = [1, 2, 3, 4, 5]
  weekdays: any = [
    { text: 'Sun - Sat', value: [0, 1, 2, 3, 4, 5, 6] },
    { text: 'Mon - Sun', value: [1, 2, 3, 4, 5, 6, 0] },
    { text: 'Mon - Fri', value: [1, 2, 3, 4, 5] },
    { text: 'Mon, Wed, Fri', value: [1, 3, 5] }
  ]

  value: any = ''
  events: any = []

  colors: any = ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1']
  names: any = ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party']

  getEvents ({ start, end }) {
    const events: any = []

    const min = new Date(`${start.date}T00:00:00`)
    const max = new Date(`${end.date}T23:59:59`)
    const days = (max.getTime() - min.getTime()) / 86400000
    const eventCount = this.rnd(days, days + 20)

    for (let i = 0; i < eventCount; i++) {
      const allDay = this.rnd(0, 3) === 0
      const firstTimestamp = this.rnd(min.getTime(), max.getTime())
      const first = new Date(firstTimestamp - (firstTimestamp % 900000))
      const secondTimestamp = this.rnd(2, allDay ? 288 : 8) * 900000
      const second = new Date(first.getTime() + secondTimestamp)

      events.push({
        name: this.names[this.rnd(0, this.names.length - 1)],
        start: first,
        end: second,
        color: this.colors[this.rnd(0, this.colors.length - 1)],
        timed: !allDay
      })
    }

    this.events = events
    // [
    //   {
    //     name: 'Meeting',
    //     start: new Date('2020-11-18T19:15:00.000Z'),
    //     end: new Date('2020-11-18T20:15:00.000Z'),
    //     color: 'green',
    //     timed: true
    //   },
    //   {
    //     name: 'PTO',
    //     start: new Date('2020-11-19T17:45:00.000Z'),
    //     end: new Date('2020-11-19T18:30:00.000Z'),
    //     color: 'orange',
    //     timed: true
    //   },
    //   {
    //     name: 'PTO',
    //     start: new Date('2020-11-19T04:30:00.000Z'),
    //     end: new Date('2020-11-19T06:00:00.000Z'),
    //     color: 'green',
    //     timed: true
    //   },
    //   {
    //     name: 'Travel',
    //     start: new Date('2020-11-17T11:15:00.000Z'),
    //     end: new Date('2020-11-17T13:00:00.000Z'),
    //     color: 'cyan',
    //     timed: true
    //   }
    // ]
  }

  getEventColor (event) {
    return event.color
  }

  rnd (a, b) {
    return Math.floor((b - a + 1) * Math.random()) + a
  }

  // vuetify calender end
  public blockEventSelect: any = false
  public clickedAppt: any = null
  public clickedTime: any = null
  public config: any = {
    selectOverlap: true,
    columnHeaderFormat: 'ddd/D',
    selectAllow: () => {
      return true
    },
    defaultView: 'agendaWeek',
    editable: false,
    eventRender: (evt, el, view) => {
      if (evt.blackout_flag === 'Y') {
        el.css('font-size', '.9rem')
        el.css('max-width', '100%')
        el.css('background-color', '#000000')
        el.css('border-color', '#000000')
        el.css('color', 'white')
      } else if (evt.is_draft === true) {
        el.css('font-size', '.9rem')
        el.css('max-width', '85%')
        el.css('background-color', 'lightgray')
        el.css('border-color', 'darkgray')
        el.css('color', 'black')
      } else {
        el.css('font-size', '.9rem')
        el.css('max-width', '85%')
        el.css('background-color', '#EFD469')
        el.css('border-color', '#EFD469')
        el.css('color', 'black')
      }
    },
    eventColor: 'pink',
    eventConstraint: {
      start: '08:30:00',
      end: '17:00:00'
    },
    fixedWeekCount: false,
    header: {
      left: null,
      center: null,
      right: null
    },
    height: 'auto',
    maxTime: '17:00:00',
    minTime: '08:30:00',
    navLinks: false,
    schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
    selectConstraint: {
      start: '08:30:00',
      end: '17:00:00'
    },
    showNonCurrentDates: false,
    slotDuration: '00:15:00',
    slotLabelInterval: '00:30:00',
    slotLabelFormat: 'h:mm',
    timezone: 'local',
    unselectCancel: '.modal, .modal-content',
    views: {
      agendaDay: {
        allDaySlot: false
      },
      agendaWeek: {
        allDaySlot: false
      }
    },
    weekends: false
  }

  agendaDay () {
    // this.$refs.appointments.fireMethod('changeView', 'agendaDay')
    this.type = 'day'
  }

  agendaWeek () {
    this.type = 'week'
    // this.$refs.appointments.fireMethod('changeView', 'agendaWeek')
  }

  eventRender (event, el, view) {
    return null
  }

  // events () {
  //   return null
  // }

  eventSelected ({ nativeEvent, event }) {
    this.checkRescheduleCancel()
    if ((this.apptRescheduling && this.$store.state.rescheduling) || event.id === '_tempEvent') {
      return
    }

    console.log('event', event)
    let clickedEvent = event
    clickedEvent = { ...clickedEvent, ...{ start: moment(event.start) }, ...{ end: moment(event.end) } }
    console.log('clickedEvent', clickedEvent)
    this.clickedAppt = clickedEvent
    this.highlightEvent(clickedEvent)
    this.toggleCheckInModal(true)
    nativeEvent.stopPropagation()
  }

  goToDate (date) {
    this.$refs.appointments.fireMethod('gotoDate', date)
  }

  month () {
    // this.$refs.appointments.fireMethod('changeView', 'month')
    this.type = 'month'
  }

  next () {
    this.$refs.calendar.next()
    // this.$refs.appointments.fireMethod('next')
  }

  options (option) {
    this.$refs.appointments.fireMethod('option', option.name, option.value)
  }

  prev () {
    this.$refs.calendar.prev()
    // this.$refs.appointments.fireMethod('prev')
  }

  renderEvent (event) {
    this.$refs.appointments.fireMethod('renderEvent', event)
  }

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

  selectEvent (event) {
    this.checkRescheduleCancel()
    this.blockEventSelect = true
    // this.unselect()
    console.log('event', event)
    const start = moment(`${event.date} ${event.time}`)// event.start.clone()
    console.log('start', start)
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

    // this.$refs.appointments.fireMethod('today')
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
    this.$refs.appointments.fireMethod('updateEvent', e)
  }

  setTempEvent (event) {
    this.removeTempEvent()
    // const start = moment(event.start).clone()
    const start = moment(event.start).clone()
    const end = moment(event.end).clone()
    const e = {
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
    console.log('data', data)
    // this.postDraftAppointment(data)
    this.postDraftAppointment(data).then((resp) => {
      // this.getAppointments().then(() => {
      //   // finish()
      //   // this.$store.commit('toggleServeCitizenSpinner', false)
      //   // setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
      // })
    })
    // this.$refs.appointments.fireMethod('renderEvent', e)
  }

  unselect () {
    this.$refs.appointments.fireMethod('unselect')
  }

  viewRender (view, el) {
    let { title, name } = view
    title = `The Q Appointments: ${title}`
    if (view.name === 'agendaDay') {
      title = moment(view.intervalStart).format('dddd MMMM D, YYYY')
    }
    this.setCalendarSetup({ title, name })
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
