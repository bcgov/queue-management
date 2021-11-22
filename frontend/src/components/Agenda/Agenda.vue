<template>
  <div>
    <b-container fluid>
      <div v-if="examEvents.length === 0" class="ml-3 my-3 no-exam-notice">
        There are no exams scheduled for the week currently in view.
        <br />Use the Arrow Buttons above to view a
        different week or click
        <strong class="mx-1">"This Week"</strong> to instantly view the current week.
      </div>
      <template v-for="(date, i) in examDates">
        <b-container fluid style="background-color: white" v-bind:key="{i}">
          <b-form-row class="mt-1">
            <b-col class="date-header-col">
              <span class="date-header">{{ examEvents.length > 0 ? date : 'No Exams Scheduled' }}</span>
            </b-col>
          </b-form-row>
          <b-form-row
            class="p-0"
            style="background-color: white; border-bottom: 1px solid lightgrey;"
          >
            <b-col class="p-0 inner-col-table-style">
              <b-table
                :items="getExamItems(date)"
                :fields="fields"
                class="pb-0 mb-0"
                small
                fixed
                hover
              >
                <template
                  #cell(start)="row"
                >{{ formatDetail(row.item.exam.booking.start_time) }}</template>

                <template #cell(length)="row">{{ duration(row.item) }}</template>

                <template #cell(row-details)="row">
                  <span class="ml-2 mr-3" style="font-size: .9rem;">Location Details:</span>
                  {{ row.item.exam.offsite_location ? row.item.exam.offsite_location : null }}
                </template>

                <template #cell(materials)="row">
                  <span v-if="row.item.exam.exam_received_date" class="good-2-go">YES</span>
                  <span v-if="!row.item.exam.exam_received_date" class="no-way-jose">NO</span>
                </template>

                <template #cell(invigilator)="row">
                  <span
                    v-if="showInvigilator(row.item).length == 0"
                    class="no-way-jose"
                  >NOT ASSIGNED</span>
                  <span
                    v-if="showInvigilator(row.item).length > 0"
                    v-for="invigilator in showInvigilator(row.item)"
                    :style="row.item.exam.booking.invigilators ? null : {color: '#ff9f17'}"
                  >
                    {{ invigilator }}
                    <br />
                  </span>
                </template>

                <template #cell(shadow_invigilator)="row">
                  <span v-if="!showShadowInvigilator(row.item)">-</span>
                  <span
                    v-else-if="showShadowInvigilator(row.item)"
                  >{{ showShadowInvigilator(row.item) }}</span>
                </template>

                <template #cell(room)="row">
                  <span v-if="showLocation(row.item)">{{ showLocation(row.item) }}</span>
                  <span
                    v-if="!showLocation(row.item)"
                    @click="row.toggleDetails()"
                    class="toggle-link"
                  >{{ row.detailsShowing ? 'Hide' : 'Show' }}</span>
                </template>

                <template #cell(writer)="row">{{ showWriter(row.item) }}</template>
              </b-table>
            </b-col>
          </b-form-row>
        </b-container>
      </template>
    </b-container>
    <b-container fluid class="mt-3">
      <b-container fluid style="background-color: white" v-if="nonExamEvents.length > 0">
        <b-form-row class="mt-1">
          <b-col class="date-header-col-other">
            <span class="date-header">Non Exam Bookings</span>
          </b-col>
        </b-form-row>
        <b-form-row class="p-0" style="background-color: white">
          <b-col class="p-0 inner-col-table-style">
            <b-table :items="nonExamEvents" small fixed hover :fields="fieldsOther">
              <template #cell(date)="row">{{ row.item.start.format('ddd MMM Do, YYYY') }}</template>
              <template #cell(start)="row">{{ row.item.start.format('h:mm a') }}</template>
              <template
                #cell(booking_contact_information)="row"
              >{{ row.item.booking_contact_information ? row.item.booking_contact_information : '–' }}</template>
              <template #cell(end)="row">{{ row.item.end.format('h:mm a') }}</template>
            </b-table>
          </b-col>
        </b-form-row>
      </b-container>
    </b-container>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'

import moment from 'moment'

@Component({})
export default class Agenda extends Vue {
  @State('calendarEvents') private calendarEvents!: any
  @State('calendarSetup') private calendarSetup!: any
  @State('invigilators') private invigilators!: any

  @Getter('invigilator_multi_select') private invigilator_multi_select!: any;
  @Getter('all_invigilator_options') private all_invigilator_options!: any;

  @Action('initializeAgenda') public initializeAgenda: any
  @Action('getInvigilators') public getInvigilators: any

  @Mutation('setCalendarSetup') public setCalendarSetup: any

  private fields: any = [
    { key: 'exam.event_id', label: 'Event ID', thStyle: 'width: 8%;font-size:.9rem;' },
    { key: 'start', label: 'Time', thStyle: 'width: 6%;font-size:.9rem;' },
    { key: 'length', label: 'Duration', thStyle: 'width: 6%;font-size:.9rem;' },
    { key: 'room', label: 'Location', thStyle: 'width: 8%;font-size:.9rem;' },
    { key: 'exam.exam_type.exam_type_name', label: 'Exam Type', thStyle: 'font-size:.9rem;' },
    { key: 'exam.exam_method', label: 'Exam Method', thStyle: 'font-size:.9rem;' },
    { key: 'invigilator', thStyle: 'width: 10%;font-size:.9rem;' },
    { key: 'shadow_invigilator', thStyle: 'width: 10%;font-size:.9rem;' },
    { key: 'materials', label: 'Materials?', thStyle: 'width: 6%;font-size:.9rem;' },
    { key: 'exam.exam_name', label: 'Exam Name', thStyle: 'font-size:.9rem;' },
    { key: 'writer', label: 'Candidate Name', thStyle: 'font-size:.9rem;' },
    { key: 'exam.notes', label: 'Notes', thStyle: 'font-size:.9rem;' }
  ]

