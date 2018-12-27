<template>
    <div @mouseup="resetDrag"
         @click="resetDrag"
         style="position: relative; height: 100%; width: 100%">
      <keep-alive>
        <full-calendar ref="bookingcal"
                       key="bookingcal"
                       id="bookingcal"
                       class="q-calendar-margins"
                       @view-render="viewRender"
                       @mouseup="resetDrag"
                       @event-created="selectEvent"
                       @click="resetDrag"
                       :events="events"
                       :config="setup"></full-calendar>
      </keep-alive>
      <div class="exam-card"
           v-if="scheduling"
           :style="examCardStyle"
           @mousedown="startDrag"
           @mousemove="moveCard"
           @mouseup="resetDrag"
           ref="examCardDiv">
        <div style="display: flex; justify-content: space-between; border-radius: 24">
          <div class="mr-2">
            <span style="font-weight:600; font-size:1rem">Now</span><br>
            <span style="font-weight:600; font-size:1rem">Scheduling</span>
          </div>
          <div class="mr-3">
            <span><b>Exam: </b> {{ selectedExam.exam_name }}</span><br>
            <span><b>Writer: </b>{{ selectedExam.examinee_name }}</span><br>
            <span><b>Duration: </b>{{ `${selectedExam.exam_type.number_of_hours }HRS` }}</span><br>
          </div>
          <div style="margin-top: auto; margin-bottom: auto">
            <b-button @click="cancel"
                      class="btn-danger">Cancel</b-button>
          </div>
        </div>
      </div>
    <BookingModal />
    <ExamInventoryModal v-if="showExamInventoryModal" />
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState, } from 'vuex'
  import { FullCalendar } from 'vue-full-calendar'
  import BookingModal from './booking-modal'
  import DropdownCalendar from './dropdown-calendar'
  import ExamInventoryModal from './exam-inventory-modal'
  import Moment from 'moment'
  import 'fullcalendar/dist/fullcalendar.css'
  import 'fullcalendar-scheduler'

  export default {
    name: 'Calendar',
    components: { BookingModal, DropdownCalendar, ExamInventoryModal, FullCalendar, },
    mounted() {
      this.initialize()
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('today', () => { this.today() })
      this.$root.$on('month', () => { this.month() })
      this.$root.$on('agendaWeek', () => { this.agendaWeek() })
      this.$root.$on('agendaDay', () => { this.agendaDay() })
      this.$root.$on('initialize', () => { this.initialize() })
    },
    data() {
      return {
        initialEvent: true,
        clicked: false,
        top: 80,
        left: 10,
        setup: {
          editable: false,
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          showNonCurrentDates: false,
          fixedWeekCount: false,
          navLinks: true,
          timezone: 'local',
          defaultView: 'agendaWeek',
          views: {
            agendaDay: {
              allDaySlot: false,
            },
            agendaWeek: {
              allDaySlot: false,
            },
          },
          contentHeight: 'auto',
          resources: [],
          weekends: false,
          maxTime: '18:00:00',
          minTime: '07:00:00',
          header: {
            left: null,
            center: null,
            right: null
          },
          groupByResource: true,
        },
      }
    },
    computed: {
      ...mapGetters(['calendar_events']),
      ...mapState([
        'exams',
        'scheduling',
        'selectedExam',
        'showBookingModal',
        'showExamInventoryModal',
        'viewPortSizes',
      ]),
      events() {
        if (this.calendar_events.length > 0) {
          return this.calendar_events
        }
        return []
      },
      examCardStyle() {
        return {top: this.top+'px', left: this.left+'px'}
      },
      height() {
        return this.viewPortSizes.h
      },
    },
    destroyed() {
      this.setCalendarTitle(null)
    },
    methods: {
      ...mapActions(['initializeAgenda', 'getBookings']),
      ...mapMutations([
        'navigationVisible',
        'setCalendarTitle',
        'setClickedDate',
        'setSelectedDate',
        'setSelectedExam',
        'toggleBookingModal',
        'toggleCalendarControls',
        'toggleScheduling',
      ]),
      agendaDay() {
        this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
        this.$refs.bookingcal.fireMethod('option', 'groupByResource', true)
      },
      agendaWeek() {
        this.$refs.bookingcal.fireMethod('changeView', 'agendaWeek')
        this.$refs.bookingcal.fireMethod('option', 'groupByResource', true)
      },
      cancel() {
        this.toggleScheduling(false)
        this.navigationVisible(true)
        this.toggleCalendarControls(true)
        this.setSelectedExam(null)
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
          this.getBookings()
        })
      },
      month() {
        this.$refs.bookingcal.fireMethod('changeView', 'month')
        this.$refs.bookingcal.fireMethod('option', 'groupByResource', false)
      },
      moveCard(e) {
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
      prev() {
        this.$refs.bookingcal.fireMethod('prev')
      },
      resetDrag() {
        this.initialEvent = true
        this.clicked = false
      },
      selectEvent(event) {
        if (this.scheduling) {
          this.setClickedDate(event)
          this.toggleScheduling(false)
          this.toggleBookingModal(true)
        }
      },
      startDrag() {
        this.initialEvent = true
        this.clicked = true
      },
      today() {
        this.$refs.bookingcal.fireMethod('today')
      },
      viewRender(view, el) {
        this.$refs.bookingcal.fireMethod('option', 'height', this.height)
        this.setCalendarTitle({ title: view.title, view: view.name })
        if (view.name === 'basicDay') {
          this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
        }
        if (view.name === 'agendaWeek') {
          let days = el.find('th > a')
          let n = days.length
          for (let i = 1; i <= n; i++) {
            if (i <= 5) {
              let head = new Moment(view.intervalStart).add(i, 'days')
              days[i - 1].innerHTML = head.format(`D[/]ddd`)
            }
            if (i > 5 && i <=10) {
              let head = new Moment(view.intervalStart).add((i-5), 'days')
              days[i - 1].innerHTML = head.format(`D[/]ddd`)
            }
            if (i > 10) {
              let head = new Moment(view.intervalStart).add((i-10), 'days')
              days[i - 1].innerHTML = head.format(`D[/]ddd`)
            }
          }
        }
      },
    }
  }


</script>

<style scoped>
  .exam-card {
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