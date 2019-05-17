<template>
  <fragment>
    <EditExamModal :actionedExam="actionedExam" :resetExam="resetActionedExam" />
    <ReturnExamModal :actionedExam="actionedExam" :resetExam="resetActionedExam" />
    <EditGroupExamBookingModal :actionedExam="actionedExam" :resetExam="resetActionedExam" />
    <DeleteExamModal v-if="showDeleteExamModal" :actionedExam="actionedExam" :resetExam="resetActionedExam" />
    <b-modal v-model="officeFilterModal"
             size="sm"
             centered
             hide-backdrop
             @hide="resetInvalidOfficeOnHide()"
             hide-header
             hide-footer>
      <h5>View Another Office</h5>
      <p>To search, start typing or enter an office #</p>
      <b-form autocomplete="off">
        <b-form-row>
          <OfficeDrop columnW="8" :office_number="officeNumber" :setOffice="setOfficeFilter"/>
        </b-form-row>
      </b-form>
      <div style="display:flex; justify-content: space-between">
        <b-button class="mr-2 btn-secondary"
                  @click="setHomeOffice">This Office</b-button>
        <b-button class="ml-2 btn-primary"
                  @click="officeFilterModal=false">Ok</b-button>
      </div>
    </b-modal>
    <div class="q-w100-flex-fs">
      <b-form inline class="ml-3">
        <b-input-group>
          <b-input-group-prepend><label class="mx-1 pt-1 my-auto label-text">Search</label></b-input-group-prepend>
          <b-input size="sm" class="mb-1 mt-3" v-model="searchTerm"></b-input>
        </b-input-group>
        <b-input-group class="ml-3" v-if="!showExamInventoryModal">
          <b-input-group-prepend>
            <label class="mx-1 pt-1 my-auto label-text">Filters</label>
          </b-input-group-prepend>
          <b-btn-group v-if="is_liaison_designate" class="pt-2">
            <b-btn @click="officeFilterModal=true"
                   :variant="officeFilter === userOffice || officeFilter === 'default' ? 'primary' : 'warning'"
                   class="btn-sm">Office # {{ officeNumber }} - {{ officeName }}</b-btn>
          </b-btn-group>
          <b-button-group horizontal
                          class="ml-2 pt-2"
                          label="Expired Exam Filters">
            <b-button size="sm"
                      :pressed="inventoryFilters.expiryFilter==='all'"
                      @click="setInventoryFilters({type:'expiryFilter', value:'all'})"
                      variant="primary">
              <span class="mx-2">All</span>
            </b-button>
            <b-button size="sm"
                      :pressed="inventoryFilters.expiryFilter==='expired'"
                      @click="setInventoryFilters({type:'expiryFilter', value:'expired'})"
                      variant="primary">Expired</b-button>
            <b-button size="sm"
                      :pressed="inventoryFilters.expiryFilter==='current'"
                      @click="setInventoryFilters({type:'expiryFilter', value:'current'})"
                      variant="primary">Current</b-button>
          </b-button-group>
          <b-btn-group horizontal class="ml-2 pt-2">
            <b-btn size="sm"
                   :pressed="inventoryFilters.scheduledFilter==='both'"
                   @click="setInventoryFilters({type:'scheduledFilter', value:'both'})"
                   variant="primary">
              <span class="mx-2">Both</span>
            </b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.scheduledFilter==='unscheduled'"
                   @click="setInventoryFilters({type:'scheduledFilter', value:'unscheduled'})"
                   variant="primary">Not Ready</b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.scheduledFilter==='scheduled'"
                   @click="setInventoryFilters({type:'scheduledFilter', value:'scheduled'})"
                   variant="primary">Ready</b-btn>
          </b-btn-group>
          <b-btn-group horizontal class="ml-2 pt-2">
            <b-btn size="sm"
                   :pressed="inventoryFilters.groupFilter==='both'"
                   @click="setInventoryFilters({type:'groupFilter', value:'both'})"
                   variant="primary"><span class="mx-2">Both</span></b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.groupFilter==='individual'"
                   @click="setInventoryFilters({type:'groupFilter', value:'individual'})"
                   variant="primary">Individual</b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.groupFilter==='group'"
                   @click="setInventoryFilters({type:'groupFilter', value:'group'})"
                   variant="primary">Group</b-btn>
          </b-btn-group>
          <b-btn-group horizontal class="ml-2 pt-2">
            <b-btn size="sm"
                   :pressed="inventoryFilters.returnedFilter==='both'"
                   @click="setFilter({type:'returnedFilter', value:'both'})"
                   variant="primary"><span class="mx-2">Both</span></b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.returnedFilter==='returned'"
                   @click="setFilter({type:'returnedFilter', value:'returned'})"
                   variant="primary">Returned</b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.returnedFilter==='unreturned'"
                   @click="setFilter({type:'returnedFilter', value:'unreturned'})"
                   variant="primary">Not Returned</b-btn>
          </b-btn-group>
        </b-input-group>
      </b-form>
    </div>
    <div :style="tableStyle" class="my-0 mx-3">
      <b-table :items="filteredExams()"
               :fields="fields"
               sort-by="scheduled"
               :sort-desc="true"
               head-variant="light"
               :style="availableH"
               empty-text="There are no exams that match this filter criteria"
               small
               :sort-compare="sortCompare"
               outlined
               @row-clicked="clickModalRow"
               hover
               show-empty
               responsive
               :current-page="page"
               :per-page="10"
               :filter="searchTerm"
               id="exam_inventory_table">

        <template slot="exam_received" slot-scope="row">
          {{ row.item.exam_received_date ? 'Yes' : 'No' }}
        </template>

        <template slot="exam_type_name" slot-scope="row">
          {{ row.item.exam_type.exam_type_name }}
        </template>

        <template slot="expiry_date" slot-scope="row">
          <span v-if="row.item.exam_type.exam_type_name === 'Monthly Session Exam'">–</span>
          <span v-else-if="row.item.exam_type.group_exam_ind">–</span>
          <span v-else>{{ formatDate(row.item.expiry_date) }}</span>
        </template>

        <template slot="scheduled" slot-scope="row">
          <font-awesome-icon v-if="!row.detailsShowing"
                             :icon="statusIcon(row.item).icon"
                             @click.stop="row.toggleDetails()"
                             class="m-0 p-0 icon-cursor-hover"
                             :style="statusIcon(row.item).style"/>
          <b-button v-if="row.detailsShowing"
                    variant="link"
                    style="padding: 0px;"
                    @click.stop="row.toggleDetails()">Hide</b-button>
        </template>

        <template slot="row-details" slot-scope="row">
          <template v-if="stillRequires(row.item).length === 0">
            <div class="details-slot-div">
              <div style="flex-grow: 1" class="ml-3"><b>Date:</b> {{ formatDate(row.item.booking.start_time) }}</div>
              <div style="flex-grow: 1"><b>Time:</b> {{ formatTime(row.item.booking) }}</div>
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

          <template v-if="stillRequires(row.item).length > 0">
            <div class="details-slot-div">
              <div class="ml-3" style="font-size: 1rem; flex-grow: 1;">Still Requires:</div>
              <template v-for="(req, i) in stillRequires(row.item)">
                <div :key="i+'it'" class="ml-3 mt-1" style="flex-grow: 1;">{{ req }}</div>
              </template>
              <div style="flex-grow: 6" />
              <div style="flex-grow: 1; font-size: 1rem;">Details</div>
              <template v-for="(val, key) in readyDetailsMap(row.item)">
                <div class="ml-3 mt-1" style="flex-grow: 1;"><b>{{ key }}: </b> {{ val }} </div>
              </template>
              <div style="flex-grow: 12" />
            </div>
          </template>
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
            <template v-if="!row.item.exam_returned_date">
              <template v-if="officeFilter == userOffice || officeFilter == 'default'">

                <template v-if="row.item.exam_type.exam_type_name === 'Monthly Session Exam' ">
                  <template v-if="row.item.offsite_location">
                    <b-dropdown-item size="sm"
                                     v-if="row.item.offsite_location"
                                     @click="editGroupBooking(row.item)">
                        {{ checkInvigilator(row.item) ? 'Update Booking' : 'Add Invigilator' }}
                    </b-dropdown-item>
                  </template>

                  <template v-if="!row.item.offsite_location">
                    <b-dropdown-item size="sm"
                                       v-if="row.item.booking && Object.keys(row.item.booking).length > 0"
                                     @click="updateCalendarBooking(row.item)">
                        {{ checkInvigilator(row.item) ? 'Update Booking' : 'Add Invigilator' }}</b-dropdown-item>
                    <b-dropdown-item size="sm"
                                     v-if="!row.item.booking || Object.keys(row.item.booking).length === 0"
                                     @click="addCalendarBooking(row.item)">Schedule Exam</b-dropdown-item>
                  </template>
                </template>

                <template v-else-if="row.item.exam_type.group_exam_ind">
                  <b-dropdown-item size="sm"
                                   v-if="row.item.offsite_location"
                                   @click="editGroupBooking(row.item)">
                    {{ checkInvigilator(row.item) ? 'Update Booking' : 'Add Invigilator' }}
                  </b-dropdown-item>
                </template>

                <template v-else>
                  <template v-if="row.item.offsite_location && row.item.offsite_location === '_offsite'">
                    <b-dropdown-item size="sm"
                                     v-if="!row.item.booking || Object.keys(row.item.booking).length === 0"
                                     @click="editGroupBooking(row.item)">Schedule Exam</b-dropdown-item>
                  </template>
                  <template v-if="row.item.offsite_location && row.item.offsite_location !== '_offsite'">
                    <b-dropdown-item size="sm"
                                     v-if="row.item.offsite_location"
                                     @click="editGroupBooking(row.item)">
                      {{ checkInvigilator(row.item) ? 'Update Booking' : 'Add Invigilator' }}
                    </b-dropdown-item>
                  </template>
                  <template template v-if="!row.item.offsite_location">
                    <b-dropdown-item size="sm"
                                     v-if="row.item.booking && Object.keys(row.item.booking).length > 0"
                                     @click="updateCalendarBooking(row.item)">
                      {{ checkInvigilator(row.item) ? 'Update Booking' : 'Add Invigilator' }}</b-dropdown-item>
                    <b-dropdown-item size="sm"
                                     v-if="!row.item.booking || Object.keys(row.item.booking).length === 0"
                                     @click="addCalendarBooking(row.item)">Schedule Exam</b-dropdown-item>
                  </template>
                </template>

                  <b-dropdown-item size="sm"
                                   @click="editExamDetails(row.item)">Edit Exam Details</b-dropdown-item>
                  <b-dropdown-item size="sm"
                                   @click="returnExam(row.item)">Return Exam</b-dropdown-item>
              </template>

              <template v-if="officeFilter != userOffice && officeFilter != 'default'">
                <b-dropdown-item size="sm"
                                 v-if="row.item.offsite_location"
                                 @click="editGroupBooking(row.item)">Edit Booking</b-dropdown-item>
                <b-dropdown-item size="sm"
                                 @click="editExamDetails(row.item)">Edit Exam Details</b-dropdown-item>
              </template>
            </template>

            <template v-if="examReturnedFilter(row.item)">
              <b-dropdown-item size="sm"
                               @click="returnExam(row.item)">Edit Return Details</b-dropdown-item>
            </template>
          </b-dropdown>
        </template>
      </b-table>
    </div>
    <b-pagination :total-rows="totalRows"
                  :per-page="10"
                  v-if="filteredExams().length > 10"
                  v-model="page" />
  </fragment>
