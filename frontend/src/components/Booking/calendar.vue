<template>
  <v-app>
    <div class="v-application">
      <!-- <div style="width: 100%" class="m-3"> -->
      <div
        style="position: relative; width: 100%"
        ref="calcontainer"
        class="m-3"
      >
        <div style="display: flex; justify-content: flex-start">
          <div style="padding: 0; margin-top: auto; margin-left: 20px">
            <b-form inline>
              <label class="mr-2">
                Filter Exams
                <font-awesome-icon
                  icon="filter"
                  class="m-0 p-0"
                  style="font-size: 1rem"
                />
              </label>
              <!-- <b-form-input
                v-model="searchTerm"
                size="sm"
                @input="filter"
              ></b-form-input> -->
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

              <b-button-group
                horizontal
                class="ml-3 mb-2 pt-2"
                label="Show Bookings in"
              >
                <b-button
                  size="sm"
                  variant="primary"
                  :pressed="!offsiteVisible"
                  @click="toggleOffsite(false)"
                  >On-site</b-button
                >
                <b-button
                  size="sm"
                  variant="primary"
                  :pressed="offsiteOnly"
                  @click="toggleOffsiteOnly('offsite-only')"
                  >Off-site</b-button
                >
                <b-button
                  size="sm"
                  variant="primary"
                  :pressed="offsiteVisible && !offsiteOnly"
                  @click="toggleOffsiteOnly('both')"
                >
                  <span class="mx-1">Both</span>
                </b-button>
              </b-button-group>
            </b-form>
          </div>
          <div
            class="w-50 mt-2 ml-3 pl-3"
            style="display: flex; justify-content: space-between"
            v-if="calView === 'listYear'"
          >
            <div v-for="col in roomLegendArray" :key="col.title">
                <b-badge :style="{ backgroundColor: `${col.color}` }">
                  <span :style="{ color: `${col.color}` }">legend</span>
                </b-badge>
                <span>{{ col.title }}</span>
              </div>
          </div>
        </div>
        <v-sheet>
          <filterCards :events="events" v-if="listView" />
          <v-calendar
            v-else
            ref="calendar"
            :now="currentDay"
            color="primary"
            v-model="value"
            first-time="08:30"
            interval-minutes="30"
            interval-height="40"
            interval-count="17"
            :type="type"
            category-show-all
            :categories="categories"
            :category-days="categoryDays"
            :events="events"
            :event-overlap-mode="mode"
            :event-overlap-threshold="30"
            :event-color="getEventColor"
            @click:event="eventSelected"
            @click:more="eventSelected"
            @change="fetchEvents"
            @click:time-category="selectEvent"
            @click:date="switchView"
            event-text-color=""
          ></v-calendar>
        </v-sheet>
        <div
          class="w-50 mt-2 ml-3 pl-3"
          style="display: flex; justify-content: space-between"
          v-if="calView === 'month'"
        >
          <div v-for="col in roomLegendArray" :key="col.title">
            <b-badge :style="{ backgroundColor: `${col.color}` }">
              <span :style="{ color: `${col.color}` }">legend</span>
            </b-badge>
            <span>{{ col.title }}</span>
          </div>
        </div>
        <BookingModal />
        <ExamInventoryModal v-if="showExamInventoryModal" />
        <OtherBookingModal
          :editSelection="editSelection"
          :getEvent="getEvent"
        />
        <EditBookingModal :tempEvent="tempEvent" />
        <BookingBlackoutModal
          v-if="showBookingBlackoutModal"
        ></BookingBlackoutModal>
        <LoadingModal v-if="show_loading" />
      </div>
    </div>
    <v-dialog
          v-model="expiryNotificationDialog"
          max-width="290"
        >
      <v-card>
        <v-card-title class="headline">
          Schedule Exam
        </v-card-title>
        <v-card-text>
          This exam has expired on {{ examExpiryDateScheduling }}. Scheduling past expiry date is not allowed.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red darken-1"
            text
            @click="expiryNotificationDialog = false"
          >
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script lang="ts">
/* eslint-disable */
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'
// import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

import BookingBlackoutModal from './booking-blackout-modal.vue'
import BookingModal from './booking-modal.vue'
import LoadingModal from './loading.vue'


