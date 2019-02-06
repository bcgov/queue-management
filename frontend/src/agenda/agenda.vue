<template>
  <div>
    <full-calendar ref="agendacal"
                   v-show="false"
                   key="agendacal"
                   class="q-calendar-margins"
                   @event-render="eventRender"
                   @view-render="viewRender"
                   :events="events()"
                   :config="config"></full-calendar>
    <b-container fluid>
    <template v-for="date in displayDates">
      <b-container fluid style="background-color: white">
        <b-form-row class="mt-1">
          <b-col class="date-header-col">
            <span class="date-header">{{ exams.length > 0 ? setDate(date) : 'No Exams Scheduled' }}</span>
          </b-col>
        </b-form-row>
        <b-form-row class="p-0" style="background-color: white; border-bottom: 1px solid lightgrey;">
          <b-col class="p-0 inner-col-table-style">
            <b-table :items="exams.filter(ev=>ev.start.format('YYYY-MM-DD') == date)"
                     class="pb-0 mb-0"
                     small
                     fixed
                     hover
                     :fields="fields">
              <template slot="start" slot-scope="row">
                {{ row.item.start.format('h:mm a') }}
              </template>

              <template slot="length" slot-scope="row">
                {{ row.item.exam.exam_type.number_of_hours }} hrs
              </template>

              <template slot="materials" slot-scope="row">
                <span v-if="!row.item.exam.exam_received" style="color: red;">No</span>
                <span v-if="row.item.exam.exam_received">Yes</span>
              </template>

              <template slot="invigilator" slot-scope="row">
                <span v-if="!row.item.exam.booking.invigilator_id" style="color: red;">Not Scheduled </span>
                <span v-if="row.item.exam.booking.invigilator_id">
                  {{ row.item.exam.booking.invigilator.invigilator_name }}
                </span>
              </template>

              <template slot="room" slot-scope="row">
                <template v-if="row.item.resourceId === '_offsite'">
                  <b-badge  variant="info">Offsite</b-badge>
                </template>
                <template v-else>
                  {{ row.item.exam.booking.room ? row.item.exam.booking.room.room_name : 'Not booked' }}
                </template>
              </template>

              <template slot="writer" slot-scope="row">
                {{ row.item.exam.examinee_name }}
              </template>
            </b-table>
          </b-col>
        </b-form-row>
      </b-container>
    </template>
    </b-container>
    <b-container fluid class="mt-3">
      <b-container fluid style="background-color: white">
        <b-form-row class="mt-1">
          <b-col class="date-header-col-other"><span class="date-header">Non Exam Bookings</span></b-col>
        </b-form-row>
        <b-form-row class="p-0" style="background-color: white">
          <b-col class="p-0 inner-col-table-style">
            <b-table :items="others"
                     small
                     fixed
                     hover
                     :fields="fieldsOther">
              <template slot="date" slot-scope="row">
                {{ row.item.start.format('ddd MMM Do, YYYY') }}
              </template>
              <template slot="start" slot-scope="row">
                {{ row.item.start.format('h:mm a') }}
              </template>
              <template slot="end" slot-scope="row">
                {{ row.item.end.format('h:mm a') }}
              </template>
            </b-table>
          </b-col>
        </b-form-row>
      </b-container>
    </b-container>
  </div>
</template>

