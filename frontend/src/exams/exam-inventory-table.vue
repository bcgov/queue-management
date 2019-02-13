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
                 :pressed="expiryFilter==='all'"
                 @click="handleFilter({type:'expiryFilter', value:'all'})"><span class="mx-2">All</span></b-btn>
          <b-btn size="sm"
                 :pressed="expiryFilter==='expired'"
                 @click="handleFilter({type:'expiryFilter', value:'expired'})">Expired</b-btn>
          <b-btn size="sm"
                 :pressed="expiryFilter==='current'"
                 @click="handleFilter({type:'expiryFilter', value:'current'})">Current</b-btn>
        </b-btn-group>
        <b-btn-group horizontal class="ml-2 pt-2">
          <b-btn size="sm"
                 :pressed="scheduledFilter==='both'"
                 @click="handleFilter({type:'scheduledFilter', value:'both'})"><span class="mx-2">Both</span></b-btn>
          <b-btn size="sm"
                 :pressed="scheduledFilter==='unscheduled'"
                 @click="handleFilter({type:'scheduledFilter', value:'unscheduled'})">Un-Scheduled</b-btn>
          <b-btn size="sm"
                 :pressed="scheduledFilter==='scheduled'"
                 @click="handleFilter({type:'scheduledFilter', value:'scheduled'})">Scheduled</b-btn>
        </b-btn-group>
        <b-btn-group horizontal class="ml-2 pt-2">
          <b-btn size="sm"
                 :pressed="groupFilter==='both'"
                 @click="handleFilter({type:'groupFilter', value:'both'})"><span class="mx-2">Both</span></b-btn>
          <b-btn size="sm"
                 :pressed="groupFilter==='individual'"
                 @click="handleFilter({type:'groupFilter', value:'individual'})">Individual</b-btn>
          <b-btn size="sm"
                 :pressed="groupFilter==='group'"
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
               outlined
               @row-clicked="clickRow"
               hover
               show-empty
               :filter="filter">
      <template slot="examinee_name" slot-scope="row">
        {{ row.item.offsite_location ? 'Group Exam' : row.item.examinee_name }}
      </template>
      <template slot="exam_received" slot-scope="row">
        {{ row.item.exam_received === 0 ? 'No' : 'Yes' }}
      </template>
      <template slot="expiry_date" slot-scope="row">
        {{ row.item.examinee_name === 'group exam' ? '–' : row.item.expiry_date.split('T')[0] }}
      </template>
      <template slot="scheduled" slot-scope="row">
        <b-button v-if="row.item.booking_id && row.item.booking.invigilator_id"
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
          <div style="flex-grow: 1">
            <b>Invigilator: </b>
               {{ row.item.booking.invigilator_id ? row.item.booking.invigilator.invigilator_name : '–' }}
          </div>
          <div v-if="row.item.offsite_location"
               style="flex-grow: 4">Location: {{ row.item.offsite_location }}</div>
          <div v-else
               style="flex-grow: 6">Room: {{ row.item.booking.room_id ? row.item.booking.room.room_name : '–' }}</div>
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
                           @click.stop="editExam(row.item)">Edit Exam</b-dropdown-item>
          <b-dropdown-item size="sm"
                           @click.stop="returnExamInfo(row.item)">Return Exam</b-dropdown-item>
          <template v-if="row.item.booking && row.item.booking.invigilator_id">
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
    <EditExamModal :exam="item" :resetExam="resetEditedExam" />
    <ReturnExamModal v-if="showReturnExamModalVisible" />
    <EditGroupExamBookingModal :exam="item" :resetExam="resetEditedExam" />
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
        item: null,
        tableStyle: null,
        expiryFilter: 'current',
        scheduledFilter: 'unscheduled',
        groupFilter: 'both',
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
        'navigationVisible',
        'setSelectedExam',
        'toggleCalendarControls',
        'toggleExamInventoryModal',
        'toggleScheduling',
        'toggleSchedulingIndicator',
        'toggleEditBookingModal',
        'toggleEditExamModal',
        'toggleEditGroupBookingModal',
        'setEditedBooking',
        'setEditedBookingOriginal',
        'setEditExamInfo',
        'toggleReturnExamModalVisible',
        'setReturnExamInfo',
      ]),
      handleExpiryFilter(e) {
        this.expiryFilter = e.target.value
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
          switch (this.expiryFilter) {
            case 'all':
              filtered = exams
              break
            case 'expired':
              filtered = exams.filter(ex => moment(ex.expiry_date).isBefore(moment(), 'day'))
              break
            case 'current':
              filtered = exams.filter(ex => moment(ex.expiry_date).isSameOrAfter(moment(), 'day'))
              break
            default:
              filtered = exams
              break
          }
          let moreFiltered = []
          switch (this.scheduledFilter) {
            case 'both':
              moreFiltered = filtered
              break
            case 'unscheduled':
              moreFiltered = filtered.filter(ex => !ex.booking || !ex.booking.invigilator_id)
              break
            case 'scheduled':
              moreFiltered = filtered.filter(ex => ex.booking && ex.booking.invigilator_id)
              break
            default:
              moreFiltered = filtered
              break
          }
          let evenMoreFiltered = []
          switch (this.groupFilter) {
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
      handleFilter(e) {
        this[e.type] = e.value
        localStorage.setItem(e.type, e.value)
      },
      getWidth() {
        if (!this.showExamInventoryModal) {
          this.tableStyle = { width: `${ window.innerWidth - 40 }px` }
        }
        if (this.showExamInventoryModal) {
          this.tableStyle = { width: 98 + '%' }
        }
      },
      handleBookedFilter(e) {
        this.bookedFilter = e.target.value
      },
      resetButtons() {
        this.buttons.all = 'btn-secondary'
        this.buttons.current = 'btn-secondary'
        this.buttons.expired = 'btn-secondary'
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
      clickRow(e) {
        if (this.showExamInventoryModal) {
          this.$root.$emit('toggleOffsite', false)
          this.$root.$emit('options', {name: 'selectable', value: true})
          this.navigationVisible(false)
          this.setSelectedExam(e)
          this.toggleCalendarControls(false)
          this.toggleExamInventoryModal(false)
          this.toggleScheduling(true)
          this.toggleSchedulingIndicator(true)
        }
      },
      editExam(item) {
        this.item = item
        this.setEditExamInfo(item)
        this.toggleEditExamModal(true)
      },
      returnExamInfo(item) {
        this.toggleReturnExamModalVisible(true)
        this.setReturnExamInfo(item)
      },
      editGroupExam(item) {
        this.item = item
        this.toggleEditGroupBookingModal(true)
      },
      updateBookingRoute(item) {
        let calendarEvent = this.calendarEvents.find(event => event.id == item.booking_id)
        this.setEditedBookingOriginal(calendarEvent)
        this.setEditedBooking(calendarEvent)
        this.toggleEditBookingModal(true)
        this.$router.push('/booking/' + moment(item.booking.start_time).format('YYYY-MM-DD'))
      },
      resetEditedExam() {
        this.item = {}
      },
      formatDate(d) {
        return new moment(d).format('MMM DD, YYYY')
      },
      formatTime(d) {
        return new moment(d).format('h:mm a')
      },
      addBookingRoute(item) {
        let bookingRoute = '/booking/?schedule=true'
        this.$router.push(bookingRoute)
        this.navigationVisible(false)
        this.setSelectedExam(item)
        this.toggleCalendarControls(false)
        this.toggleExamInventoryModal(false)
        this.toggleScheduling(true)
        this.toggleSchedulingIndicator(true)
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