</template>

<script>
  import moment from 'moment'
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import EditExamModal from './edit-exam-form-modal'
  import EditGroupExamBookingModal from './edit-group-exam-modal'
  import FailureExamAlert from './failure-exam-alert'
  import OfficeDrop from './office-drop'
  import ReturnExamModal from './return-exam-form-modal'
  import SuccessExamAlert from './success-exam-alert'
  import DeleteExamModal from './delete-exam-modal'
  import AddCitizen from '../add-citizen/add-citizen'
  import zone from 'moment-timezone'

  export default {
    name: "ExamInventoryTable",
    components: {
      AddCitizen,
      DeleteExamModal,
      EditExamModal,
      EditGroupExamBookingModal,
      FailureExamAlert,
      OfficeDrop,
      ReturnExamModal,
      SuccessExamAlert,
    },
    mounted() {
      this.getExams().then( () => { this.getBookings() })
      this.getOffices()
      this.getInvigilators()
      this.getSize()
      this.$nextTick(function() {
        window.addEventListener('resize', () => { this.getSize() })
      })
      this.setFilter({type: 'office_number', value: 'default'})
    },
    data() {
      return {
        actionedExam: {},
        detailsRowSetup: null,
        searchTerm: null,
        officeFilterModal: false,
        page: 1,
        tableStyle: null,
        buttonH: 45,
        qLengthH: 28,
        totalH: 0,
      }
    },
    computed: {
      ...mapGetters(['calendar_events', 'exam_inventory', 'role_code', 'is_liaison_designate' ]),
      ...mapState([
        'bookings',
        'calendarSetup',
        'calendarEvents',
        'exams',
        'inventoryFilters',
        'showDeleteExamModal',
        'showEditExamModal',
        'showExamInventoryModal',
        'showReturnExamModalVisible',
        'offices',
        'user',
      ]),
      availableH() {
        let h = this.totalH - 240
        return { height:`${h}px`, border: '1px solid dimgrey' }
      },
      fields() {
        if (!this.showExamInventoryModal) {
          return [
            { key: 'event_id', label: 'Event ID', sortable: false, thStyle: 'width: 6%' },
            { key: 'exam_type_name', label: 'Exam Type', sortable: true },
            { key: 'exam_name', label: 'Exam Name', sortable: true, thStyle: 'width: 11%' },
            { key: 'exam_method', label: 'Method', sortable: false, thStyle: 'width: 5%' },
            { key: 'expiry_date', label: 'Expiry Date', sortable: true, thStyle: 'width: 8%' },
            { key: 'exam_received', label: 'Received?', sortable: true, thStyle: 'width: 5%' },
            { key: 'examinee_name', label: 'Student Name', sortable: true, thStyle: 'width: 12%' },
            { key: 'notes', label: 'Notes', sortable: false, thStyle: 'width: 21%' },
            { key: 'scheduled', label: 'Scheduled?', sortable: true, thStyle: 'width: 5%', tdClass: 'text-center'},
            { key: 'actions', label: 'Actions', sortable: false, thStyle: 'width: 5%' },
          ]
        }
        if (this.showExamInventoryModal) {
          return [
            { key: 'event_id', label: 'Event ID', sortable: false, thStyle: 'width: 6%' },
            { key: 'exam_type.exam_type_name', label: 'Exam Type', sortable: true},
            { key: 'exam_name', label: 'Exam Name', sortable: true, thStyle: 'width: 15%' },
            { key: 'exam_method', label: 'Method', sortable: true, thStyle: 'width: 5%' },
            { key: 'expiry_date', label: 'Expiry Date', sortable: true, thStyle: 'width: 8%' },
            { key: 'exam_received', label: 'Received?', sortable: true, thStyle: 'width: 5%' },
            { key: 'examinee_name', label: 'Student Name', sortable: true, thStyle: 'width: 20%' },
            { key: 'notes', label: 'Notes', sortable: false, },
          ]
        }
      },
      officeFilter() {
        if (this.inventoryFilters && this.inventoryFilters.office_number) {
          return this.inventoryFilters.office_number
        }
        return ''
      },
      officeName() {
        if (this.offices && this.offices.length > 0) {
          let office = this.offices.find( office => office.office_number==this.officeNumber)
          if (office) {
            return office.office_name
          }
          return 'Invalid Office'
        }
        if (this.user && this.user.office_id) {
          return this.user.office.office_name
        }
        return ''
      },
      officeNumber() {
        if (this.inventoryFilters && this.inventoryFilters.office_number) {
          let { office_number } = this.inventoryFilters
          if (office_number !== 'default') {
            return office_number
          }
        }
        if (this.user && this.user.office_id) {
          return this.user.office.office_number
        }
        return ''
      },
      totalRows() {
        let exams = this.filteredExams() || null
        if (exams && exams.length > 0) {
          return exams.length
        }
        return 10
      },
      userOffice() {
        if (this.user && this.user.office_id) {
          return this.user.office.office_number
        }
        return ''
      },
    },
    methods: {
      ...mapActions(['getBookings', 'getExams', 'getExamsForOffice', 'getInvigilators', 'getOffices',]),
      ...mapMutations([
        'setEditedBooking',
        'setEditedBookingOriginal',
        'setEditExamInfo',
        'setInventoryFilters',
        'setSelectedExam',
        'toggleDeleteExamModal',
        'toggleEditBookingModal',
        'toggleEditExamModal',
        'toggleEditGroupBookingModal',
        'toggleExamInventoryModal',
        'toggleReturnExamModal',
        'toggleScheduling',
      ]),
      addCalendarBooking(item) {
        this.toggleScheduling(true)
        item.referrer = 'inventory'
        this.setSelectedExam(item)
        this.$router.push('/booking')
        this.toggleExamInventoryModal(false)
      },
      checkChallenger(item) {
        if (item.event_id && item.booking.invigilator_id && item.number_of_students) {
          return true
        }
        return false
      },
      checkInvigilator(item) {
        if (item.booking && (item.booking.invigilator_id || item.booking.sbc_staff_invigilated)) {
          return true
        }
        return false
      },
      clickModalRow(item) {
        if (this.showExamInventoryModal) {
          this.toggleScheduling(true)
          this.setSelectedExam(item)
          this.$router.push('/booking')
          this.toggleExamInventoryModal(false)
        }
      },
      editExamDetails(item) {
        this.actionedExam = item
        this.toggleEditExamModal(true)
      },
      editGroupBooking(item) {
        this.actionedExam = item
        this.toggleEditGroupBookingModal(true)
      },
      examReturnedFilter(item) {
        if (item.exam_returned_date && (this.officeFilter === this.userOffice || this.officeFilter === 'default')) {
          return true
        }
        return false
      },
      filterByGroup(ex) {
        if (ex.exam_type.exam_type_name === 'Monthly Session Exam' || ex.exam_type.group_exam_ind) {
          return true
        }
        if (ex.number_of_students && parseInt(ex.number_of_students) > 1) {
          return true
        }
        return false
      },
      filterByScheduled(ex) {
        if (ex.exam_received_date) {
          if (ex.booking && ( ex.booking.invigilator_id || ex.booking.sbc_staff_invigilated )) {
            if (ex.booking.invigilator && ex.booking.invigilator.deleted) {
              return false
            }
            if (ex.exam_type.exam_type_name !== 'Monthly Session Exam') {
              return true
            }
            if (ex.exam_type.exam_type_name === 'Monthly Session Exam') {
              if (ex.number_of_students && ex.event_id) {
                return true
              }
            }
          }
        }
        return false
      },
      filteredExams() {
        let examInventory = this.exam_inventory
        let office_number = this.inventoryFilters.office_number === 'default' ?
          this.user.office.office_number : this.inventoryFilters.office_number
        let filtered = []
        if (examInventory.length > 0) {
          if (this.showExamInventoryModal) {
            filtered = examInventory.filter(ex => moment(ex.expiry_date).isSameOrAfter(moment(), 'day'))
            let moreFiltered = filtered.filter(ex => !ex.booking)
            let evenMoreFiltered = moreFiltered.filter(ex => !ex.offsite_location)
            let { office_id } = this.user
            return evenMoreFiltered.filter(ex => ex.office_id == office_id)
          }
          let exams = examInventory.filter(ex => ex.office.office_number == office_number)
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
              moreFiltered = filtered.filter( x => !this.filterByScheduled(x))
              break
            case 'scheduled':
              moreFiltered = filtered.filter( x => this.filterByScheduled(x))
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
              evenMoreFiltered = moreFiltered.filter(ex => !this.filterByGroup(ex))

              break
            case 'group':
              evenMoreFiltered = moreFiltered.filter(ex => this.filterByGroup(ex))
              break
            default:
              evenMoreFiltered = moreFiltered
              break
          }
          let finalFiltered = []
          switch (this.inventoryFilters.returnedFilter) {
            case 'both':
              finalFiltered = evenMoreFiltered
              break
            case 'returned':
              finalFiltered = evenMoreFiltered.filter(ex => ex.exam_returned_date)
              break
            case 'unreturned':
              finalFiltered = evenMoreFiltered.filter(ex => !ex.exam_returned_date)
              break
            default:
              finalFiltered = evenMoreFiltered
              break
          }
          return finalFiltered
        }
        return []
      },
      formatDate(d) {
        return new moment(d).utc().format('ddd MMM DD, YYYY')
      },
      formatTime(d) {
        let tz = d.office.timezone.timezone_name
        let time =  new zone.tz(d.start_time, tz).format('2017-MM-DD[T]HH:mm:ss').toString()
        return new moment(time).format('h:mm a')
      },
      getSize() {
        this.totalH = window.innerHeight - 70 - 36
        if (!this.showExamInventoryModal) {
          this.tableStyle = { height: `${this.availableH}px`, width: `${ window.innerWidth - 40 }px` }
        }
        if (this.showExamInventoryModal) {
          this.tableStyle = { width: 98 + '%' }
        }
      },
      readyDetailsMap(item) {
        let output = {}
        if (item.offsite_location && item.offsite_location !== '_offsite') {
          output.Location = item.offsite_location
        }
        if (item.booking) {
          if (item.booking.sbc_staff_invigilated) {
            output.Invigilator = 'SBC Staff'
          }
          if (item.booking.invigilator_id && !item.booking.invigilator.deleted) {
            output.Invigilator = item.booking.invigilator.invigilator_name
          }
          if (item.booking.room_id) {
            output.Room = item.booking.room.room_name
          }
          if (item.booking.start_time) {
            output.Date = this.formatDate(item.booking.start_time)
            output.Time = this.formatTime(item.booking)
          }
        }
        return output
      },
      resetActionedExam() {
        this.actionedExam = {}
      },
      resetInvalidOfficeOnHide() {
        if  (this.officeName === 'Invalid Office') {
          this.setFilter({type: 'office_number', value: 'default'})
        }
      },
      returnExam(item) {
        this.actionedExam = item
        this.toggleReturnExamModal(true)
      },
      setFilter(e) {
        this.setInventoryFilters(e)

        if (e.type === "office_number") {
          this.getExamsForOffice(e.value)
        }
      },
      setOfficeFilter(office_number) {
        this.setFilter({type:'office_number', value: office_number})
      },
      setHomeOffice() {
        this.setFilter({type: 'office_number', value: 'default'})
        this.officeFilterModal = false
      },
      sortCompare(a, b, key) {
        if (key === 'scheduled') {
          let val1, val2
          if (this.statusIcon(a).rank !== this.statusIcon(b).rank) {
            val1 = parseInt(this.statusIcon(a).rank)
            val2 = parseInt(this.statusIcon(b).rank)
          }
          if (this.statusIcon(a).rank === this.statusIcon(b).rank) {
            val1 = parseInt(a.exam_id)
            val2 = parseInt(b.exam_id)
          }
          return val1 < val2 ? -1 : val1 > val2 ? 1 : 0
        }
        if (typeof a[key] === 'number' && typeof b[key] === 'number') {
          return a[key] < b[key] ? -1 : a[key] > b[key] ? 1 : 0
        } else {
          return toString(a[key]).localeCompare(toString(b[key]), undefined, {
            numeric: true
          })
        }
        function toString(value) {
          if (!value) {
            return ''
          } else if (value instanceof Object) {
            return keys(value)
            .sort()
            .map(key => toString(value[key]))
            .join(' ')
          }
          return String(value)
        }
      },
      statusIcon(item) {
        let lifeRing = {
          icon: 'life-ring',
          rank: 3,
          style: {fontSize: '1rem', color: 'red'}
        }
        let exclamationTriangle = {
          icon: 'exclamation-triangle',
          rank: 2,
          style: {fontSize: '.9rem', color: '#FFC32B'}
        }
        let clipboardCheck = {
          icon: 'clipboard-check',
          rank: 1,
          style: {fontSize: '1rem', color: 'green'}
        }
        if (item.booking && item.booking.invigilator && item.booking.invigilator.deleted) {
          return lifeRing
        }
        if (item.exam_type.exam_type_name === 'Monthly Session Exam') {
          if (!item.booking) {
            return lifeRing
          }
          if (!item.booking.invigilator_id && !item.booking.sbc_staff_invigilated) {
            return lifeRing
          }
          if (!item.event_id || !item.number_of_students || !item.exam_received_date) {
            return exclamationTriangle
          }
          return clipboardCheck
        }
        if (item.exam_type.group_exam_ind) {
          if (!item.booking) {
            return lifeRing
          }
          if (!item.booking.invigilator_id && !item.booking.sbc_staff_invigilated) {
            return lifeRing
          }
          if (!item.exam_received_date) {
            return exclamationTriangle
          }
          return clipboardCheck
        }
        if (item.booking && (item.booking.invigilator_id || item.booking.sbc_staff_invigilated) &&
            item.exam_received_date) {
          return clipboardCheck
        }
        return exclamationTriangle
      },
      stillRequires(item) {
        let output = []
        if (!item.booking) {
          output.push('Scheduling and Assignment of Invigilator')
        }
        if (!item.exam_received_date) {
          output.push('Receipt of Materials')
        }
        if (item.exam_type.exam_type_name === 'Monthly Session Exam') {
          if (!item.number_of_students) {
            output.push('Number of Students')
          }
          if (!item.event_id) {
            output.push('Event ID')
          }
        }
        if (item.booking) {
          if (item.booking.invigilator && item.booking.invigilator.deleted) {
            output.push('Re-assignment of Invigilator')
          }
          if (!item.booking.invigilator_id && !item.booking.sbc_staff_invigilated) {
            output.push('Assignment of Invigilator')
          }
        }
        return output
      },
      updateCalendarBooking(item) {
        item.gotoDate = new moment(item.booking.start_time)
        item.referrer = 'rescheduling'
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
  .label-text {
    font-size: .9rem;
  }
  .exam-table-holder {
    border: 1px solid dimgrey;
  }
  .tr-container-div {
    min-height: 50% !important;
  }
  .details-slot-div {
    display: flex;
    justify-content: flex-start;
    justify-items: flex-start;
    width: 100%;
    padding-top: 6px;
    padding-bottom: 6px;
  }
  .pagination-class {
    position: fixed;
    bottom: 35px;
    left: 30px;
  }
  .icon-cursor-hover {
    cursor: pointer !important;
  }
  .btn:active, .btn.active {
   background-color: #184368 !important;
   color: white !important;
  }
</style>
