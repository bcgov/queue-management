<template>
  <div class="px-3">
    <b-col md="6" class="my-1">
      <b-form-group horizontal label="Filter" class="mb-0">
        <b-input-group>
          <b-form-input v-model="filter" placeholder="Type to Search" />
          <b-input-group-append>
            <b-btn :disabled="!filter" @click="filter = ''">Clear</b-btn>
          </b-input-group-append>
        </b-input-group>
      </b-form-group>
    </b-col>
    <b-table :items="selectedExams"
             :fields=getFields
             class="m-0 p-0"
             head-variant="light"
             empty-text="There are no exams that match this filter criteria"
             small
             outlined
             @row-clicked="clickRow"
             hover
             show-empty
             :filter="filter">
      <template slot="exam_received" slot-scope="row">
        {{ row.item.exam_received === 0 ? 'No' : 'Yes' }}
      </template>
      <template slot="invigilator" slot-scope="row">
        {{ getInvigilator(row) }}
      </template>
      <template slot="expiry_date" slot-scope="row">
        {{ row.item.expiry_date.split('T')[0] }}
      </template>
    </b-table>
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

  export default {
    name: "ExamInventoryTable",
    props: ['mode'],
    data() {
      return {
        filter: null,
        events: null,
        fields: [
          {key: 'office.office_name', label: 'Office', sortable: true},
          {key: 'event_id', label: 'Event ID', sortable: false },
          {key: 'exam_name', label: 'Exam Name', sortable: true },
          {key: 'exam_method', label: 'Method', sortable: false },
          {key: 'expiry_date', label: 'Expiry Date', sortable: true },
          {key: 'exam_received', label: 'Received?', sortable: true },
          {key: 'examinee_name', label: 'Student Name', sortable: true },
          {key: 'notes', label: 'Notes', sortable: false },
          {key: 'invigilator', label: 'Invigilator', sortable: true },
          {key: 'booking.room.room_name', label: 'Location', sortable: true },
        ],
      }
    },
    methods: {
      ...mapActions(['getExams', 'getBookings']),
      ...mapMutations([
        'navigationVisible',
        'setSelectedExam',
        'toggleCalendarControls',
        'toggleExamInventoryModal',
        'toggleScheduling',
        'toggleSchedulingIndicator',
      ]),
      getInvigilator(row) {
        if (this.events) {
          let bookingObj = this.events.find(event=>event.booking_id==row.item.booking_id)
          if (bookingObj && bookingObj.invigilator) {
            return bookingObj.invigilator.invigilator_name
          }
          return ''
        }
        return ''
      },
      clickRow(e) {
        if (this.showExamInventoryModal) {
          this.$root.$emit('options', {name: 'selectable', value: true})
          this.navigationVisible(false)
          this.setSelectedExam(e)
          this.toggleCalendarControls(false)
          this.toggleExamInventoryModal(false)
          this.toggleScheduling(true)
          this.toggleSchedulingIndicator(true)
        }
      },
    },
    mounted() {
      this.getBookings().then(bookings => {
        this.events = bookings
      })
      this.getExams()
    },
    computed: {
      ...mapGetters(['role_code', 'exam_inventory', 'calendar_events']),
      ...mapState(['user', 'exams', 'showExamInventoryModal', 'bookings']),
      selectedExams() {
        if (this.showExamInventoryModal) {
          return this.exam_inventory
        }
        return this.exams
      },
      getFields() {
        if (this.role_code === "LIAISON") {
          return this.fields
        } else {
          let returnFields = this.fields
          let index = this.fields.findIndex(x => x.key === "office.office_name")
          returnFields.splice(index, 1)
          return returnFields
        }
      }
    }
  }
</script>
