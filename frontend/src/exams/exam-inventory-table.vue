<template>
  <div>
    <b-form inline class="ml-3">
      <b-input-group>
        <b-input-group-prepend><label class="mx-1 pt-1 my-auto label-text">Search</label></b-input-group-prepend>
        <b-input size="sm" class="mb-1 mt-3" v-model="filter"></b-input>
      </b-input-group>
      <b-input-group class="ml-3" v-if="!showExamInventoryModal">
        <b-input-group-prepend>
          <label class="mx-1 pt-1 my-auto label-text">Filters</label>
        </b-input-group-prepend>
        <b-btn-group horizontal class="pt-2">
          <b-btn size="sm"
                 :pressed="inventoryFilters.expiryFilter==='all'"
                 @click="handleFilter({type:'expiryFilter', value:'all'})"><span class="mx-2">All</span></b-btn>
          <b-btn size="sm"
                 :pressed="inventoryFilters.expiryFilter==='expired'"
                 @click="handleFilter({type:'expiryFilter', value:'expired'})">Expired</b-btn>
          <b-btn size="sm"
                 :pressed="inventoryFilters.expiryFilter==='current'"
                 @click="handleFilter({type:'expiryFilter', value:'current'})">Current</b-btn>
        </b-btn-group>
        <b-btn-group horizontal class="ml-2 pt-2">
          <b-btn size="sm"
                 :pressed="inventoryFilters.scheduledFilter==='both'"
                 @click="handleFilter({type:'scheduledFilter', value:'both'})"><span class="mx-2">Both</span></b-btn>
          <b-btn size="sm"
                 :pressed="inventoryFilters.scheduledFilter==='unscheduled'"
                 @click="handleFilter({type:'scheduledFilter', value:'unscheduled'})">Un-Scheduled</b-btn>
          <b-btn size="sm"
                 :pressed="inventoryFilters.scheduledFilter==='scheduled'"
                 @click="handleFilter({type:'scheduledFilter', value:'scheduled'})">Scheduled</b-btn>
        </b-btn-group>
        <b-btn-group horizontal class="ml-2 pt-2">
          <b-btn size="sm"
                 :pressed="inventoryFilters.groupFilter==='both'"
                 @click="handleFilter({type:'groupFilter', value:'both'})"><span class="mx-2">Both</span></b-btn>
          <b-btn size="sm"
                 :pressed="inventoryFilters.groupFilter==='individual'"
                 @click="handleFilter({type:'groupFilter', value:'individual'})">Individual</b-btn>
          <b-btn size="sm"
                 :pressed="inventoryFilters.groupFilter==='group'"
                 @click="handleFilter({type:'groupFilter', value:'group'})">Group</b-btn>
        </b-btn-group>
      </b-input-group>`
    </b-form>
    <div :style="tableStyle" class="my-0 mx-3">
      <b-table :items="filteredExams()"
               :fields="getFields"
               head-variant="light"
               style="border: 1px solid dimgrey"
               empty-text="There are no exams that match this filter criteria"
               small
               tbody-tr-class="q-custom-tr"
               outlined
               @row-clicked="clickRow"
               hover
               show-empty
               :filter="filter">
      <template slot="examinee_name" slot-scope="row">
        {{ row.item.offsite_location ? 'Group Exam' : row.item.examinee_name }}
      </template>
      <template slot="exam_received" slot-scope="row">
        {{ row.item.exam_received_date ? 'Yes' : 'No' }}
      </template>
      <template slot="expiry_date" slot-scope="row">
        {{ row.item.examinee_name === 'group exam' ? '–' : formatDate(row.item.expiry_date) }}
      </template>
      <template slot="scheduled" slot-scope="row">
        <b-button v-if="row.item.booking && (row.item.booking.invigilator_id || row.item.booking.sbc_staff_invigilated)"
                  class="btn-link"
                  @click.stop="row.toggleDetails">
          {{ row.detailsShowing ? 'Hide' : 'Show'}}
        </b-button>
        <font-awesome-icon v-else
                           icon="exclamation-triangle"
                           class="m-0 p-0"
                           style="font-size:1rem;color:#ffc32b"/>
      </template>
      <template slot="row-details" slot-scope="row">
        <div class="details-slot-div">
          <div style="flex-grow: 1" class="ml-3"><b>Date:</b> {{ formatDate(row.item.booking.start_time) }}</div>
          <div style="flex-grow: 1"><b>Time:</b> {{ formatTime(row.item.booking.start_time) }}</div>
          <div style="flex-grow: 2">
            <b>Invigilator: </b>
            <span v-if="row.item.booking.invigilator_id">{{ row.item.booking.invigilator.invigilator_name }}</span>
            <span v-if="row.item.booking.sbc_staff_invigilated">ServiceBC Staff</span>
          </div>
          <div v-if="row.item.offsite_location"
               style="flex-grow: 8">Location: {{ row.item.offsite_location }}</div>
          <div v-else
               style="flex-grow: 8">Room: {{ row.item.booking.room_id ? row.item.booking.room.room_name : '–' }}</div>
          <div style="flex-grow: 8" />
        </div>
      </template>
      <template slot="actions" slot-scope="row">
        <b-dropdown variant="link"
                    no-caret
                    size="sm"
                    class="pl-0 ml-0 mr-3"
                    id="nav-dropdown"
                    right>
          <template slot="button-content">
            <font-awesome-icon icon="caret-down"
                               style="padding: -2px; margin: -2px; font-size: 1rem; color: dimgray"/>
          </template>
          <b-dropdown-item size="sm"
                           @click="editExam(row.item)">Edit Exam</b-dropdown-item>
          <b-dropdown-item size="sm"
                           @click="returnExamInfo(row.item)">Return Exam</b-dropdown-item>
          <template v-if="row.item.booking&&(row.item.booking.invigilator_id||row.item.booking.sbc_staff_invigilated)">
            <b-dropdown-item v-if="row.item.offsite_location"
                             size="sm"
                             @click="editGroupExam(row.item)">Reschedule</b-dropdown-item>
            <b-dropdown-item v-if="!row.item.offsite_location"
                             size="sm"
                             @click="updateBookingRoute(row.item)">Reschedule</b-dropdown-item>
          </template>
          <b-dropdown-item v-if="!row.item.booking"
                           size="sm"
                           @click="addBookingRoute(row.item)">Schedule Exam</b-dropdown-item>
          <b-dropdown-item v-if="row.item.offsite_location && !(row.item.booking && row.item.booking.invigilator_id)"
                           size="sm"
                           @click="editGroupExam(row.item)">Add Invigilator</b-dropdown-item>
        </b-dropdown>
      </template>
    </b-table>
    </div>
    <EditExamModal :examRow="examRow" :resetExam="resetEditedExam" />
    <ReturnExamModal v-if="showReturnExamModalVisible" />
    <EditGroupExamBookingModal :examRow="examRow" :resetExam="resetEditedExam" />
  </div>
</template>

<script>
  import EditExamModal from './edit-exam-form-modal'
  import EditGroupExamBookingModal from './edit-group-exam-modal'
  import FailureExamAlert from './failure-exam-alert'
  import ReturnExamModal from './return-exam-form-modal'
  import SuccessExamAlert from './success-exam-alert'
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import moment from 'moment'
  import Vue from 'vue'

  export default {
    name: "ExamInventoryTable",
    components: { EditGroupExamBookingModal, EditExamModal, ReturnExamModal, SuccessExamAlert, FailureExamAlert },
    props: ['mode'],
    mounted() {
      this.getInvigilators()
      this.getExams().then( () => { this.getBookings() })
      this.getWidth()
      this.$nextTick(function() {
        window.addEventListener('resize', () => { this.getWidth() })
      })
    },
    data() {
      return {
        examRow: {},
        tableStyle: null,
        filter: null,
        events: null,
        bookingRouteString: '',
      }
    },
    computed: {
      ...mapGetters([ 'calendar_events', 'exam_inventory', 'role_code' ]),
      ...mapState([
        'bookings',
        'calendarSetup',
        'calendarEvents',
        'exams',
        'inventoryFilters',
        'showEditExamModal',
        'showExamInventoryModal',
        'showReturnExamModalVisible',
        'user',
      ]),
      fields() {
        if (!this.showExamInventoryModal) {
          return [
            { key: 'office.office_name', label: 'Office', sortable: true, thStyle: 'width: 8%' },
            { key: 'event_id', label: 'Event ID', sortable: true, thStyle: 'width: 6%' },
            { key: 'exam_name', label: 'Exam Name', sortable: true, thStyle: 'width: 11%' },
            { key: 'exam_method', label: 'Method', sortable: true, thStyle: 'width: 5%' },
            { key: 'expiry_date', label: 'Expiry Date', sortable: true, thStyle: 'width: 8%' },
            { key: 'exam_received', label: 'Received?', sortable: true, thStyle: 'width: 5%' },
            { key: 'examinee_name', label: 'Student Name', sortable: true, thStyle: 'width: 12%' },
            { key: 'notes', label: 'Notes', sortable: true, thStyle: 'width: 21%' },
            { key: 'scheduled', label: 'Scheduled?', thStyle: 'width: 5%', tdClass: 'text-center'},
            { key: 'actions', label: 'Actions', sortable: true, thStyle: 'width: 5%' },
          ]
        }
        if (this.showExamInventoryModal) {
          return [
            { key: 'event_id', label: 'Event ID', sortable: true, thStyle: 'width: 6%' },
            { key: 'exam_name', label: 'Exam Name', sortable: true, thStyle: 'width: 15%' },
            { key: 'exam_method', label: 'Method', sortable: true, thStyle: 'width: 5%' },
            { key: 'expiry_date', label: 'Expiry Date', sortable: true, thStyle: 'width: 8%' },
            { key: 'exam_received', label: 'Received?', sortable: true, thStyle: 'width: 5%' },
            { key: 'examinee_name', label: 'Student Name', sortable: true, thStyle: 'width: 20%' },
            { key: 'notes', label: 'Notes', sortable: true, },
          ]
        }
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

    },
    methods: {
      ...mapActions(['getExams', 'getBookings', 'getInvigilators']),
      ...mapMutations([
        'setEditedBooking',
        'setEditedBookingOriginal',
        'setEditExamInfo',
        'setInventoryFilters',
        'setReturnExamInfo',
        'setSelectedExam',
        'toggleEditBookingModal',
        'toggleEditExamModal',
        'toggleEditGroupBookingModal',
        'toggleExamInventoryModal',
        'toggleReturnExamModalVisible',
        'toggleScheduling',
      ]),
      addBookingRoute(item) {
        this.toggleScheduling(true)
        item.referringAction = 'scheduling'
        this.setSelectedExam(item)
        this.$router.push('/booking')
        this.toggleExamInventoryModal(false)
      },
      clickRow(item) {
        if (this.showExamInventoryModal) {
          this.toggleScheduling(true)
          this.setSelectedExam(item)
          this.$router.push('/booking')
          this.toggleExamInventoryModal(false)
        }
      },
      editExam(item) {
        Object.keys(item).forEach( i => {
          Vue.set(
            this.examRow,
            i,
            item[i]
          )
        })
        this.toggleEditExamModal(true)
      },
      editGroupExam(item) {
        this.examRow = item
        this.toggleEditGroupBookingModal(true)
      },
      filteredExams() {
        let exams = this.exam_inventory || []
        let filtered = []
        if (exams.length > 0) {
          if (this.showExamInventoryModal) {
            filtered = exams.filter(ex => moment(ex.expiry_date).isSameOrAfter(moment(), 'day'))
            let moreFiltered = filtered.filter(ex => !ex.booking)
            let evenMoreFiltered = moreFiltered.filter(ex => !ex.offsite_location)
            return evenMoreFiltered
          }
          switch (this.inventoryFilters.expiryFilter) {
            case 'all':
              filtered = exams
              break
            case 'expired':
              filtered = exams.filter(ex => moment(ex.expiry_date).isBefore(moment(), 'day'))
              break
            case 'current':
              let step1 = exams.filter(ex => moment(ex.expiry_date).isSameOrAfter(moment(), 'day'))
              let step2 = exams.filter(ex => !ex.expiry_date)
              filtered = step1.concat(step2)
              break
            default:
              filtered = exams
              break
          }
          let moreFiltered = []
          switch (this.inventoryFilters.scheduledFilter) {
            case 'both':
              moreFiltered = filtered
              break
            case 'unscheduled':
              moreFiltered=filtered.filter(x=>!x.booking||(!x.booking.invigilator_id&&!x.booking.sbc_staff_invigilated))
              break
            case 'scheduled':
              moreFiltered = filtered.filter(x=>x.booking&&(x.booking.invigilator_id||x.booking.sbc_staff_invigilated))
              break
            default:
              moreFiltered = filtered
              break
          }
          let evenMoreFiltered = []
          switch (this.inventoryFilters.groupFilter) {
            case 'both':
              evenMoreFiltered = moreFiltered
              break
            case 'individual':
              evenMoreFiltered = moreFiltered.filter(ex => !ex.offsite_location)
              break
            case 'group':
              evenMoreFiltered = moreFiltered.filter(ex => ex.offsite_location)
              break
            default:
              evenMoreFiltered = moreFiltered
              break
          }
          return evenMoreFiltered
        }
        return []
      },
      formatDate(d) {
        return new moment(d).format('ddd MMM DD, YYYY')
      },
      formatTime(d) {
        return new moment(d).format('h:mm a')
      },
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
      getWidth() {
        if (!this.showExamInventoryModal) {
          this.tableStyle = { width: `${ window.innerWidth - 40 }px` }
        }
        if (this.showExamInventoryModal) {
          this.tableStyle = { width: 98 + '%' }
        }
      },
      handleFilter(e) {
        this.setInventoryFilters(e)
      },
      resetButtons() {
        this.buttons.all = 'btn-secondary'
        this.buttons.current = 'btn-secondary'
        this.buttons.expired = 'btn-secondary'
      },
      resetEditedExam() {
        this.examRow = {}
      },
      returnExamInfo(item) {
        this.toggleReturnExamModalVisible(true)
        this.setReturnExamInfo(item)
      },
      updateBookingRoute(item) {
        item.gotoDate = new moment(item.booking.start_time)
        item.referringAction = 'rescheduling'
        this.setSelectedExam(item)
        let booking = this.calendarEvents.find(event => event.id == item.booking_id)
        booking.start = new moment(booking.start)
        booking.end = new moment(booking.end)
        this.setEditedBooking(booking)
        this.setEditedBookingOriginal(booking)
        this.toggleEditBookingModal(true)
        this.$router.push('/booking')
      },
    },
  }
</script>

<style scoped>
  .open-cal-link {
    text-decoration: #007bff underline !important;
    text-underline-position: under !important;
    font-size: .85rem !important;
    color: #007bff !important;
    font-weight: 300 !important;
  }
  .view-details-link {
    text-decoration: #007bff underline !important;
    text-underline-position: under;
    font-size: .85rem;
    color: #007bff !important;
    font-weight: 300;
  }
  .view-details-link:hover {
    font-weight: 600;
  }
  .open-cal-link:hover {
    font-weight: 600;
  }
  .schedule-link {
    text-decoration: #28a745 underline !important;
    text-underline-position: under;
    font-size: .85rem;
    color: #28a745 !important;
    font-weight: 300;
  }
  .schedule-link:hover {
    font-weight: 600;
  }
  .btn {
    border: none !important;
  }
  .label-text {
    font-size: .9rem;
  }
  .btn {
    border: none !important;
    box-shadow: none !important;
    transition: none !important;
  }
  .btn:active, .btn.active {
    background-color: lightgrey !important;
    color: dimgrey !important;
  }
  .exam-table-holder {
    border: 1px solid dimgrey;
  }
  .details-slot-div {
    display: flex;
    justify-content: flex-start;
    width: 100%;
    padding-top: 6px;
    padding-bottom: 6px;
  }
</style>
