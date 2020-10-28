<template>
  <fragment>
    <ApptBookingModal :clickedTime="clickedTime" :clickedAppt="clickedAppt" />
    <AppointmentBlackoutModal />
    <CheckInModal :clickedAppt="clickedAppt" />
    <keep-alive>
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
    </keep-alive>
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
    this.$refs.appointments.fireMethod('changeView', 'agendaDay')
  }

  agendaWeek () {
    this.$refs.appointments.fireMethod('changeView', 'agendaWeek')
  }

  eventRender (event, el, view) {
    return null
  }

  events () {
    return null
  }

  eventSelected (event) {
    this.checkRescheduleCancel()
    if ((this.apptRescheduling && this.$store.state.rescheduling) || event.id === '_tempEvent') {
      return
    }
    console.log('==> In eventSelected')
    console.log(event)
    this.clickedAppt = event
    this.highlightEvent(event)
    this.toggleCheckInModal(true)
  }

  goToDate (date) {
    this.$refs.appointments.fireMethod('gotoDate', date)
  }

  month () {
    this.$refs.appointments.fireMethod('changeView', 'month')
  }

  next () {
    this.$refs.appointments.fireMethod('next')
  }

  options (option) {
    this.$refs.appointments.fireMethod('option', option.name, option.value)
  }

  prev () {
    this.$refs.appointments.fireMethod('prev')
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
    this.unselect()
    const start = event.start.clone()
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
    this.$refs.appointments.fireMethod('today')
  }

  removeTempEvent () {
    this.deleteDraftAppointment().then((resp) => {

      // this.getAppointments().then(() => {
      //   // finish()
      //   // this.$store.commit('toggleServeCitizenSpinner', false)
      //   // setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
      // })
    })

    this.$refs.appointments.fireMethod('removeEvents', ['_tempEvent'])
  }

  highlightEvent (event) {
    const e = event
    e.color = 'pink'
    this.$refs.appointments.fireMethod('updateEvent', e)
  }

  setTempEvent (event) {
    this.removeTempEvent()
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
    // this.postDraftAppointment(data)
    this.postDraftAppointment(data).then((resp) => {
      // this.getAppointments().then(() => {
      //   // finish()
      //   // this.$store.commit('toggleServeCitizenSpinner', false)
      //   // setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
      // })
    })
    this.$refs.appointments.fireMethod('renderEvent', e)
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
