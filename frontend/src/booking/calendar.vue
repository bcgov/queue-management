<template>
    <div :style="mainDivStyle">
      <SchedulingIndicator :cancel="cancel" />
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
  import 'fullcalendar/dist/fullcalendar.css'
  import 'fullcalendar-scheduler'
  import SchedulingIndicator from './scheduling-indicator'

  export default {
    name: 'Calendar',
    components: { SchedulingIndicator, BookingModal, DropdownCalendar, ExamInventoryModal, FullCalendar, OtherBookingModal },
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
        setup: {
          selectable: false,
          unselectCancel: '.modal, .modal-content',
          editable: false,
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          showNonCurrentDates: false,
          fixedWeekCount: false,
          navLinks: true,
          height: 'auto',
          timezone: 'local',
          defaultView: 'agendaWeek',
          views: {
            agendaDay: {
              allDaySlot: false,
              groupByResource: true,
            },
            agendaWeek: {
              allDaySlot: false,
              groupByDateAndResource: true,
            },
            month: {
              allDaySlot: false,
              groupByResource: false,
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
        },
      }
    },
    computed: {
      ...mapGetters(['calendar_events', 'room_resources']),
      ...mapState([
        'calendarSetup',
        'exams',
        'exam_types',
        'scheduling',
        'schedulingOther',
        'selectedExam',
        'showBookingModal',
        'showExamInventoryModal',
        'showSchedulingIndicator',
        'viewPortSizes',
      ]),
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
      events() {
        if (this.calendar_events.length > 0) {
          return this.calendar_events
        }
        return []
      },
    },
    destroyed() {
      this.setCalendarSetup(null)
    },
    methods: {
      ...mapActions(['getBookings', 'finishBooking', 'initializeAgenda', 'getExamTypes']),
      ...mapMutations([
        'setCalendarSetup',
        'setClickedDate',
        'setSelectedExam',
        'toggleBookingModal',
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
        //passed to child component SchedulingIndicator as prop
        this.finishBooking()
        this.options({name: 'selectable', value: false})
      },
      initialize() {
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
      mainDivStyle() {
        return {
          position: 'relative'
        }
      },
      month() {
        this.$refs.bookingcal.fireMethod('changeView', 'month')
      },
      goToDate(date) {
        this.$refs.bookingcal.fireMethod('gotoDate', date)
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
      selectEvent(event) {
        if (this.calendarSetup.viewName === 'month') {
          this.goToDate(event.start.local())
          this.agendaDay()
          return
        }
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
      today() {
        this.$refs.bookingcal.fireMethod('today')
      },
      viewRender(view, el) {
        this.setCalendarSetup({ title: view.title, viewName: view.name })
        if (view.name === 'basicDay') {
          this.$refs.bookingcal.fireMethod('changeView', 'agendaDay')
        }
        if (view.name === 'month') {
          let adj = 75
          if (this.scheduling || this.schedulingOther) {
            adj = 130
          }
          this.options({name: 'height', value: this.viewPortSizes.h - adj})
        }
        if (view.name === 'agendaDay' || view.name === 'agendaWeek' ) {
          this.options({name: 'height', value: 'auto'})
        }
      },
      unselect() {
        this.$refs.$bookingcal.fireMethod('unselect')
      }
    }
  }


</script>