<template>
    <div style="position: relative; height: 100%; width: 100%">
      <keep-alive>
        <full-calendar ref="bookingcal"
                       key="bookingcal"
                       id="bookingcal"
                       class="q-calendar-margins"
                       @view-render="viewRender"
                       @event-created="selectEvent"
                       :events="events"
                       :config="setup"></full-calendar>
      </keep-alive>
      <div class="scheduling-indicator"
           v-if="showSchedulingIndicator"
           :style="indicatorStyle"
           @mousedown="startDrag"
           @mousemove="moveCard"
           @mouseup="resetDrag">
        <div style="display: flex; justify-content: space-between; border-radius: 24">
          <div class="mr-2">
            <span style="font-weight:600; font-size:1rem">Now</span><br>
            <span style="font-weight:600; font-size:1rem">Scheduling</span>
          </div>
          <div class="mr-3" v-if="scheduling">
            <span><b>Exam: </b> {{ selectedExam.exam_name }}</span><br>
            <span><b>Writer: </b>{{ selectedExam.examinee_name }}</span><br>
            <span><b>Duration: </b>{{ `${selectedExam.exam_type.number_of_hours }HRS` }}</span><br>
          </div>
          <div v-else>
            <span><b>Non-Exam Event</b></span><br>
            <span class="smaller-font">Click and Drag to select</span><br>
            <span class="smaller-font">a time on the calendar</span><br>
          </div>
          <div style="margin-top: auto; margin-bottom: auto">
            <b-button @click="cancel"
                      class="btn-danger ml-3">Cancel</b-button>
          </div>
        </div>
      </div>
    <BookingModal />
    <ExamInventoryModal v-if="showExamInventoryModal" />
    <OtherBookingModal />
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState, } from 'vuex'
  import { FullCalendar } from 'vue-full-calendar'
  import BookingModal from './booking-modal'
  import DropdownCalendar from './dropdown-calendar'
  import OtherBookingModal from './other-booking-modal'
  import ExamInventoryModal from './exam-inventory-modal'
  import moment from 'moment'
  import _ from 'lodash'
  import 'fullcalendar/dist/fullcalendar.css'
  import 'fullcalendar-scheduler'

  export default {
    name: 'Calendar',
    components: { BookingModal, DropdownCalendar, ExamInventoryModal, FullCalendar, OtherBookingModal },
    mounted() {
      this.initialize()
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('today', () => { this.today() })
      this.$root.$on('month', () => { this.month() })
      this.$root.$on('unselect', () => { this.unselect() })
      this.$root.$on('agendaWeek', () => { this.agendaWeek() })
      this.$root.$on('agendaDay', () => { this.agendaDay() })
      this.$root.$on('options', (option) => { this.options(option) })
      this.$root.$on('initialize', () => { this.initialize() })
    },
    data() {
      return {
        initialEvent: true,
        clicked: false,
        top: 80,
        left: 10,
        setup: {
          unselectCancel: '.modal, .modal-content',
          selectable: false,
          editable: false,
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          showNonCurrentDates: false,
          fixedWeekCount: false,
          navLinks: true,
          height: 'auto',
          timezone: 'local',
          defaultView: 'agendaWeek',
          resourceAreaWidth: 100,
          views: {
            timelineDay: {
              slotWidth: 40,
              allDaySlot: false,
            },
            agendaDay: {
              allDaySlot: false,
            },
            agendaWeek: {
              allDaySlot: false,
            },
          },
          resources: [],
          weekends: false,
          maxTime: '18:00:00',
          minTime: '07:00:00',
          header: {
            left: null,
            center: null,
            right: null
          },
          groupByDateAndResource: false,
          groupByResource: false,
        },
      }
    },
    computed: {
      ...mapGetters(['calendar_events']),
      ...mapState([
        'exams',
        'scheduling',
        'schedulingOther',
        'selectedExam',
        'showBookingModal',
        'showExamInventoryModal',
        'showSchedulingIndicator',
        'viewPortSizes',
      ]),
      events() {
        if (this.calendar_events.length > 0) {
          return this.calendar_events
        }
        return []
      },
      indicatorStyle() {
        return {top: this.top+'px', left: this.left+'px'}
      },
    },
    destroyed() {
      this.setCalendarTitle(null)
    },
    methods: {
      ...mapActions(['getBookings', 'finishBooking', 'initializeAgenda',]),
      ...mapMutations([
        'navigationVisible',
        'setCalendarTitle',
        'setClickedDate',
        'setSelectedDate',
        'setSelectedExam',
        'toggleBookingModal',
        'toggleCalendarControls',
        'toggleOtherBookingModal',
        'toggleScheduling',
        'toggleSchedulingIndicator',
        'toggleSchedulingOther'
      ]),
      agendaDay() {
        this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
      },
      agendaWeek() {
        this.$refs.bookingcal.fireMethod('changeView', 'agendaWeek')
      },
      cancel() {
        this.finishBooking()
        this.unselect()
        this.options({name: 'selectable', value: false})
      },
      initialize() {
        this.initializeAgenda().then( rooms => {
          rooms.forEach( room => {
            let roomObj = {
              id: room.room_id,
              title: room.room_name,
              eventColor: room.color
            }
            this.$refs.bookingcal.fireMethod('addResource', roomObj)
          })
          this.setupResourceView(rooms)
          this.getBookings()
        })
      },
      month() {
        this.$refs.bookingcal.fireMethod('changeView', 'month')
        this.$refs.bookingcal.fireMethod('option', 'groupByResource', false)
      },
      moveCard(e) {
        e.preventDefault()
        if (this.clicked) {
          if (this.initialEvent === true) {
            this.offsetX = e.clientX
            this.offsetY = e.clientY
            this.initialEvent = false
          }
          let adjX = e.clientX - this.offsetX
          let adjY = e.clientY - this.offsetY
          this.offsetX = e.clientX
          this.offsetY = e.clientY
          this.left += adjX
          this.top += adjY
        }
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
      resetDrag(e) {
        e.preventDefault()
        this.initialEvent = true
        this.clicked = false
      },
      selectEvent(event) {
        if (this.scheduling) {
          this.setClickedDate(event)
          this.toggleSchedulingIndicator(false)
          this.toggleBookingModal(true)
        }
        if (this.schedulingOther) {
          this.setClickedDate(event)
          this.toggleSchedulingIndicator(false)
          this.toggleOtherBookingModal(true)
        }
      },
      setupResourceView(rooms) {
        if (rooms.length <= 3) {
          this.options({name:'groupByDateAndResource', value: true})
        }
        if (rooms.length > 3 && rooms.length <= 5) {
          this.options({name:'groupByResource', value: true})
        }
      },
      startDrag(e) {
        e.preventDefault()
        this.initialEvent = true
        this.clicked = true
      },
      today() {
        this.$refs.bookingcal.fireMethod('today')
      },
      viewRender(view, el) {
        if (this.room_resources && this.room_resources.length > 0) {
          this.setupResourceView(this.room_resources)
        }
        this.setCalendarTitle({ title: view.title, view: view.name })
        if (view.name === 'basicDay') {
          this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
        }
        if (view.name === 'agendaWeek') {
          //days = refs to the text dates displayed in the column headers (ie. the day of the week and month)
          let days = el.find('th > a')
          let length = days.length
          //weeksArray is empty array with as many slots as the number of times Mon-Fri dates are rendered in header
          //eg. 5x per room_resource when groupByDateAndResource===true
          let weeksArray = Array(length / 5)
          //fill the empty slots with [1,2,3,4,5] and flaten
          //now is a template for calculating the day based on days from interval start, left to right, across headers
          _.fill(weeksArray, [1,2,3,4,5])
          let flaten = (arr) => [].concat(...arr)
          let addDaysArray = flaten(weeksArray)
          for (let i = 0; i < length; i++) {
            let header = new moment(view.intervalStart).add(addDaysArray[i], 'days')
            days[i].innerHTML = header.format(`D[/]ddd`)
          }
        }
      },
      unselect() {
        this.$refs.$bookingcal.fireMethod('unselect')
      }
    }
  }


</script>

<style scoped>
  .smaller-font {
    font-size: .75rem;
  }
  .scheduling-indicator {
    position: absolute;
    border: 1px solid grey;
    border-radius: 7px;
    box-shadow: 4px 4px 5px 0px grey;
    background-color: white;
    padding: 14px;
    width: 300;
    z-index: 2000;
  }
</style>