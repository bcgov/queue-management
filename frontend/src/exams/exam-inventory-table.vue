<template>
  <div style="margin-left: 20px">
    <b-form inline class="pb-2 pl-3">
      <font-awesome-icon icon="filter"
                         class="mr-1"
                         style="font-size: 1.0rem"/>
      <b-form-select :options="filters"
                     @input.native="changeFilter"
                     :value="filter"/>
      <font-awesome-icon icon="binoculars"
                         class="ml-3 mr-1"
                         style="font-size: 1.0rem"/>
      <b-form-input placeholder="type to search"/>
    </b-form>
    <b-table :items="examInventory"
             :fields="fields"
             class="m-0 p-0"
             head-variant="light"
             small
             outlined
             hover>
      <template slot="roomloc" slot-scope="row">
        <div v-if="row.item.location">
          {{ row.item.location }}
        </div>
        <div v-if="row.item.room">
          {{ row.item.room }}
        </div>
      </template>
    </b-table>

  </div>
</template>

<script>
  import { mapGetters, mapState } from 'vuex'

  export default {
    name: "ExamInventoryTable",
    props: ['mode'],
    data() {
      return {
        filter: null,
        filters: [
          {text: 'Select a Filter', value: null},
        ],
        fieldsModal: [
          {key: 'event_id', label: 'Event ID', sortable: false, thStyle: {width: '9%'} },
          {key: 'exam_name', label: 'Exam Name', sortable: true, thStyle: {width: '17%'} },
          {key: 'exam_method', label: 'Method', sortable: false, thStyle: {width: '8%'} },
          {key: 'expiry_date', label: 'Expirey Date', sortable: true, thStyle: {width: '9%'} },
          {key: 'exam_received', label: 'Received', sortable: true, thStyle: {width: '10%'} },
          {key: 'examinee_name', label: 'Student Name', sortable: true, thStyle: {width: '18%'}},
          {key: 'notes', label: 'Notes', sortable: true, thStyle: {width: '18%'}},
          {key: 'number_of_students', label: 'Students', sortable: false, thStyle: {width: '11%'}}
        ],
        fieldsInventory: [
          {key: 'event_id', label: 'Event ID', sortable: false, thStyle: {width: '9%'} },
          {key: 'exam_name', label: 'Exam Name', sortable: true, thStyle: {width: '17%'} },
          {key: 'exam_method', label: 'Method', sortable: false, thStyle: {width: '8%'} },
          {key: 'expiry_date', label: 'Expirey Date', sortable: true, thStyle: {width: '9%'} },
          {key: 'exam_received', label: 'Received', sortable: true, thStyle: {width: '10%'} },
          {key: 'examinee_name', label: 'Student Name', sortable: true, thStyle: {width: '18%'}},
          {key: 'notes', label: 'Notes', sortable: true, thStyle: {width: '18%'}},
          {key: 'number_of_students', label: 'Students', sortable: false, thStyle: {width: '11%'}}
        ],
      }
    },
    computed: {
      ...mapGetters(['role_code']),
      ...mapState(['examInventory']),
      fields() {
        if (this.mode === 'inventory') {
          if (this.role_code === 'GA' || this.role_code === 'CSR' || this.role_code === 'SUPPORT') {
            return this.fieldsInventory
          }
        } else if (this.mode === 'modal') {
          return this.fieldsModal
        }
      }
    },

  }
</script>

<style scoped>

</style>