import DropdownCalendar from './dropdown-calendar.vue'
import EditBookingModal from './edit-booking-modal.vue'
import ExamInventoryModal from './exam-inventory-modal.vue'
import OfficeDropDownFilter from '../exams/office-dropdown-filter.vue'
import OtherBookingModal from './other-booking-modal.vue'
import { adjustColor } from '../../store/helpers'
import filterCards from './filterCards.vue'
import { showBookingFlagBus, ShowBookingFlagBusEvents } from '../../events/showBookingFlagBus'

import { formatedStartTime } from '@/utils/helpers'
import moment from 'moment'

const defaultHoursDuration = 0.5
const categoryDefaultDays = 7
const WEEKEND_STRINGS = ['SAT', 'SUN']

@Component({
  components: {
    BookingBlackoutModal,
    OfficeDropDownFilter,
    BookingModal,
    DropdownCalendar,
    EditBookingModal,
    ExamInventoryModal,
    OtherBookingModal,
    filterCards,
    LoadingModal
  }
})
export default class Calendar extends Vue {
  public $refs: any = {
    bookingcal: HTMLElement
  };

  @State('showBookingBlackoutModal') private showBookingBlackoutModal!: any
  @State('calendarEvents') private calendarEvents!: any
  @State('calendarSetup') private calendarSetup!: any
  @State('editedBooking') private editedBooking!: any
  @State('editedBookingOriginal') private editedBookingOriginal!: any
  @State('exams') private exams!: any
  @State('offsiteOnly') private offsiteOnly!: any
  @State('offsiteVisible') private offsiteVisible!: any
  @State('rescheduling') private rescheduling!: any
  @State('roomResources') private roomResources!: any
  @State('scheduling') public scheduling!: any
  @State('selectedExam') private selectedExam!: any
  @State('showBookingModal') private showBookingModal!: any
  @State('showExamInventoryModal') private showExamInventoryModal!: any
  @State('showStartDateModal') private showStartDateModal!: any

  @Getter('filtered_calendar_events') private filtered_calendar_events!: any;
  @Getter('show_scheduling_indicator') private show_scheduling_indicator!: any;

  @Action('getBookings') public getBookings: any
  @Action('getRooms') public getRooms: any
  @Action('finishBooking') public finishBooking: any
  @Action('initializeAgenda') public initializeAgenda: any
  @Action('getExamTypes') public getExamTypes: any
  @Action('getInvigilators') public getInvigilators: any

  @Mutation('setCalendarSetup') public setCalendarSetup: any
  @Mutation('setClickedDate') public setClickedDate: any
  @Mutation('setEditedBooking') public setEditedBooking: any
  @Mutation('setEditedBookingOriginal') public setEditedBookingOriginal: any
  @Mutation('setOffsiteOnly') public setOffsiteOnly: any
  @Mutation('setSelectedExam') public setSelectedExam: any
  @Mutation('setSelectionIndicator') public setSelectionIndicator: any
  @Mutation('toggleBookingModal') public toggleBookingModal: any
  @Mutation('toggleEditBookingModal') public toggleEditBookingModal: any
  @Mutation('toggleOffsiteVisible') public toggleOffsiteVisible: any
  @Mutation('toggleOtherBookingModal') public toggleOtherBookingModal: any
  @Mutation('toggleScheduling') public toggleScheduling: any
  @Mutation('toggleStartDateModalVisible') public toggleStartDateModalVisible: any

  @Watch('scheduling')
  onSchedulingChange (newVal, oldVal) {
    if (newVal && !oldVal) {
      this.toggleOffsite(false)
    }
    if (oldVal && !newVal) {
      if (this.offsiteVisible) {
        this.toggleOffsite(true)
      }
    }
  }

  @Watch('rescheduling')
  onReschedulingChange (newVal, oldVal) {
    if (newVal && !oldVal) {
      this.toggleOffsite(false)
    }
    if (oldVal && !newVal) {
      if (this.offsiteVisible) {
        this.toggleOffsite(true)
      }
    }
  }
  // vuetify calender

