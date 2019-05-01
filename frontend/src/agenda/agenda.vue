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
      <b-alert show v-if="exams.length === 0" variant="primary">
        There are no exam events to display.  <b>Note:</b> The Agenda only shows events scheduled on or after today's date.
      </b-alert>
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
                <span v-if="row.item.exam && row.item.exam.exam_type">
                {{ row.item.exam.exam_type.number_of_hours }} hrs</span>
              </template>

              <template slot="row-details" slot-scope="row">
                <span class="ml-3 pl-3">Location: {{ row.item.exam.offsite_location }} </span>
              </template>

              <template slot="materials" slot-scope="row">
                <span v-if="!row.item.exam.exam_received_date" style="color: red;">No</span>
                <span v-if="row.item.exam.exam_received_date">Yes</span>
              </template>

              <template slot="invigilator" slot-scope="row">
                <template v-if="row.item.exam && row.item.exam.booking">
                  <span v-if="!row.item.exam.booking.invigilator_id && !row.item.exam.booking.sbc_staff_invigilated"
                        style="color: red;">Not Assigned</span>
                  <span v-if="row.item.exam.booking.invigilator_id">
                    {{ row.item.exam.booking.invigilator.invigilator_name }}
                  </span>
                  <span v-if="row.item.exam.booking.sbc_staff_invigilated"
                        class="text-warning">
                    SBC Staff
                  </span>
                </template>
              </template>

              <template slot="room" slot-scope="row">
                <template v-if="row.item.resourceId === '_offsite'">
                  <b-badge  variant="info"
                            style="cursor: pointer;"
                            v-if="!row.detailsShowing"
                            @click="row.toggleDetails()">Offsite</b-badge>
                  <b-btn class="btn-link btn-sm m-0 p-0"
                         style="border: none;"
                         @click="row.toggleDetails()"
                         v-if="row.detailsShowing">Hide</b-btn>
                </template>
                <template v-else>
                  <span v-if="row.item.exam && row.item.exam.booking">
                  {{ row.item.exam.booking.room ? row.item.exam.booking.room.room_name : 'Not booked' }}</span>
                </template>
              </template>

              <template slot="writer" slot-scope="row">
                <span v-if="!row.item.exam.exam_type.group_exam_ind &&
                            !row.item.exam.exam_type.exam_type_name.includes('Monthly Session Exam')">
                  {{ row.item.exam.examinee_name }}
                </span>
                <span v-else>
                  –
                </span>
              </template>
            </b-table>
          </b-col>
        </b-form-row>
      </b-container>
    </template>
    </b-container>
    <b-container fluid class="mt-3">
      <b-container fluid style="background-color: white" v-if="others.length > 0">
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
      this.initializeAgenda()
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
          {key: 'start', label: 'Time', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'length', label:'Duration', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'room',  thStyle: 'width: 8%;font-size:.9rem;'},
          {key: 'exam.exam_type.exam_type_name', label: 'Exam Type', thStyle:'font-size:.9rem;'},
          {key: 'invigilator', thStyle: 'width: 10%;font-size:.9rem;'},
          {key: 'materials', label: 'Materials?', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'title', thStyle: 'font-size:.9rem;'},
          {key: 'writer', label: "Candidate's Name", thStyle: 'font-size:.9rem;'},
          {key: 'notes', thStyle: 'font-size:.9rem;'},
        ],
        fieldsOther: [
          {key: 'date', thStyle: 'width: 11%;font-size:.9rem;'},
          {key: 'start', label: 'Start', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'end', label: 'End', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'room.room_name', label: 'Room', thStyle: 'font-size:.9rem;' },
          {key: 'title', thStyle: 'font-size:.9rem;' },
          {key: 'notes', thStyle: 'font-size:.9rem;'},
        ],
        config: {
          timezone: 'local',
          schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
          showNonCurrentDates: false,
          fixedWeekCount: true,
          navLinks: true,
          defaultView: 'listWeek',
          resources: (setResources) => {
            this.getRooms().then( resources => {
              setResources(resources)
            })
          },
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
      ...mapGetters(['room_resources']),
      ...mapState(['calendarEvents','calendarSetup']),
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
      ...mapActions(['initializeAgenda', 'getBookings', 'getRooms']),
      ...mapMutations([
        'setCalendarSetup',
        'toggleBookRoomModal',
      ]),
      events() {
        if (this.calendarEvents.length > 0) {
          if (this.groupFilter === 'individual') {
            return this.calendarEvents.filter(event => !event.resourceId === '_offsite')
          } else if (this.groupFilter === 'group') {
            return this.calendarEvents.filter(event => event.resourceId === '_offsite')
          } else {
            return this.calendarEvents
          }
        }
        return []
      },
      setDate(d) {
        return new moment(d).format('dddd, MMMM Do, YYYY')
      },
      viewRender(view, el) {
        this.setCalendarSetup({ title: view.title, view: view.name })
      },
      eventRender(event, el, view) {
        if (event.exam) {
          let list = this.exams.length > 0 ? this.exams.map(exam => exam.id) : []
          if (!list.includes(event.id)) {
            let now = moment()
            if (event.start.isSameOrAfter(now, 'day')) {
              this.exams.push(event)
            }

          }
        }
        if (!event.exam) {
          let list = this.others.length > 0 ? this.others.map(other => other.id) : []
          if (!list.includes(event.id)) {
            let now = moment()
            if (event.start.isSameOrAfter(now, 'day')) {
              this.others.push(event)
            }
          }
        }
      },
      next() {
        this.exams = []
        this.others = []
        this.$nextTick(function() {
          this.$refs.agendacal.fireMethod('next')
        })

      },
      prev() {
        this.exams = []
        this.others = []
        this.$nextTick(function() {
          this.$refs.agendacal.fireMethod('prev')
        })
      },
      today() {
        this.exams = []
        this.others = []
        this.$nextTick(function() {
          this.$refs.agendacal.fireMethod('today')
        })
      },
    }
  }
</script>

<style scoped>
  .header-table-special {
    color: red !important;
  }
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
