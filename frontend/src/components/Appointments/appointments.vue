
<template>
    <v-app>
      <div class="v-application">
        <div style="width: 100%" class="m-3">
          <div
            style="padding: 0; margin-top: auto; margin-left: 20px"
            class="mb-2"
          >
            <b-form inline @submit.stop.prevent>
              <label class="mr-2">
                Filter Appointments
                <font-awesome-icon
                  icon="filter"
                  class="m-0 p-0"
                  style="font-size: 1rem"
                />
              </label>
                <b-input-group>
                  <b-form-input
                    v-model="searchTerm"
                    size="sm"
                    @input="filter"
                  ></b-form-input>
                  <b-input-group-append v-if='searchTerm.length'>
                    <b-button size='sm' variant="danger" @click='clearSearch'>Clear</b-button>
                  </b-input-group-append>
                </b-input-group>
            </b-form>
          </div>
          <v-sheet>
            <AppointmentsFilter :events="events" v-if="listView" />
            <v-calendar
              v-else
              ref="calendar"
              color="primary"
              :now="currentDay"
              v-model="value"
              interval-height="20"
              first-time="08:30"
              interval-minutes="15"
              interval-count="34"
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
              :interval-style = "intervalStyle"
              :show-interval-label="showIntervalLabel"
            >
              <template v-slot:event="date">
                <v-tooltip bottom class="mytooltip" v-bind:fixed="false" v-bind:nudge-top="150">
                  <template v-slot:activator="{ on }">
                    <div v-on="on" class="ml-2">
                      <span v-if="date.eventParsed.input.stat_flag && date.eventParsed.input.comments">
                        {{ date.eventParsed.input.comments }} {{ date.eventParsed.start.time }} -
                        {{ date.eventParsed.end.time }}
                      </span>
                      <span v-else>
                        {{ date.event.title }} {{ date.eventParsed.start.time }} -
                        {{ date.eventParsed.end.time }}
                      </span>
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
          </v-sheet>
        </div>
      </div>
      <ApptBookingModal v-if="!is_stat" :clickedTime="clickedTime" :clickedAppt="clickedAppt" />
      <AppointmentBlackoutModal />
      <CheckInModal :clickedAppt="clickedAppt" />
      <LoadingModal v-if="show_loading" />
    </v-app>
</template>

<script lang="ts">
/* eslint-disable */
// /* eslint-disable sort-imports */
import { Component, Vue } from 'vue-property-decorator'

import AddCitizen from '../AddCitizen/add-citizen.vue'

import AppointmentBlackoutModal from './appt-booking-modal/appt-blackout-modal.vue'

import ApptBookingModal from './appt-booking-modal/appt-booking-modal.vue'

import LoadingModal from './appt-booking-modal/loading.vue'

import CheckInModal from './checkin-modal.vue'
import AppointmentsFilter from './appointmentsFilter.vue'

import moment from 'moment'

import { namespace } from 'vuex-class'
import { formatedStartTime } from '@/utils/helpers'
import { showFlagBus, ShowFlagBusEvents } from '../../events/showFlagBus'

const appointmentsModule = namespace('appointmentsModule')

// For MOMENT, not the calendar
const SATURDAY = 6
const SUNDAY = 1

@Component({
  components: {
    AppointmentBlackoutModal,
    AddCitizen,
    CheckInModal,
    ApptBookingModal,
    AppointmentsFilter,
    LoadingModal
  }
})
export default class Appointments extends Vue {
  public $refs: any = {
    appointments: HTMLElement
  };

  @appointmentsModule.State('apptRescheduling') private apptRescheduling!: any

  @appointmentsModule.Getter('calendar_setup') private calendar_setup!: any
  @appointmentsModule.Getter('appointment_events') private appointment_events!: any
  @appointmentsModule.Getter('filtered_appointment_events') private filtered_appointment_events!: any

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

  @appointmentsModule.State('clickedAppt') public clickedAppt: any
  @appointmentsModule.Mutation('setAgendaClickedAppt') public setAgendaClickedAppt: any