  type: any = 'category'
  categoryDays: number = categoryDefaultDays
  // types: any = ['month', 'week', 'day', '4day']
  mode: any = 'stack'
  // modes: any = ['stack', 'column']
  weekday: any = [1, 2, 3, 4, 5]
  start: any = moment().format('YYYY-MM-DD')
  // weekdays: any = [
  //   { text: 'Sun - Sat', value: [0, 1, 2, 3, 4, 5, 6] },
  //   { text: 'Mon - Sun', value: [1, 2, 3, 4, 5, 6, 0] },
  //   { text: 'Mon - Fri', value: [1, 2, 3, 4, 5] },
  //   { text: 'Mon, Wed, Fri', value: [1, 3, 5] }
  // ]

  value: any = ''
  eventsList: any = []
  currentDay: any = moment().format('YYYY-MM-DD')// new Date()

  categories: any = [] // [] // 'Boardroom 1'
  show_loading: boolean = false

  updated () {
    this.disableSatSun();
  }

  /**
   * The V-Calendar library unfortunately does not support hiding Sat/Sunday when on "Category" view
   * And we are using "Category" view to show multiple rooms per day.
   * As such, our workaround solution is to manually add 
   * a class to the appropriate elements.
   * 
   * Called on every `updated()` CD.
   */
  disableSatSun() {
    const headerElements: NodeListOf<HTMLElement> = document.querySelectorAll('.v-calendar-daily_head-weekday')
    const columnElements: NodeListOf<HTMLElement> = document.querySelectorAll('.v-calendar-category__columns')
    const numberElements: NodeListOf<HTMLElement> = document.querySelectorAll('.v-calendar-daily_head-day-label')
    // Define function inside because we don't need to pollute the main body
    // with heper function used in one place.
    // function disableCalendarElement(el: HTMLElement) {
    function disableCalendarElement(el: HTMLElement) {
      return el.classList.add('disable-sat-sun')
    }
    headerElements.forEach((el: HTMLElement, index) => {
      // For some strange reason, IE11 gets an illegal \u200e typesetting characters, 
      // like hidden whitespace. Doesn't happen on any other browser.
      const elText = el.textContent!.replace('\u200e', '').toUpperCase();
      if (WEEKEND_STRINGS.includes(elText)) {
        disableCalendarElement(el)
        disableCalendarElement(columnElements[index])
        disableCalendarElement(numberElements[index])
      }
    })
  }


  fetchEvents ({ start, end }) {
    return this.events
  }

  getEventColor (event) {
    return event.color
  }

  switchView ({ date }) {
    this.value = date
    this.type = 'category'
    if (this.categoryDays === 1) {
      this.categoryDays = categoryDefaultDays
    } else {
      this.categoryDays = 1
    }
    this.viewRender()
  }

  // vuetify calender end

