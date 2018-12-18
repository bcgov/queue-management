<template>
  <div style="margin-left: 20px">
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
    <b-table :items="exams"
             :fields=getFields
             class="m-0 p-0"
             head-variant="light"
             empty-text="There are no exams that match this filter criteria"
             small
             outlined
             hover
             show-empty
             :filter="filter">
      <template slot="exam_received" slot-scope="row">
        {{ row.item.exam_received === 0 ? 'No' : 'Yes' }}
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
        fields: [
          {key: 'office.office_name', label: 'Office', sortable: true},
          {key: 'event_id', label: 'Event ID', sortable: false },
          {key: 'exam_name', label: 'Exam Name', sortable: true },
          {key: 'exam_method', label: 'Method', sortable: false },
          {key: 'expiry_date', label: 'Expiry Date', sortable: true },
          {key: 'exam_received', label: 'Received?', sortable: true },
          {key: 'examinee_name', label: 'Student Name', sortable: true },
          {key: 'notes', label: 'Notes', sortable: false },
          {key: 'invigilator.invigilator_name', label: 'Invigilator', sortable: true },
          {key: 'booking.room.room_name', label: 'Location', sortable: true },
        ],
      }
    },
    methods: {
      ...mapActions(['getExams']),
    },
    mounted() {
      this.getExams()
    },
    computed: {
      ...mapGetters(['role_code']),
      ...mapState(['exams', 'user']),
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