  @appointmentsModule.State('clickedTime') public clickedTime: any
  @appointmentsModule.Mutation('setAgendaClickedTime') public setAgendaClickedTime: any
  @appointmentsModule.Mutation('setToggleAppCalenderView') public setToggleAppCalenderView: any

  show_loading = false
  // vuetify calender
  listView: any = false
  searchTerm: string = ''
  type: any = 'week'
  mode: any = 'stack'
  weekday: any = [1, 2, 3, 4, 5]

  value: any = ''
  currentDay: any = moment().format('YYYY-MM-DD')// new Date()

  is_stat: boolean = false
  _keyListenerNewApp: any = null
  _keyListenerWeek: any = null
  _keyListenerDay: any = null

  get events () {
    if (this.searchTerm) {
      return this.filtered_appointment_events(this.searchTerm)
    }
    return this.appointment_events
  }

  clearSearch() {
    this.searchTerm = ''
    this.filter(false)
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
      this.setToggleAppCalenderView(false)
      this.type = 'week'
    } else {
      this.setToggleAppCalenderView(true)
      this.type = 'day'
    }
    this.calendarSetup()
  }

  // vuetify calender end

  public blockEventSelect: any = false

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
    this.setAgendaClickedAppt(clickedEvent)
    this.highlightEvent(clickedEvent)
    this.toggleCheckInModal(true)
    nativeEvent.stopPropagation()
  }

  goToDate (date) {
    if (date) {
      this.listView = false
      this.type = 'day'
      this.value = new Date(date)
    }
    this.calendarSetup()
  }

  month () {
    this.type = 'month'
    this.calendarSetup()
  }


  // If  working on  localhost and you get "TypeError: Cannot read property 'next' of undefined"
  // Just restart `npm run serve`, as it glitches out.
  next () {
    const daysToMove = this.getDaysToMove('next')
    if (this.$refs.calendar) {
      this.$refs.calendar.move(daysToMove)
    }
    this.calendarSetup()
  }

  options (option) {
    this.$refs.appointments.fireMethod('option', option.name, option.value)
  }

  prev () {
    const daysToMove = this.getDaysToMove('prev')
    if (this.$refs.calendar) {
      this.$refs.calendar.move(daysToMove)
    }
    this.calendarSetup()
  }

  /**
   * This function helps skipping weekends on day views
   * Returns the # of days to move to skip the weekend
   * used with `this.$refs.calendar.move()`
   */
  getDaysToMove(direction: 'next' | 'prev'): number {
    if (this.type  !== 'day') {
      // Just move one week forward/back, simple.
      return direction === 'next' ? 1 : -1
    } else {
      if (this.$refs.calendar) {
      // For days, we have to handle jumping of weekends.
      const viewedDate = this.$refs.calendar.value
      const dayOfWeek = moment(viewedDate).day()
      let daysToMove = 1
      if (direction === 'next') {    
        if ((dayOfWeek + 1) === SATURDAY ) {
          daysToMove = 3
        }
      } else if (direction === 'prev') {
        daysToMove = -1
        if ((dayOfWeek) === SUNDAY ) {
          // Value must be negative for prev
          daysToMove = -3
        }
      }
      return daysToMove
      }
      return 1
    }
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

  filter (event) {
    if (event) {
      this.listView = true
    } else {
      this.listView = false
      this.calendarSetup()
    }
  }

  selectEvent (event) {
    const eventDate = moment(event.date + " " + event.time);
    if (eventDate < moment(moment.now())) {
      return
    }
    this.is_stat = false
    this.getAppointments().then((each) => {
      const bb = each.find(element => ((moment(event.date).format('YYYY-MM-DD') === moment(element.start_time).format('YYYY-MM-DD')) && (element.stat_flag)));
      if (bb) {
        this.is_stat = true
      }
    })
    this.checkRescheduleCancel()
    this.blockEventSelect = true
    const start = formatedStartTime(event.date, event.time)
    let end
    for (const l of [15, 30, 45, 60]) {
      const testEnd = moment(start).clone().add(l, 'minutes')
      if (this.appointment_events.find(apptEvent => moment(apptEvent.start).isBetween(start, testEnd))) {
        break
      }
      end = testEnd
    }
    const e = {
      start,
      end,
      title: event.title
    }
    this.setAgendaClickedTime(e)
    this.setTempEvent(e)
    this.toggleApptBookingModal(true)
    this.blockEventSelect = false
  }

  clearClickedAppt () {
    this.setAgendaClickedAppt(null)
  }

  clearClickedTime () {
    this.setAgendaClickedTime(null)
  }

  today () {
    this.value = ''
    this.calendarSetup()
  }

  removeTempEvent () {
    this.deleteDraftAppointment().then((resp) => {
      // I assume this empty block is intentional
    })

  }

  highlightEvent (event) {
    const e = event
    e.color = 'pink'
  }

  setTempEvent (event) {
    this.removeTempEvent()
    const start = moment(moment.tz(event.start.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).format()).clone()
    let end = moment(moment.tz(event.start.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).format()).clone()
    if (event.end) {
      end = moment(moment.tz(event.end.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).format()).clone()
    } 

    // for draft
    const data: any = {
      start_time: moment.utc(start).format(),
      // setting end time aftger 15 min of start to fix over appoinment time      
      end_time: moment(start).clone().add(15, 'minutes')
    }

    this.postDraftAppointment(data).then((resp) => {
      // I assume this empty block is intentional
    })
  }

  unselect () {
    this.$refs.appointments.fireMethod('unselect')
  }

  calendarSetup () {
    let title = 'Appointments:'
    const name = this.type
    // This happens when user has typed in search field and selected a result
    // It effectively looks like Day View, but we lose the calendar ref.
    if (name === 'day' && this.$refs.calendar === undefined ) {
      title = 'Search Results'
    }

    // This happens when clearing a search result w/o selecting
    if (name === 'week' && this.$refs.calendar === undefined ) {
      return this.setCalendarSetup({ title, name, titleRef: this.calendar_setup.titleRef })
    }
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

    showFlagBus.$on(ShowFlagBusEvents.ShowFlagEvent, (flag: boolean) =>{
      this.show_loading = flag
    }
    )
     this._keyListenerNewApp = function(e) {
            if (e.key === "A" && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                this.setAgendaClickedTime(null)
                this.setAgendaClickedAppt(null)
                this.toggleApptBookingModal(true)
            }
        };
       this._keyListenerWeek = function(e) {
            if (e.key === "M" && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                this.$root.$emit('agendaWeek')
                 this.setToggleAppCalenderView(false)
            }
        };
       this._keyListenerDay = function(e) {
            if (e.key === "D" && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                this.$root.$emit('agendaDay')
                 this.setToggleAppCalenderView(true)
            }
        };
        document.addEventListener('keydown', this._keyListenerNewApp.bind(this));
        document.addEventListener('keydown', this._keyListenerWeek.bind(this));
        document.addEventListener('keydown', this._keyListenerDay.bind(this));
  }
  beforeDestroy() {
      document.removeEventListener('keydown', this._keyListenerNewApp);
      document.removeEventListener('keydown', this._keyListenerWeek);
      document.removeEventListener('keydown', this._keyListenerDay);
  }
  intervalStyle (interval) {
    if (interval.minute == '0' || interval.minute == '30')  {
      interval['background-color'] = "#ebebeb"
    }
    return interval
  }
  showIntervalLabel(interval) {
    if (interval.minute == '0' || interval.minute == '30')  {
      if (interval.minute == '30' && interval.hour == '8') {
        return 
        }
        return interval
    }
  }
} 

</script>
<style scoped>
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
.notes {
  white-space: pre-wrap;
}
tr.fc-list-item {
  border-top: 1px solid gray;
  border-bottom: 1px solid gray;
}
</style>