  //  TOCONFIRM created method for selectAllow to fix context issue
  selectAllow (info) {
    if (info.resourceId === '_offsite') {
      return false
    }
    if (info.weekday === 6 || info.weekday === 0) {
      return false
    }
    // const today = moment()
    const today =  moment.tz(moment().format(), this.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ss')
    if (info.start.isBefore(moment(today))) {
      return false
    }

    if (this.scheduling || this.rescheduling) {
      return true
    }
    return false
  }

  private intervalStart: any = ''
  private intervalEnd: any = ''
  private listView: boolean = false
  private previousView: string = 'agendaWeek'
  private viewRestore: any = []
  private savedSelection: any = null
  private searchTerm: string = ''
  private tempEvent: boolean = false
  public scheduling1: any = false

  private expiryNotificationDialog: boolean = false
  private examExpiryDateScheduling: string = ''

  get events () {
    if (this.searchTerm) {
      return this.filtered_calendar_events(this.searchTerm)
    }

    if (!this.offsiteVisible) {
      return this.calendarEvents.filter(ev => ev.resourceId !== '_offsite')
    }
    if (this.offsiteOnly) {
      return this.calendarEvents.filter(ev => ev.resourceId === '_offsite')
    }
    return this.calendarEvents.filter(x => {
      // Remove events that belong to deleted rooms
      // "roomless" events can stay,i.e. when scheduling an un-scheduled appointment.
      if ( x.room ) {
        return !x.room.deleted
      }
      return true;
    });

  }

  get adjustment () {
    if (this.scheduling || this.rescheduling) {
      return 240
    }
    return 190
  }

  get calView () {
    // if (this.calendarSetup && this.calendarSetup.viewName) {
    //   return this.calendarSetup.viewName
    // }
    return this.type
  }

  get roomLegendArray () {
    if (this.roomResources && this.roomResources.length > 0) {
      return this.roomResources.map(room =>
        ({ color: room.eventColor, title: room.title })
      )
    }
    return []
  }

  agendaDay () {
    this.type = 'category'
    this.categoryDays = 1
    this.viewRender()
  }

  agendaWeek () {
    // this.type = 'category'
    this.type = 'category'
    this.categoryDays = categoryDefaultDays
    this.viewRender()
  }


  clearSearch() {
    this.searchTerm = '';
    this.filter(false);
  }

  cancel () {
    this.removeSavedSelection()
    this.setSelectionIndicator(false)
    if (this.editedBooking) {
      this.toggleEditBookingModal(true)
      // this.$refs.bookingcal.fireMethod('rerenderEvents')
      return
    }
    this.finishBooking()
  }

  // checik both below functions
  getEvent () {
    return this.$refs.bookingcal.fireMethod('clientEvents', '_cal$election')[0]
  }

  editSelection (event: any, adj: any) {
    // eslint-disable-next-line new-cap
    // TOCHECK removed new keyword in moment. not needed
    // const newEnd = new moment(event.end).add(adj, 'h')
    const newEnd = moment(event.end).add(adj, 'h')
    event.end = newEnd
    this.$refs.bookingcal.fireMethod('updateEvent', event)
  }

  // eventRender (event, el, view) {
  //   el.css('max-width', '85%')
  //   if (event.blackout_flag === 'Y') {
  //     el.css('font-size', '.9rem')
  //     el.css('max-width', '100%')
  //     el.css('background-color', '#000000')
  //     el.css('border-color', '#000000')
  //     el.css('color', 'white')
  //   }
  //   if (event.exam && view.name === 'listYear') {
  //     el.find('td.fc-list-item-title.fc-widget-content').html(
  //       `<div style="display: flex; justify-content: center; width: 100%;">
  //            <div class="ft-wt-600 mr-1"><b>Exam:</b></div>
  //            <div class="ft-wt-400 mr-3">${event.title}</div>
  //            <div class="ft-wt-600 mx-1"><b>Event ID:</b></div>
  //            <div class="ft-wt-400 mr-3"> ${event.exam.event_id}</div>
  //            <div class="ft-wt-600 mx-1"><b>Writer:</b></div>
  //            <div class="ft-wt-400 mr-3">${event.exam.examinee_name}</div>
  //            <div class="ft-wt-600 mx-1"><b>Received:</b></div>
  //            <div class="ft-wt-400 mr-3">${moment(event.exam.exam_received_date).format('MMM Do, YYYY')}</div>
  //            <div class="ft-wt-600 mx-1"><b>Expiry:</b></div>
  //            <div class="ft-wt-400 mr-3">${moment(event.exam.exam_expiry).format('MMM Do, YYYY')}</div>
  //            <div class="ft-wt-600 mx-1"><b>Method:</b></div>
  //            <div class="ft-wt-400 mr-3">${event.exam.exam_method}</div>
  //            <div class="ft-wt-600 mx-1"><b>Invigilator:</b></div>
  //            <div class="ft-wt-400 mr-3">${event.invigilator.invigilator_name}</div>
  //          </div>`
  //     )
  //   }
  //   if (!event.exam) {
  //     el.find('td.fc-list-item-title.fc-widget-content').html(
  //       `<div style="display: flex; justify-content: flex-center; width: 100%;">
  //            <div class="ft-wt-400 mr-3">${event.title}</div>
  //            <div>Non-Exam / Other Event</div>
  //          </div>
  //         `
  //     )
  //   }
  // }

  eventSelected (selectedEvent, jsEvent, view) {
    // shallow copy to avoid re-rendering start time with moment instance
    // vuetify will accept only date  instance / string / epoch
    const currentEvent = { ...selectedEvent.event }
    // console.log('event', event)
    currentEvent.start = moment(currentEvent.start)
    currentEvent.end = moment(currentEvent.end)
    // currentEvent.start = moment.tz(currentEvent.start, this.$store.state.user.office.timezone.timezone_name)
    // currentEvent.end = moment.tz(currentEvent.start, this.$store.state.user.office.timezone.timezone_name)

    if (this.scheduling || this.rescheduling || currentEvent.resourceId === '_offsite') {
      return
    }
    if (this.type !== 'category') {
      this.goToDate(currentEvent.start)
      // this.goToDate(moment.tz(currentEvent.start, this.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'))
      this.agendaDay()
      this.searchTerm = ''
    }
    const newColor = adjustColor(currentEvent.room.color, 128)
    currentEvent.backgroundColor = newColor
    // this.$refs.bookingcal.fireMethod('updateEvent', event)
    this.setEditedBooking(currentEvent)
    if (Object.keys(currentEvent).includes('exam')) {
      this.setSelectedExam(currentEvent.exam)
    }
    this.setEditedBookingOriginal(currentEvent)
    this.toggleEditBookingModal(true)
  }

  filter (event) {
    if (event) {
      if (!this.listView) {
        // this.$refs.bookingcal.fireMethod('changeView', 'listYear')
        this.listView = true
      }
    }
    if (!event) {
      if (this.listView) {
        // const view = this.calendarSetup.viewName
        // this.$refs.bookingcal.fireMethod('changeView', view)
        this.listView = false
      }
    }
  }

  filterKeyPress (e) {
    if (e.keyCode === 13) {
      e.preventDefault()
    }
  }

  goToDate (date) {
    if (date) {
      this.listView = false
      this.type = 'category'
      this.categoryDays = 1
      this.value = new Date(date)
      this.viewRender()
    }
  }

  initialize () {
    this.initializeAgenda()
    this.setSelectionIndicator(false)
    this.tempEvent = false
  }

  month () {
    this.type = 'month'
    this.viewRender()
  }

  next () {
    if (this.$refs.calendar) {
      // this.$refs.bookingcal.fireMethod('next')
      this.$refs.calendar.next()
      this.viewRender()
    }
  }

  options (option) {
    // if (this.$refs.bookingcal) {
    //   this.$refs.bookingcal.fireMethod('option', option.name, option.value)
    // }
  }

  prev () {
    if (this.$refs.calendar) {
      // this.$refs.bookingcal.fireMethod('prev')
      this.$refs.calendar.prev()
      this.viewRender()
    }
  }

  removeSavedSelection () {
    if (this.savedSelection) {
      this.$refs.bookingcal.fireMethod('removeEvents', [this.savedSelection.id])
    }
  }

  renderEvent (event) {
    // this.$refs.bookingcal.fireMethod('renderEvent', event)
    this.savedSelection = event
    this.setSelectionIndicator(true)
  }

  selectEvent (event) {
    // setting format date time for events
    // const date = moment.tz(event.date, this.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD')
    // const time = moment.tz(event.time, this.$store.state.user.office.timezone.timezone_name).format('HH:mm:ssZ')
    //  const start = formatedStartTime(date, time)// event.start.clone()
    const start = formatedStartTime(event.date, event.time)// event.start.clone()
    event.start = start

    // not allowd if past date
    if (!this.selectAllow(event)) {
      return false
    }
    // setting default end time
    event.end = moment(event.start).add(defaultHoursDuration, 'h')
    // event.end = moment.tz(event.start, this.$store.state.user.office.timezone.timezone_name).add(defaultHoursDuration, 'h')
    const resourceDetails = this.roomResources.find(cat => {
      // Refer to getCategoryList():
      // event.category is a string and it does not have a property named categoryName
      // However, event.categoryName was added as part of Roombooking issue fix PR #555
      // Hence this extended expression for equality to keep the changes passive.
      return cat.title === event.category?.categoryName || cat.title === event.category
    })
    if (resourceDetails) { event.resource = resourceDetails }

    // called whenever a a block of free time is clicked or a range of free time is selected on the calendar
    // if (this.calendarSetup && this.calendarSetup.viewName && this.calendarSetup.viewName === 'month') {
    if (this.type === 'month') {
      // overrides the default behavior (sets event=all day event on the day) to a view change instead
      this.goToDate(event.start.local())
      // this.goToDate(moment.tz(event.start, this.$store.state.user.office.timezone.timezone_name))
      this.agendaDay()
      return
    }
    // category
    if (this.rescheduling) {
      // this.unselect()
      this.removeSavedSelection()
      const booking = this.editedBookingOriginal     
      // Checking if re-scheduled date is past expiry date of the exam
      if(this.selectedExam) {
        if (moment(this.selectedExam.expiry_date).isValid() && moment(this.selectedExam.expiry_date).isBefore(moment(event.start), 'day')) {          
          console.log('expiry date in the past!')
          this.examExpiryDateScheduling = moment(this.selectedExam.expiry_date).format('MMMM DD, YYYY')
          this.expiryNotificationDialog = true
          return
        }
      }
      if (this.selectedExam && (Object.keys(this.selectedExam) as any) > 0) {
        const { number_of_hours, number_of_minutes } = this.selectedExam.exam_type
        // TOCHECK removed new keyword in moment. not needed
        // const endTime = new moment(event.start).add(number_of_hours, 'h')
        const endTime = moment(event.start).add(number_of_hours, 'h')
          .add(number_of_minutes, 'm')
        // const endTime = moment.tz(event.start, this.$store.state.user.office.timezone.timezone_name).add(number_of_hours, 'h')
        //   .add(number_of_minutes, 'm')
        event.end = endTime
        this.setClickedDate(event)
        // TOCHECK removed new keyword in moment. not needed
        //  start: new moment(event.start),
        // end: new moment(event.end),
        const tempEvent = {
          start: moment(event.start),
          end: moment(event.end),
          // start: moment.tz(event.start, this.$store.state.user.office.timezone.timezone_name),
          // end: moment.tz(event.end, this.$store.state.user.office.timezone.timezone_name),
          title: '(NEW TIME) ' + booking.title,
          borderColor: event.resource.eventColor,
          backgroundColor: 'white',
          resourceId: event.resource.id,
          id: '_cal$election'
        }
        // Verify below `setEditedBooking()` is working in OCP3
        // When re-scheduling, is proper date shown?
        this.setEditedBooking(tempEvent)
        this.toggleEditBookingModal(true)

        return
      }
      // change to moment time
      booking.end = !moment.isMoment(booking.end) ? moment(booking.end) : booking.end
      booking.start = !moment.isMoment(booking.start) ? moment(booking.start) : booking.start
      // booking.end = !moment.isMoment(booking.end) ? moment.tz(booking.end, this.$store.state.user.office.timezone.timezone_name) : booking.end
      // booking.start = !moment.isMoment(booking.start) ? moment.tz(booking.start, this.$store.state.user.office.timezone.timezone_name) : booking.start
      
      const i = booking.start.clone()
      const f = booking.end.clone()
      // TOCHECK removed new keyword in moment. not needed
      // const duration = new moment(f).diff(new moment(i), 'h', true)
      const duration = moment(f).diff(moment(i), 'h', true)
      const ii = event.start.clone()
      const ff = event.end.clone()
      const clickedDuration = ff.diff(ii, 'h', true)
      const tempEvent: any = {
        // TOCHECK removed new keyword in moment. not needed
        // start: new moment(event.start),
        start: moment(event.start), 
        // start: moment.tz(event.start, this.$store.state.user.office.timezone.timezone_name),
        title: '(NEW TIME) ' + booking.title,
        borderColor: event.resource.eventColor,
        backgroundColor: 'white',
        resourceId: event.resource.id,
        id: '_cal$election'
      }
      if (clickedDuration == 0.5) {
        // TOCHECK removed new keyword in moment. not needed
        // tempEvent.end = new moment(event.start).add(duration, 'h')
        tempEvent.end = moment(event.start).add(duration, 'h')
        // tempEvent.end = moment.tz(event.start, this.$store.state.user.office.timezone.timezone_name).add(duration, 'h')
      } else {
        // TOCHECK removed new keyword in moment. not needed
        // tempEvent.end = new moment(event.end)
        tempEvent.end = moment(event.end)
      }
      event.end = tempEvent.end
      this.tempEvent = true

      // this.renderEvent(tempEvent)

      this.toggleEditBookingModal(true)
      this.setClickedDate(event)
      return
    }
    const selection: any = {
      // TOCHECK removed new keyword in moment. not needed
      // start: new moment(event.start),
      start: moment(event.start),
      // start: moment.tz(event.start, this.$store.state.user.office.timezone.timezone_name),
      resourceId: (event && event.resource ) ? event.resource.id : undefined,
      id: '_cal$election'
    }

    if (this.scheduling) {
      if (this.selectedExam && Object.keys(this.selectedExam).length > 0) {
        // Checking if scheduled date is past expiry date of the exam  
        if (moment(this.selectedExam.expiry_date).isValid() && moment(this.selectedExam.expiry_date).isBefore(selection.start, 'day')) {          
          this.examExpiryDateScheduling = moment(this.selectedExam.expiry_date).format('MMMM DD, YYYY')
          this.expiryNotificationDialog = true
          return
        } else {          
          // this.unselect()
          // TOCHECK removed new keyword in moment.not needed
          // selection.end = new moment(event.start).add(this.selectedExam.exam_type.number_of_hours, 'h')
          selection.end = moment(event.start).add(this.selectedExam.exam_type.number_of_hours, 'h')
            .add(this.selectedExam.exam_type.number_of_minutes, 'm')
          // selection.end = moment.tz(event.start, this.$store.state.user.office.timezone.timezone_name)
          //   .add(this.selectedExam.exam_type.number_of_hours, 'h')
          //   .add(this.selectedExam.exam_type.number_of_minutes, 'm')
          selection.title = this.selectedExam.exam_name
          this.removeSavedSelection()
          this.toggleBookingModal(true)
          this.$root.$emit('showbookingmodal')
        }        
      } else {
        // this.unselect()
        this.toggleOtherBookingModal(true)
        selection.title = 'New Event'
        // TOCHECK removed new keyword in moment.not needed
        selection.end = moment(event.end)
      }
    }
    // this.renderEvent(selection)

    event.start = moment(selection.start)
    event.end = moment(selection.end)
    // event.start = moment.tz(selection.start, this.$store.state.user.office.timezone.timezone_name)
    // event.end = moment.tz(selection.end, this.$store.state.user.office.timezone.timezone_name)

    this.setClickedDate(event)
  }

  today () {
    this.value = ''
    this.type = 'category'
    this.viewRender()
  }

  toggleOffsiteOnly (mode) {
    this.getCategoryList(mode)
    if (mode === 'both') {
      if (this.offsiteOnly) {
        // const addRooms = this.roomResources.filter(room => room.id !== '_offsite')
        // addRooms.forEach(room => {
        //   // this.$refs.bookingcal.fireMethod('addResource', room)
        // })

        this.setOffsiteOnly(false)
        return
      }
      if (!this.offsiteVisible) this.toggleOffsite(true)
      return
    }
    const setOffsiteOnly = () => {
      if (!this.offsiteVisible) this.toggleOffsite(true)
      // const removeRooms = this.roomResources.filter(room => room.id !== '_offsite')
      // removeRooms.forEach(room => {
      //    this.$refs.bookingcal.fireMethod('removeResource', room.id)
      // })
      this.toggleOffsiteVisible(true)
      this.setOffsiteOnly(true)
    }
    if (mode === 'offsite-only' && !this.offsiteOnly) {
      setOffsiteOnly()
    }
    if (mode === 'setup') {
      setOffsiteOnly()
    }
  }

  toggleOffsite (bool) {
    this.toggleOffsiteVisible(bool)
    if (bool) {
      // this.$refs.bookingcal.fireMethod('addResource', {
      //   id: '_offsite',
      //   title: 'Offsite',
      //   eventColor: '#F58B4C'
      // })
    }
    if (!bool) {
      if (this.offsiteOnly) {
        // const addRooms = this.roomResources.filter(room => room.id !== '_offsite')
        // addRooms.forEach(room => {
        //   // this.$refs.bookingcal.fireMethod('addResource', room)
        // })
      }
      // this.$refs.bookingcal.fireMethod('removeResource', '_offsite')
      this.setOffsiteOnly(false)
    }
    this.getCategoryList(bool)
  }

  unselect () {
    // this.$refs.bookingcal.fireMethod('unselect')
    this.tempEvent = false
  }

  updateEvent (event, params) {
    Object.keys(params).forEach(key => {
      event[key] = params[key]
    })
    // this.$refs.bookingcal.fireMethod('updateEvent', event)
  }

  viewRender () {
    // const title = this.$refs.calendar.title
    let viewName = 'week'

    if (this.type === 'category') {
      if (this.categoryDays === 1) {
        viewName = 'agendaDay'
      } else {
        viewName = 'week'
      }
    } else {
      viewName = 'month'
    }
    if (this.$refs.calendar) {
        this.setCalendarSetup({ title: this.$refs.calendar.title, viewName, titleRef: this.$refs.calendar })
    }
  }

  // viewRender (view, el) {
  //   if (view.name !== 'listYear') {
  //     if (view.name === 'agendaDay') {
  //       const title = moment(view.intervalStart).format('dddd MMMM D, YYYY')
  //       this.setCalendarSetup({ title, viewName: view.name })
  //     } else {
  //       this.setCalendarSetup({ title: view.title, viewName: view.name })
  //     }
  //   }
  //   if (view.name === 'basicDay') {
  //     this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
  //   }
  //   if (view.name === 'month') {
  //     this.options({ name: 'height', value: window.innerHeight - this.adjustment })
  //   }
  //   if (view.name === 'agendaDay' || view.name === 'agendaWeek') {
  //     this.options({ name: 'height', value: 'auto' })
  //   }
  //   if (this.selectedExam && this.selectedExam.gotoDate) {
  //     this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
  //     this.goToDate(this.selectedExam.gotoDate)
  //   }
  // }

  mounted () {
    document.addEventListener('keydown', this.filterKeyPress)
    this.getRooms()
    this.getExamTypes()
    this.getInvigilators()
    this.initialize()
    this.$root.$on('agendaDay', () => { this.agendaDay() })
    this.viewRender()
    this.$root.$on('agendaWeek', () => { this.agendaWeek() })
    this.$root.$on('cancel', () => { this.cancel() })
    this.$root.$on('initialize', () => { this.initialize() })
    this.$root.$on('month', () => { this.month() })
    this.$root.$on('next', () => { this.next() })
    this.$root.$on('options', (option) => { this.options(option) })
    this.$root.$on('prev', () => { this.prev() })
    this.$root.$on('removeSavedSelection', () => { this.removeSavedSelection() })
    this.$root.$on('today', () => { this.today() })
    this.$root.$on('toggleOffsite', (bool) => { this.toggleOffsite(bool) })
    this.$root.$on('unselect', () => { this.unselect() })
    this.$root.$on('updateEvent', (event, params) => { this.updateEvent(event, params) })
    this.$root.$on('goToDate', (date) => { this.goToDate(date) })
    this.toggleOffsite(false) // initial show only onsite rooms
  }

  async getCategoryList (flag) {
    this.categories = []
    await this.getRooms()
    this.roomResources.forEach(each => {
          if (each.title) {
            if (flag == false) {
              if (each.id !== '_offsite'){
                   this.categories.push(each.title)
              }
            }
            else if (flag === 'offsite-only') {
              if (each.id === '_offsite'){
                   this.categories.push(each.title)
              }
            } else if (flag === 'both')
             {
              this.categories.push(each.title)
            }
          }
        });
  }

  destroyed () {
    this.setCalendarSetup(null)
    this.toggleScheduling(false)
    document.removeEventListener('keydown', this.filterKeyPress)
  }

  created () {
    showBookingFlagBus.$on(ShowBookingFlagBusEvents.ShowBookingFlagEvent, (flag: boolean) =>{
      this.show_loading = flag
    })
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
.btn:active,
.btn.active {
  background-color: #184368 !important;
  color: white !important;
}

tr.fc-list-item {
  border-top: 1px solid gray;
  border-bottom: 1px solid gray;
}
</style>