<script>
  import { mapState, mapMutations, mapActions, mapGetters } from 'vuex'
  import { FullCalendar } from 'vue-full-calendar'
  import 'fullcalendar/dist/fullcalendar.css'
  import 'fullcalendar-scheduler'
  import moment from 'moment'

  export default {
    name: 'Agenda',
    components: { FullCalendar },
    mounted() {
      this.initialize()
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('today', () => { this.today() })
      this.$root.$on('listWeek', () => { this.listWeek() })
      this.$root.$on('listDay', () => { this.listDay() })
    },
    destroyed() {
      this.setCalendarSetup(null)
      this.exams = []
      this.others = []
    },
    data() {
      return {
        exams: [],
        others: [],
        rendered: false,
        fields: [
          {key: 'start', label: 'Time', thStyle: 'width: 6%'},
          {key: 'length', label:'Duration', thStyle: 'width: 6%'},
          {key: 'room',  thStyle: 'width: 8%'},
          {key: 'exam.exam_type.exam_type_name', label: 'Exam Type'},
          {key: 'invigilator', thStyle: 'width: 10%'},
          {key: 'materials', label: 'Materials?', thStyle: 'width: 6%'},
          {key: 'title' },
          {key: 'writer', label: "Writer's Name"},
          {key: 'notes'},
        ],
        fieldsOther: [
          {key: 'date', thStyle: 'width: 11%'},
          {key: 'start', label: 'Start', thStyle: 'width: 6%'},
          {key: 'end', label: 'End', thStyle: 'width: 6%'},
          {key: 'room.room_name', label: 'Room'},
          {key: 'title' },
          {key: 'notes'},
        ],
        config: {
          timezone: 'local',
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          showNonCurrentDates: false,
          fixedWeekCount: true,
          navLinks: true,
          defaultView: 'listWeek',
          resources: [],
          listDayFormat: 'dddd, MMM Do',
          views: {
            listDay: {
              allDaySlot: false,
              listDayAltFormat: '[Invigilator]',
            },
            listWeek: {
              allDaySlot: false,
              listDayAltFormat: null,
            },
          },
          height: 'auto',
          weekends: false,
          header: {
            left: null,
            center: null,
            right: null
          },
          groupByDateAndResource: true
        },
      }
    },
    computed: {
      ...mapGetters(['calendar_events', 'room_resources']),
      ...mapState(['calendarSetup']),
      displayDates() {
        let output = []
        this.exams.sort(function(a,b) {
          if (a.start.isSame(b.start)) {
            return 0
          }
          if (a.start.isBefore(b.start)) {
            return -1
          }
          return 1
        })
        this.exams.forEach(exam => {
          let d = exam.start.format('YYYY-MM-DD')
          if (!output.includes(d)) {
            output.push(d)
          }
        })
        return output
      }
    },
    methods: {
      ...mapActions(['initializeAgenda', 'getBookings']),
      ...mapMutations([
        'setCalendarSetup',
        'toggleBookRoomModal',
      ]),
      events() {
        if (this.calendar_events.length > 0) {
          if (this.groupFilter === 'individual') {
            return this.calendar_events.filter(event => !event.resourceId === '_offsite')
          } else if (this.groupFilter === 'group') {
            return this.calendar_events.filter(event => event.resourceId === '_offsite')
          } else {
            return this.calendar_events
          }
        }
        return []
      },
      setDate(d) {
        return new moment(d).format('dddd, MMMM Do, YYYY')
      },
      initialize() {
        this.initializeAgenda().then( rooms => {
          rooms.forEach( room => {
            this.$refs.agendacal.fireMethod('addResource', room)
          })
          this.getBookings()
        })
      },
      viewRender(view, el) {
        this.setCalendarSetup({ title: view.title, view: view.name })
      },
      eventRender(event, el, view) {
        if (Object.keys(event).includes('exam')) {
          let list = this.exams.length > 0 ? this.exams.map(exam => exam.id) : []
          if (!list.includes(event.id)) {
            this.exams.push(event)
          }
        }
        if (!Object.keys(event).includes('exam')) {
          let list = this.others.length > 0 ? this.others.map(other => other.id) : []
          if (!list.includes(event.id)) {
            this.others.push(event)
          }
        }
      },
      next() {
        this.exams = []
        this.others = []
        this.$refs.agendacal.fireMethod('next')
      },
      prev() {
        this.exams = []
        this.others = []
        this.$refs.agendacal.fireMethod('prev')

      },
      today() {
        this.exams = []
        this.others = []
        this.$refs.agendacal.fireMethod('today')
      },
      listDay() {
        this.exams = []
        this.others = []
        this.$refs.agendacal.fireMethod('changeView', 'listDay')

      },
      listWeek() {
        this.exams = []
        this.others = []
        this.$refs.agendacal.fireMethod('changeView', 'listWeek')
      },
    }
  }
</script>

<style scoped>
  .exam-title {
    font-weight: 500 !important;
    font-size: 1rem !important;
  }
  .inner-col-table-style {

    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
  }
  .date-header {
    font-size: .9rem;
    font-weight: 300;
  }
  .date-header-col {
     background-color: lightgrey;
     color: black;
     padding: 3px 3px 2px 6px;
   }
  .date-header-col-other {
    background-color: slategray;
    color: white;
    padding: 3px 3px 2px 6px;
  }
</style>