  private fieldsOther: any = [
    { key: 'date', thStyle: 'width: 11%;font-size:.9rem;' },
    { key: 'start', label: 'Start', thStyle: 'width: 6%;font-size:.9rem;' },
    { key: 'end', label: 'End', thStyle: 'width: 6%;font-size:.9rem;' },
    { key: 'room.room_name', label: 'Room', thStyle: 'font-size:.9rem;' },
    { key: 'title', label: 'Event Title/Booking Party', thStyle: 'font-size:.9rem;' },
    { key: 'booking_contact_information', thStyle: 'font-size:.9rem;' }
  ]

  private weekStart: any = null

  get examDates () {
    if (this.examEvents && this.examEvents.length > 0) {
      const dates = this.examEvents.map(ex => ex.start)
      const output: any = []
      for (const date of dates) {
        const d = moment(date).format('dddd, MMM Do, YYYY').toString()
        if (!output.includes(d)) {
          output.push(d)
        }
      }
      return output
    }
  }

  get events () {
    if (this.calendarEvents.length > 0 && this.weekStart) {
      const events = this.calendarEvents
      const weekEnd = this.weekStart.clone().add(4, 'day')
      return events.filter((e:any) =>
        moment(e.start).isSameOrAfter(this.weekStart, 'day') &&
        moment(e.start).isSameOrBefore(weekEnd, 'day')
      ).sort(function (a: any, b: any) {
        const A = moment(a.start).clone()
        const B = moment(b.start).clone()
        if (A.isSame(B)) {
          return 0
        }
        if (A.isBefore(B)) {
          return -1
        }
        return 1
      })
    }
    return []
  }

  get examEvents () {
    if (this.events && this.events.length > 0) {
      return this.events.filter(e => !!e.exam)
    }
    return []
  }

  get teseter () {
    return this.examEvents
  }

  get nonExamEvents () {
    if (this.events && this.events.length > 0) {
      const nonExams = Object.assign([], this.events.filter(e => !e.exam))
      nonExams.forEach(ev => {
        ev.start = moment(ev.start)
        ev.end = moment(ev.end)
      })
      return nonExams
    }
    return []
  }

  private duration (data: any) {
    const { exam } = data
    const start = moment(exam.booking.start_time).clone()
    const end = moment(exam.booking.end_time).clone()
    return `${end.diff(start, 'hours')} hrs`
  }

  private formatDetail (d: any) {
    return moment(d).clone().format('h:mm a')
  }

  private formatHeader (d: any) {
    return moment(d).clone().format('dddd, MMM Do, YYYY')
  }

  private next () {
    Vue.set(
      this,
      'weekStart',
      this.weekStart.clone().add(7, 'day')
    )
    this.updateButtonsDate()
  }

  private prev () {
    Vue.set(
      this,
      'weekStart',
      this.weekStart.clone().subtract(7, 'day')
    )
    this.updateButtonsDate()
  }

  private getExamItems (dateString: string) {
    return this.examEvents.filter((exam: any) => moment(exam.start).clone().format('dddd, MMM Do, YYYY') === dateString)
  }

  private showInvigilator (data: any) {
    const { exam } = data
    const self = this
    const invigilator_name_list: any = []
    exam.booking.invigilators.forEach(function (invigilator: any) {
      const i = self.invigilator_multi_select.filter((i: any) => i.value == invigilator)
      if (i[0] && i[0].name) {
        invigilator_name_list.push(i[0].name)
      }
    })
    if (exam.booking.sbc_staff_invigilated) {
      return ['SBC Employee']
    }
    if (exam.booking.invigilators) {
      return invigilator_name_list
    }
    return false
  }

  private showShadowInvigilator (data: any) {
    const { exam } = data
    const shadow_invigilator = this.all_invigilator_options.filter((i: any) => i.id == exam.booking.shadow_invigilator_id)
    if (shadow_invigilator[0] && shadow_invigilator[0].name) {
      return shadow_invigilator[0].name
    } else { return false }
  }

  private showLocation (data: any) {
    const { exam } = data
    if (exam.offsite_location) {
      return false
    }
    if (exam.booking && exam.booking.room_id) {
      return exam.booking.room.room_name
    }
  }

  private showWriter (data: any) {
    const { exam } = data
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
  }

  private today () {
    Vue.set(
      this,
      'weekStart',
      moment().day(1)
    )
    this.updateButtonsDate()
  }

  private updateButtonsDate () {
    this.$nextTick(function () {
      const d = this.weekStart
      const text = `Week of ${d.clone().format('MMM Do, YYYY')}`
      this.setCalendarSetup({ title: text })
    })
  }

  public mounted () {
    this.initializeAgenda()
    this.$root.$on('agenda-next', () => { this.next() })
    this.$root.$on('agenda-prev', () => { this.prev() })
    this.$root.$on('agenda-today', () => { this.today() })
    this.weekStart = moment().day(1)
    this.updateButtonsDate()
    this.getInvigilators()
  }

  public destroyed () {
    this.setCalendarSetup(null)
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
  font-size: 0.9rem;
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
