<template>
  <div style="position: relative" ref="calcontainer">
    <div style="display: flex; justify-content: flex-start">
      <div style="padding: 0; margin-top:auto; margin-left: 20px;">
        <b-form inline>
          <label class="mr-2">Filter Exams
            <font-awesome-icon icon="filter"
                               class="m-0 p-0"
                               style="font-size: 1rem;"/>
          </label>
          <b-form-input v-model="searchTerm"
                        size="sm"
                        @input="filter"></b-form-input>
          <b-button class="btn-secondary btn-sm ml-3"
                    v-if="!show_scheduling_indicator"
                    @click="toggleOffsite(!offsiteVisible)">
            {{ offsiteVisible ? 'Hide Offsite' : 'Show Offsite' }}
          </b-button>
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
                     :config="config">
      </full-calendar>
    </keep-alive>
    <div class="w-50 mt-2 ml-3 pl-3"
         style="display: flex; justify-content: space-between;"
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
  <EditBookingModal :tempEvent="tempEvent" />
</div>
</template>

<script>
  import { FullCalendar } from 'vue-full-calendar'
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import BookingModal from './booking-modal'
  import DropdownCalendar from './dropdown-calendar'
  import EditBookingModal from './edit-booking-modal'
  import ExamInventoryModal from './exam-inventory-modal'
  import moment from 'moment'
  import OtherBookingModal from './other-booking-modal'
  import 'fullcalendar-scheduler'
  import 'fullcalendar/dist/fullcalendar.css'
  import { adjustColor } from '../store/helpers'
  import OfficeDropDownFilter from '../exams/office-dropdown-filter'

  export default {
    name: 'Calendar',
    components: {
      OfficeDropDownFilter,
      BookingModal,
      DropdownCalendar,
      EditBookingModal,
      ExamInventoryModal,
      FullCalendar,
      OtherBookingModal,
    },
    mounted() {
      document.addEventListener('keydown', this.filterKeyPress)
      this.getExamTypes()
      this.getInvigilators()
      this.initialize()
      this.$root.$on('agendaDay', () => { this.agendaDay() })
      this.$root.$on('agendaWeek', () => { this.agendaWeek() })
      this.$root.$on('cancel', () => { this.cancel() })
      this.$root.$on('initialize', () => { this.initialize() })
      this.$root.$on('month', () => { this.month() })
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('options', (option) => { this.options(option) })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('removeSavedSelection', () => {this.removeSavedSelection() })
      this.$root.$on('today', () => { this.today() })
      this.$root.$on('toggleOffsite', (bool) => { this.toggleOffsite(bool) })
      this.$root.$on('unselect', () => { this.unselect() })
      this.$root.$on('updateEvent', (event, params) => { this.updateEvent(event, params) })
    },
    data() {
      return {
        tempEvent: false,
        savedSelection: null,
        listView: false,
        searchTerm: '',
        config: {
          columnHeaderFormat: 'ddd/D',
          selectAllow: (info) => {
            if (info.resourceId === '_offsite') {
              return false
            }
            let today = moment()
            if(info.start.isBefore(today)){
              return false
            }
            if (this.scheduling || this.rescheduling) {
              return true
            }
            return false
          },
          defaultView: 'agendaWeek',
          editable: false,
          eventConstraint: {
            start: '08:00:00',
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
          minTime: '08:00:00',
          navLinks: true,
          resources: (setResources) => {
            this.getRooms().then( resources => {
              setResources(resources)
              this.$nextTick(function() {
                if (!this.offsiteVisible) {
                  this.toggleOffsite(false)
                }
              })
            })
          },
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          selectConstraint: {
            start: '08:00:00',
            end: '18:00:00',
          },
          showNonCurrentDates: false,
          timezone: 'local',
          unselectCancel: '.modal, .modal-content',
          views: {
            agendaDay: {
              allDaySlot: false,
              groupByResource: true,
            },
            agendaWeek: {
              allDaySlot: false,
              groupByDateAndResource: true,
            },
            list: {
              listDayAltFormat: false,
            },
            month: {
              allDaySlot: false,
              groupByResource: false,
            },
          },
          weekends: false,
        },
      }
    },
    computed: {
      ...mapGetters(['filtered_calendar_events', 'show_scheduling_indicator']),
      ...mapState([
        'calendarEvents',
        'calendarSetup',
        'editedBooking',
        'editedBookingOriginal',
        'exams',
        'offsiteVisible',
        'rescheduling',
        'roomResources',
        'scheduling',
        'selectedExam',
        'showBookingModal',
        'showExamInventoryModal',
        'showStartDateModal',
      ]),
      adjustment() {
        if (this.scheduling || this.rescheduling) {
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
        if (this.roomResources && this.roomResources.length > 0) {
          return this.roomResources.map(room =>
            ({color: room.eventColor, title: room.title})
          )
        }
        return []
      },
    },
    watch: {
      scheduling(newVal, oldVal) {
        if (newVal && !oldVal) {
          this.toggleOffsite(false)
        }
        if (oldVal && !newVal) {
          if (this.offsiteVisible) {
            this.toggleOffsite(true)
          }
        }
      },
      rescheduling(newVal, oldVal) {
        if (newVal && !oldVal) {
          this.toggleOffsite(false)
        }
        if (oldVal && !newVal) {
          if (this.offsiteVisible) {
            this.toggleOffsite(true)
          }
        }
      }
    },
    methods: {
      ...mapActions(['getBookings','getRooms', 'finishBooking', 'initializeAgenda', 'getExamTypes', 'getInvigilators']),
      ...mapMutations([
        'setCalendarSetup',
        'setClickedDate',
        'setEditedBooking',
        'setEditedBookingOriginal',
        'setSelectedExam',
        'setSelectionIndicator',
        'toggleBookingModal',
        'toggleEditBookingModal',
        'toggleOffsiteVisible',
        'toggleOtherBookingModal',
        'toggleScheduling',
        'toggleStartDateModalVisible',
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
        if (this.editedBooking) {
          this.toggleEditBookingModal(true)
          this.$refs.bookingcal.fireMethod('rerenderEvents')
          return
        }
        this.finishBooking()
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
        el.css('width', '85%')
        if (event.exam && view.name === 'listYear') {
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
          return this.filtered_calendar_events(this.searchTerm)
        }
        return this.calendarEvents
      },
      eventSelected(event, jsEvent, view) {
        if (this.scheduling || this.rescheduling || event.resourceId === '_offsite') {
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
      filterKeyPress(e) {
        if (e.keyCode === 13) {
          e.preventDefault()
        }
      },
      goToDate(date) {
        this.$refs.bookingcal.fireMethod('gotoDate', date)
      },
      initialize() {
        this.initializeAgenda()
        this.setSelectionIndicator(false)
        this.tempEvent = false
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
          if (this.selectedExam && Object.keys(this.selectedExam) > 0) {
            let { number_of_hours, number_of_minutes } = this.selectedExam.exam_type
            let endTime = new moment(event.start).add(number_of_hours, 'h')
                                                 .add(number_of_minutes, 'm')
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
          let i = booking.start.clone()
          let f = booking.end.clone()
          let duration = new moment(f).diff(new moment(i), 'h', true)
          let ii = event.start.clone()
          let ff = event.end.clone()
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
          this.tempEvent = true
          this.renderEvent(tempEvent)
          this.toggleEditBookingModal(true)
          this.setClickedDate(event)
          return
        }
        let selection = {
          start: new moment(event.start),
          resourceId: event.resource.id,
          id: '_cal$election'
        }
        if (this.scheduling) {
          if (this.selectedExam && Object.keys(this.selectedExam).length > 0) {
            this.unselect()
            selection.end = new moment(event.start).add(this.selectedExam.exam_type.number_of_hours, 'h')
                                                   .add(this.selectedExam.exam_type.number_of_minutes, 'm')
            selection.title = this.selectedExam.exam_name
            this.removeSavedSelection()
            this.toggleBookingModal(true)
            this.$root.$emit('showbookingmodal')
          } else {
            this.unselect()
            this.toggleOtherBookingModal(true)
            selection.title = 'New Event'
            selection.end = new moment(event.end)
          }
        }
        this.renderEvent(selection)
        event.start = new moment(selection.start)
        event.end = new moment(selection.end)
        this.setClickedDate(event)
      },
      today() {
        this.$refs.bookingcal.fireMethod('today')
      },
      toggleOffsite(bool) {
        this.toggleOffsiteVisible(bool)
        if (bool) {
          this.$refs.bookingcal.fireMethod('addResource', {
            id: '_offsite',
            title: 'Offsite',
            eventColor: '#F58B4C',
          })
        }
        if (!bool) {
          this.$refs.bookingcal.fireMethod('removeResource', '_offsite')
        }
      },
      unselect() {
        this.$refs.bookingcal.fireMethod('unselect')
        this.tempEvent = false
      },
      updateEvent(event, params) {
        Object.keys(params).forEach(key => {
          event[key] = params[key]
        })
        this.$refs.bookingcal.fireMethod('updateEvent', event)
      },
      viewRender(view, el) {
        if (view.name !== 'listYear') {
          if (view.name === 'agendaDay') {
            let title = moment(view.intervalStart).format('dddd MMMM D, YYYY')
            this.setCalendarSetup({ title, viewName: view.name })
          } else {
            this.setCalendarSetup({ title: view.title, viewName: view.name })
          }
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
        if(this.selectedExam && this.selectedExam.gotoDate) {
          this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
          this.goToDate(this.selectedExam.gotoDate)
        }
      },
    },
    destroyed() {
      this.setCalendarSetup(null)
      this.toggleScheduling(false)
      document.removeEventListener('keydown', this.filterKeyPress)
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
