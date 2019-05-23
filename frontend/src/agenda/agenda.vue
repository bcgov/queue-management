<template>
  <div>
    <b-container fluid>
      <div v-if="examEvents.length === 0"
           class="ml-3 my-3 no-exam-notice">
        There are no exams scheduled for the week currently in view. <br>Use the Arrow Buttons above to view a
        different week or click <b class="mx-1">"This Week"</b> to instantly view the current week.
      </div>
    <template v-for="(date, i) in examDates">
      <b-container fluid style="background-color: white">
        <b-form-row class="mt-1">
          <b-col class="date-header-col">
            <span class="date-header">
              {{ examEvents.length > 0 ? date : 'No Exams Scheduled' }}
            </span>
          </b-col>
        </b-form-row>
        <b-form-row class="p-0" style="background-color: white; border-bottom: 1px solid lightgrey;">
          <b-col class="p-0 inner-col-table-style">
            <b-table :items="getExamItems(date)"
                     :fields="fields"
                     class="pb-0 mb-0"
                     small
                     fixed
                     hover>
              <template slot="start" slot-scope="row">
                {{ formatDetail(row.item.exam.booking.start_time) }}
              </template>

              <template slot="length" slot-scope="row">
                {{ duration(row.item) }}
              </template>

              <template slot="row-details" slot-scope="row">
                <span class="ml-2 mr-3" style="font-size: .9rem;">Location Details: </span>
                  {{ row.item.exam.offsite_location ? row.item.exam.offsite_location : null }}
              </template>

              <template slot="materials" slot-scope="row">
                <span v-if="row.item.exam.exam_received_date" class="good-2-go">YES</span>
                <span v-if="!row.item.exam.exam_received_date" class="no-way-jose">NO</span>
              </template>

              <template slot="invigilator" slot-scope="row">
                <span v-if="!showInvigilator(row.item)" class="no-way-jose">NOT ASSIGNED</span>
                <span v-if="showInvigilator(row.item)"
                      :style="row.item.exam.booking.invigilator_id ? null : {color: '#ff9f17'}">
                  {{ showInvigilator(row.item) }}
                </span>
              </template>

              <template slot="room" slot-scope="row">
                <span v-if="showLocation(row.item)">{{ showLocation(row.item) }}</span>
                <span v-if="!showLocation(row.item)"
                      @click="row.toggleDetails()"
                      class="toggle-link">{{ row.detailsShowing ? 'Hide' : 'Show' }}</span>
              </template>

              <template slot="writer" slot-scope="row">
                {{ showWriter(row.item) }}
              </template>
            </b-table>
          </b-col>
        </b-form-row>
      </b-container>
    </template>
    </b-container>
    <b-container fluid class="mt-3">
      <b-container fluid style="background-color: white" v-if="nonExamEvents.length > 0">
        <b-form-row class="mt-1">
          <b-col class="date-header-col-other"><span class="date-header">Non Exam Bookings</span></b-col>
        </b-form-row>
        <b-form-row class="p-0" style="background-color: white">
          <b-col class="p-0 inner-col-table-style">
            <b-table :items="nonExamEvents"
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
              <template slot="booking_contact_information" slot-scope="row">
                {{ row.item.booking_contact_information ? row.item.booking_contact_information : '–' }}
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
  import moment from 'moment'
  import Vue from 'vue'

  export default {
    name: 'Agenda',
    mounted() {
      this.initializeAgenda()
      this.$root.$on('next', () => { this.next() })
      this.$root.$on('prev', () => { this.prev() })
      this.$root.$on('today', () => { this.today() })
      this.weekStart = moment().day(1)
      this.updateButtonsDate()
    },
    destroyed() {
      this.setCalendarSetup(null)
    },
    data() {
      return {
        fields: [
          {key: 'start', label: 'Time', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'length', label:'Duration', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'room', label: 'Location', thStyle: 'width: 8%;font-size:.9rem;'},
          {key: 'exam.exam_type.exam_type_name', label: 'Exam Type', thStyle:'font-size:.9rem;'},
          {key: 'invigilator', thStyle: 'width: 10%;font-size:.9rem;'},
          {key: 'materials', label: 'Materials?', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'exam.exam_name', label: 'Exam Name', thStyle: 'font-size:.9rem;'},
          {key: 'writer', label: "Candidate's Name", thStyle: 'font-size:.9rem;'},
          {key: 'exam.notes', label: 'Notes', thStyle: 'font-size:.9rem;'},
        ],
        fieldsOther: [
          {key: 'date', thStyle: 'width: 11%;font-size:.9rem;'},
          {key: 'start', label: 'Start', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'end', label: 'End', thStyle: 'width: 6%;font-size:.9rem;'},
          {key: 'room.room_name', label: 'Room', thStyle: 'font-size:.9rem;' },
          {key: 'title', label: 'Event Title/Booking Party', thStyle: 'font-size:.9rem;' },
          {key: 'booking_contact_information', thStyle: 'font-size:.9rem;'},
        ],
        weekStart: null,
      }
    },
    computed: {
      ...mapState(['calendarEvents', 'calendarSetup', ]),
      examDates() {
        if (this.examEvents && this.examEvents.length > 0) {
          let dates = this.examEvents.map(ex => ex.start)
          let output = []
          for (let date of dates) {
            let d = moment(date).format('dddd, MMM Do, YYYY').toString()
            if (!output.includes(d)) {
              output.push(d)
            }
          }
          return output
        }
      },
      events() {
        if (this.calendarEvents.length > 0 && this.weekStart) {
          let events = this.calendarEvents
          let weekEnd = this.weekStart.clone().add(4, 'day')
          return events.filter(e =>
            moment(e.start).isSameOrAfter(this.weekStart, 'day') &&
            moment(e.start).isSameOrBefore(weekEnd, 'day')
          ).sort(function(a,b) {
            let A = moment(a.start).clone()
            let B = moment(b.start).clone()
            if ( A.isSame(B)) {
              return 0
            }
            if (A.isBefore(B)) {
              return -1
            }
            return 1
          })
        }
        return []
      },
      examEvents() {
        if (this.events && this.events.length > 0) {
          return this.events.filter(e => !!e.exam )
        }
        return []
      },
      teseter() {
        return this.examEvents
      },
      nonExamEvents() {
        if (this.events && this.events.length > 0) {
          let nonExams = Object.assign([], this.events.filter(e => !e.exam ))
          nonExams.forEach(ev => {
            ev.start = moment(ev.start)
            ev.end = moment(ev.end)
          })
          return nonExams
        }
        return []
      },
    },
    methods: {
      ...mapActions(['initializeAgenda']),
      ...mapMutations(['setCalendarSetup']),
      duration({exam}) {
        let start = moment(exam.booking.start_time).clone()
        let end = moment(exam.booking.end_time).clone()
        return `${end.diff(start, 'hours')} hrs`
      },
      formatDetail(d) {
        return moment(d).clone().format('h:mm a')
      },
      formatHeader(d) {
        return moment(d).clone().format('dddd, MMM Do, YYYY')
      },
      next() {
        Vue.set(
          this,
          'weekStart',
          this.weekStart.clone().add(7, 'day')
        )
        this.updateButtonsDate()
      },
      prev() {
        Vue.set(
          this,
          'weekStart',
          this.weekStart.clone().subtract(7, 'day')
        )
        this.updateButtonsDate()

      },
      getExamItems(dateString) {
        return this.examEvents.filter(exam => moment(exam.start).clone().format('dddd, MMM Do, YYYY') === dateString)
      },
      showInvigilator({exam}) {
        if (exam.booking.sbc_staff_invigilated) {
          return 'SBC Staff'
        }
        if (exam.booking.invigilator_id) {
          return exam.booking.invigilator.invigilator_name
        }
        return false
      },
      showLocation({exam}) {
        if (exam.offsite_location) {
          return false
        }
        if (exam.booking && exam.booking.room_id) {
          return exam.booking.room.room_name
        }
      },
      showWriter({exam}) {
        if (exam.exam_type.exam_type_name === 'Monthly Session Exam') {
          return 'Monthly Session'
        }
        if (exam.exam_type.group_exam_ind) {
          return 'Group Exam'
        }
        if (exam.examinee_name) {
          return exam.examinee_name
        }
        return 'Other Exam'
      },
      today() {
        Vue.set(
          this,
          'weekStart',
          moment().day(1)
        )
        this.updateButtonsDate()
      },
      updateButtonsDate() {
        this.$nextTick(function() {
          let d = this.weekStart
          let text = `Week of ${d.clone().format('MMM Do, YYYY')}`
          this.setCalendarSetup({title: text})
        })
      },
    }
  }
</script>

<style scoped>
  .good-2-go {
    color: green;
  }
  .no-way-jose {
    color: red;
  }
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
  .toggle-link {
    color: blue;
    cursor: pointer;
    text-decoration: underline;
  }
  .no-exam-notice {
    width: 75%;
    background-color: #cce5ff;
    border-radius: 4px;
    padding: 8px 8px 8px 8px;
    color: #0b2934;
    font-size: 1rem;
  }
</style>
