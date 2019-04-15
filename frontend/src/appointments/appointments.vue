<template>
  <fragment>
    <ApptBookingModal :clickedTime="clickedTime" :clickedAppt="clickedAppt"/>
    <CheckInModal :clickedAppt="clickedAppt" />
    <keep-alive>
      <full-calendar ref="appointments"
                     key="appointments"
                     id="appointments"
                     class="q-calendar-margins"
                     @event-selected="eventSelected"
                     @view-render="viewRender"
                     @event-created="selectEvent"
                     @event-render="eventRender"
                     :events="appointment_events"
                     :config="config">
      </full-calendar>
    </keep-alive>
  </fragment>
</template>

<script>
  import moment from 'moment'
  import { createNamespacedHelpers } from 'vuex'
  import { FullCalendar } from 'vue-full-calendar'
  import { adjustColor } from '../store/helpers'
  import 'fullcalendar-scheduler'
  import 'fullcalendar/dist/fullcalendar.css'
  import ApptBookingModal from './appt-booking-modal/appt-booking-modal'
  import { store } from '../store/'
  import CheckInModal from './checkin-modal'
  import AddCitizen from '../add-citizen/add-citizen'

  const { mapActions, mapGetters, mapMutations, mapState } = createNamespacedHelpers('appointmentsModule')

  export default {
    name: 'Appointments',
    components: {
      AddCitizen,
      CheckInModal,
      ApptBookingModal,
      FullCalendar,
    },
    mounted() {
      this.getAppointments()
      this.getServices()
      this.getChannels()
      this.$root.$on('clearappt', () =>  { this.clearAppt() })
      this.$root.$on('cleardate', () =>  { this.clearDate() })
      this.$root.$on('agendaDay', () => { this.agendaDay() })
      this.$root.$on('agendaWeek', () => { this.agendaWeek() })
      this.$root.$on('month', () => { this.month() })
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('options', (option) => { this.options(option) })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('today', () => { this.today() })
      this.$root.$on('removeTempEvent', () => { this.removeTempEvent() })
    },
    data() {
      return {
        clickedAppt: null,
        clickedTime: null,
        config: {
          columnHeaderFormat: 'ddd/D',
          selectAllow: () => {
            return true
          },
          defaultView: 'agendaWeek',
          editable: false,
          eventRender: (evt, el, view) => {
            el.css('font-size', '.9rem')
          },
          eventColor: 'pink',
          eventConstraint: {
            start: '09:00:00',
            end: '17:00:00',
          },
          fixedWeekCount: false,
          header: {
            left: null,
            center: null,
            right: null
          },
          height: 'auto',
          maxTime: '17:00:00',
          minTime: '09:00:00',
          navLinks: false,
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          selectConstraint: {
            start: '08:00:00',
            end: '18:00:00',
          },
          showNonCurrentDates: false,
          slotDuration: '00:15:00',
          slotLabelInterval: '00:30:00',
          slotLabelFormat: 'h:mm',
          timezone: 'local',
          unselectCancel: '.modal, .modal-content',
          views: {
            agendaDay: {
              allDaySlot: false,
            },
            agendaWeek: {
              allDaySlot: false,
            },
          },
          weekends: false,
        },
      }
    },
    computed: {
      ...mapGetters(['calendar_setup', 'appointment_events']),
      ...mapState([]),
    },
    methods: {
      ...mapActions(['getAppointments', 'getChannels', 'getServices']),
      ...mapMutations([
        'setCalendarSetup',
        'setEditedStatus',
        'setRescheduling',
        'toggleApptBookingModal',
        'toggleCheckInModal',
      ]),
      agendaDay() {
        this.$refs.appointments.fireMethod('changeView', 'agendaDay')
      },
      agendaWeek() {
        this.$refs.appointments.fireMethod('changeView', 'agendaWeek')
      },
      eventRender(event, el, view) {
        return null
      },
      events() {
        return null
      },
      eventSelected(event, jsEvent, view) {
        this.clickedAppt = event
        this.highlightEvent(event)
        this.toggleCheckInModal(true)
      },
      goToDate(date) {
        this.$refs.appointments.fireMethod('gotoDate', date)
      },
      month() {
        this.$refs.appointments.fireMethod('changeView', 'month')
      },
      next() {
        this.$refs.appointments.fireMethod('next')
      },
      options(option) {
        this.$refs.appointments.fireMethod('option', option.name, option.value)
      },
      prev() {
        this.$refs.appointments.fireMethod('prev')
      },
      renderEvent(event) {
        this.$refs.appointments.fireMethod('renderEvent', event)
      },
      selectEvent(event) {
        this.unselect()
        let start = event.start.clone()
        let end = event.start.clone().add(15, 'minutes')
        let e = {
          start,
          end,
          title: event.title,
        }
        this.clickedTime = e
        this.setTempEvent(e)
        this.toggleApptBookingModal(true)
      },
      clearAppt() {
        this.clickedAppt = null
      },
      clearDate() {
        this.clickedDate = null
      },
      today() {
        this.$refs.appointments.fireMethod('today')
      },
      removeTempEvent() {
        this.$refs.appointments.fireMethod('removeEvents', ['_tempEvent'])
      },
      highlightEvent(event) {
        let e = event
        e.color = 'pink'
        this.$refs.appointments.fireMethod('updateEvent', e)
      },
      setTempEvent(event) {
        this.removeTempEvent()
        let start = event.start.clone()
        let end = event.end.clone()
        let e = {
          start,
          end,
          title: 'Unconfirmed Booking',
          color: 'pink',
          id: '_tempEvent',
        }
        this.$refs.appointments.fireMethod('renderEvent', e)
      },
      unselect() {
        this.$refs.appointments.fireMethod('unselect')
      },
      viewRender(view, el) {
        let { title, name } = view
        title = `The Q Appointments: ${title}`
        if (view.name === 'agendaDay') {
          title = moment(view.intervalStart).format('dddd MMMM D, YYYY')
        }
        this.setCalendarSetup({ title, name })
      },
    },
  }

</script>

<style scoped>
  .btn {
    border: none !important;
  }
  .label-text {
    font-size: .9rem;
  }
  .btn {
    border: none !important;
    box-shadow: none !important;
    transition: none !important;
  }
  .btn:active, .btn.active {
    background-color: whitesmoke  !important;
    color: darkgrey !important;
  }
  .exam-table-holder {
    border: 1px solid dimgrey;
  }
</style>
