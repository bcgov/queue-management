<template>
    <div style="position: relative" ref="calcontainer">`
      <div style="display: flex; justify-content: flex-start">
        <div style="padding: 0; margin: -25px 0px -5px 15px">
          <b-form inline>
            <label class="mr-2">Filter Exams
              <font-awesome-icon icon="filter"
                                 class="m-0 p-0"
                                 style="font-size: 1rem;"/>
            </label>
            <b-form-input v-model="searchTerm" @input="filter"></b-form-input>
          </b-form>
        </div>
        <div class="w-50 mt-2 ml-3 pl-3"
             style="display: flex; justify-content: space-between;"
             v-if="calView === 'listYear'">
          <template v-for="col in roomLegendArray">
            <div>
              <b-badge :style="{backgroundColor: `${col.color}`}">
                <span :style="{color: `${col.color}`}">legend</span>
              </b-badge>
              <span>{{ col.title }}</span>
            </div>
          </template>
        </div>
      </div>
      <keep-alive>
        <full-calendar ref="bookingcal"
                       key="bookingcal"
                       id="bookingcal"
                       class="q-calendar-margins"
                       @event-selected="eventSelected"
                       @view-render="viewRender"
                       @event-created="selectEvent"
                       @event-render="eventRender"
                       :events="events()"
                       :config="setup">

        </full-calendar>
      </keep-alive>
      <div class="w-50 mt-2 ml-3 pl-3" style="display: flex; justify-content: space-between;"
           v-if="calView === 'month'">
        <template v-for="col in roomLegendArray">
          <div>
            <b-badge :style="{backgroundColor: `${col.color}`}">
              <span :style="{color: `${col.color}`}">legend</span>
            </b-badge>
            <span>{{ col.title }}</span>
          </div>
        </template>
      </div>
    <BookingModal />
    <ExamInventoryModal v-if="showExamInventoryModal" />
    <OtherBookingModal :editSelection="editSelection" :getEvent="getEvent" />
    <EditBookingModal />
  </div>
</template>

<script>
  import { FullCalendar } from 'vue-full-calendar'
  import { mapActions, mapGetters, mapMutations, mapState, } from 'vuex'
  import BookingModal from './booking-modal'
  import DropdownCalendar from './dropdown-calendar'
  import EditBookingModal from './edit-booking-modal'
  import ExamInventoryModal from './exam-inventory-modal'
  import moment from 'moment'
  import OtherBookingModal from './other-booking-modal'
  import SchedulingIndicator from './scheduling-indicator'
  import 'fullcalendar-scheduler'
  import 'fullcalendar/dist/fullcalendar.css'
  import { adjustColor } from '../store/helpers'

  export default {
    name: 'Calendar',
    components: {
      BookingModal,
      DropdownCalendar,
      EditBookingModal,
      ExamInventoryModal,
      FullCalendar,
      OtherBookingModal,
      SchedulingIndicator,
    },
    mounted() {
      this.initialize()
      this.$root.$on('agendaDay', () => { this.agendaDay() })
      this.$root.$on('agendaWeek', () => { this.agendaWeek() })
      this.$root.$on('cancel', () => { this.cancel() })
      this.$root.$on('initialize', () => { this.initialize() })
      this.$root.$on('month', () => { this.month() })
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('options', (option) => { this.options(option) })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('today', () => { this.today() })
      this.$root.$on('unselect', () => { this.unselect() })
      this.$root.$on('updateEvent', (event, params) => { this.updateEvent(event, params) })
      this.$root.$on('removeSavedSelection', () => {this.removeSavedSelection() })
    },
    data() {
      return {
        savedSelection: null,
        tempEvent: null,
        listView: false,
        searchTerm: '',
        setup: {
          defaultView: 'agendaWeek',
          editable: false,
          selectConstraint: {
            start: '07:00:00',
            end: '18:00:00',
          },
          eventConstraint: {
            start: '07:00:00',
            end: '18:00:00',
          },
          fixedWeekCount: false,
          header: {
            left: null,
            center: null,
            right: null
          },
          height: 'auto',
          maxTime: '18:00:00',
          minTime: '07:00:00',
          navLinks: true,
          resources: [],
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          selectable: false,
          showNonCurrentDates: false,
          timezone: 'local',
          unselectCancel: '.modal, .modal-content',
          weekends: false,
          views: {
            agendaDay: {
              allDaySlot: false,
              groupByResource: true,
              nowIndicator: true,
            },
            agendaWeek: {
              allDaySlot: false,
              groupByDateAndResource: true,
              nowIndicator: true,
            },
            list: {
              listDayAltFormat: false,
            },
            month: {
              allDaySlot: false,
              groupByResource: false,
            },
          },
        },
      }
    },
    computed: {
      ...mapGetters(['calendar_events', 'room_resources',]),
      ...mapState([
        'calendarSetup',
        'editedBooking',
        'editedBookingOriginal',
        'exam_types',
        'exams',
        'rescheduling',
        'scheduling',
        'schedulingOther',
        'selectedExam',
        'showBookingModal',
        'showExamInventoryModal',
        'showSchedulingIndicator',
      ]),
      adjustment() {
        if (this.showSchedulingIndicator) {
          return 240
        }
        return 190
      },
      calView() {
        if (this.calendarSetup && this.calendarSetup.viewName) {
          return this.calendarSetup.viewName
        }
        return ''
      },
      roomLegendArray() {
        if (this.room_resources && this.room_resources.length > 0) {
          return this.room_resources.map(room =>
            ({color: room.eventColor, title: room.title})
          )
        }
        return []
      },
    },
    destroyed() {
      this.setCalendarSetup(null)
    },
    methods: {
      ...mapActions(['getBookings', 'finishBooking', 'initializeAgenda', 'getExamTypes',]),
      ...mapMutations([
        'setCalendarSetup',
        'setClickedDate',
        'setEditedBooking',
        'setEditedBookingOriginal',
        'setSelectedExam',
        'setSelectionIndicator',
        'toggleBookingModal',
        'toggleEditBookingModal',
        'toggleOtherBookingModal',
        'toggleScheduling',
        'toggleSchedulingIndicator',
        'toggleSchedulingOther',
      ]),
      agendaDay() {
        this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
      },
      agendaWeek() {
        this.$refs.bookingcal.fireMethod('changeView', 'agendaWeek')
      },
      cancel() {
        this.removeSavedSelection()
        this.setSelectionIndicator(false)
        this.unselect()
        if (this.editedBooking) {
          this.toggleEditBookingModal(true)
          this.toggleSchedulingIndicator(false)
          this.$refs.bookingcal.fireMethod('rerenderEvents')
          return
        }
        this.finishBooking()
        this.options({name: 'selectable', value: false})
      },
      getEvent() {
        return this.$refs.bookingcal.fireMethod('clientEvents', '_cal$election')[0]
      },
      editSelection(event, adj) {
        let newEnd = new moment(event.end).add(adj, 'h')
        event.end = newEnd
        this.$refs.bookingcal.fireMethod('updateEvent', event)
      },
      eventRender(event, el, view) {
        if (event.exam) {
          el.find('td.fc-list-item-title.fc-widget-content').html(
          `<div style="display: flex; justify-content: center; width: 100%;">
             <div class="ft-wt-600 mr-1"><b>Exam:</b></div>
             <div class="ft-wt-400 mr-3">${ event.title }</div>
             <div class="ft-wt-600 mx-1"><b>Event ID:</b></div>
             <div class="ft-wt-400 mr-3"> ${ event.exam.event_id }</div>
             <div class="ft-wt-600 mx-1"><b>Writer:</b></div>
             <div class="ft-wt-400 mr-3">${ event.exam.examinee_name }</div>
             <div class="ft-wt-600 mx-1"><b>Received:</b></div>
             <div class="ft-wt-400 mr-3">${ moment(event.exam.exam_received_date).format('MMM Do, YYYY') }</div>
             <div class="ft-wt-600 mx-1"><b>Expiry:</b></div>
             <div class="ft-wt-400 mr-3">${ moment(event.exam.exam_expiry).format('MMM Do, YYYY') }</div>
             <div class="ft-wt-600 mx-1"><b>Method:</b></div>
             <div class="ft-wt-400 mr-3">${ event.exam.exam_method }</div>
             <div class="ft-wt-600 mx-1"><b>Invigilator:</b></div>
             <div class="ft-wt-400 mr-3">${ event.invigilator.invigilator_name }</div>
           </div>`
          )
        }
        if  (!event.exam) {
          el.find('td.fc-list-item-title.fc-widget-content').html(
          `<div style="display: flex; justify-content: flex-center; width: 100%;">
             <div class="ft-wt-400 mr-3">${ event.title }</div>
             <div>Non-Exam / Other Event</div>
           </div>
          `
          )
        }
      },
      events() {
        if (this.searchTerm) {
          return this.$store.getters.filtered_calendar_events(this.searchTerm)
        }
        return this.calendar_events
      },
      eventSelected(event, jsEvent, view) {
        if (this.scheduling || this.schedulingOther) {
          return
        }
        if (view.name === 'listYear') {
          this.goToDate(event.start)
          this.agendaDay()
          this.searchTerm = ''
        }
        let newColor = adjustColor(event.room.color, 128)
        event.backgroundColor = newColor
        this.$refs.bookingcal.fireMethod('updateEvent', event)
        this.setEditedBooking(event)
        if (Object.keys(event).includes('exam')) {
          this.setSelectedExam(event.exam)
        }
        this.setEditedBookingOriginal(event)
        this.toggleEditBookingModal(true)
      },
      filter(event) {
        if (event) {
          if (!this.listView) {
            this.$refs.bookingcal.fireMethod('changeView', 'listYear')
            this.listView = true
          }
        }
        if (!event) {
          if (this.listView) {
            let view = this.calendarSetup.viewName
            this.$refs.bookingcal.fireMethod('changeView', view)
            this.listView = false
          }
        }
      },
      goToDate(date) {
        this.$refs.bookingcal.fireMethod('gotoDate', date)
      },
      initialize() {
        this.setSelectionIndicator(false)
        this.getExamTypes()
        this.initializeAgenda().then( rooms => {
          rooms.forEach( room => {
            let roomObj = {
              id: room.room_id,
              title: room.room_name,
              eventColor: room.color
            }
            this.$refs.bookingcal.fireMethod('addResource', roomObj)
          })
          this.getBookings()
        })
      },
      month() {
        this.$refs.bookingcal.fireMethod('changeView', 'month')
      },
      next() {
        this.$refs.bookingcal.fireMethod('next')
      },
      options(option) {
        this.$refs.bookingcal.fireMethod('option', option.name, option.value)
      },
      prev() {
        this.$refs.bookingcal.fireMethod('prev')
      },
      removeSavedSelection() {
        if (this.savedSelection) {
          this.$refs.bookingcal.fireMethod('removeEvents', [this.savedSelection.id])
        }
      },
      renderEvent(event) {
        this.$refs.bookingcal.fireMethod('renderEvent', event)
        this.savedSelection = event
        this.setSelectionIndicator(true)
      },
      selectEvent(event) {
        //called whenever a a block of free time is clicked or a range of free time is selected on the calendar
        if (this.calendarSetup.viewName === 'month') {
          //overrides the default behavior (sets event=all day event on the day) to a view change instead
          this.goToDate(event.start.local())
          this.agendaDay()
          return
        }
        if (this.rescheduling) {
          this.unselect()
          this.removeSavedSelection()
          let booking = this.editedBookingOriginal
          if (Object.keys(booking).includes('exam')) {
            let { number_of_hours } = this.selectedExam.exam_type
            let endTime = new moment(event.start).add(number_of_hours, 'h')
            event.end = endTime
            this.setClickedDate(event)
            let tempEvent = {
              start: new moment(event.start),
              end: new moment(event.end),
              title: '(NEW TIME) ' + booking.title,
              borderColor: event.resource.eventColor,
              backgroundColor: 'white',
              resourceId: event.resource.id,
              id: '_cal$election'
            }
            this.renderEvent(tempEvent)
            this.toggleEditBookingModal(true)
            return
          }
          let i = new moment(booking.start)
          let f = new moment(booking.end)
          let duration = new moment(f).diff(new moment(i), 'h', true)
          let ii = new moment(event.start)
          let ff = new moment(event.end)
          let clickedDuration = ff.diff(ii, 'h', true)
          let tempEvent = {
            start: new moment(event.start),
            title: '(NEW TIME) ' + booking.title,
            borderColor: event.resource.eventColor,
            backgroundColor: 'white',
            resourceId: event.resource.id,
            id: '_cal$election'
          }
          if (clickedDuration == 0.5) {
            tempEvent.end = new moment(event.start).add(duration, 'h')
          } else {
            tempEvent.end = new moment(event.end)
          }
          event.end = tempEvent.end
          this.renderEvent(tempEvent)
          this.toggleSchedulingIndicator(false)
          this.toggleEditBookingModal(true)
          this.setClickedDate(event)
          return
        }
        let selection = {
          start: new moment(event.start),
          resourceId: event.resource.id,
          id: '_cal$election'
        }
        this.toggleSchedulingIndicator(false)
        if (this.scheduling) {
          selection.end = new moment(event.start).add(this.selectedExam.exam_type.number_of_hours, 'h')
          selection.title = this.selectedExam.exam_name
          this.unselect()
          this.removeSavedSelection()
          this.toggleBookingModal(true)
        }
        else if (this.schedulingOther) {
          this.unselect()
          this.toggleOtherBookingModal(true)
          selection.title = 'New Event'
          selection.end = new moment(event.end)
        }
        this.renderEvent(selection)
        event.start = new moment(selection.start)
        event.end = new moment(selection.end)
        this.setClickedDate(event)
      },
      today() {
        this.$refs.bookingcal.fireMethod('today')
      },
      unselect() {
        this.$refs.bookingcal.fireMethod('unselect')
      },
      updateEvent(event, params) {
        Object.keys(params).forEach(key => {
          event[key] = params[key]
        })
        this.$refs.bookingcal.fireMethod('updateEvent', event)
      },
      viewRender(view, el) {
        if (view.name !== 'listYear') {
          this.setCalendarSetup({ title: view.title, viewName: view.name })
        }
        if (view.name === 'basicDay') {
          this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
        }
        if (view.name === 'month') {
          this.options({ name: 'height', value: window.innerHeight - this.adjustment })
        }
        if (view.name === 'agendaDay' || view.name === 'agendaWeek') {
          this.options({ name: 'height', value: 'auto' })
        }
        if(this.$route.params.date) {
          this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
          this.goToDate(this.$route.params.date)
        }
      },
    }
  }


</script>
