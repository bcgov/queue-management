<template>
  <div>
    <div class="q-w100-flex-fs">
      <b-form inline class="ml-3">
        <b-input-group>
          <b-input-group-prepend><label class="mx-1 pt-1 my-auto label-text">Search</label></b-input-group-prepend>
          <b-input size="sm" class="mb-1 mt-3" v-model="filter"></b-input>
        </b-input-group>
        <b-input-group class="ml-3" v-if="!showExamInventoryModal">
          <b-input-group-prepend>
            <label class="mx-1 pt-1 my-auto label-text">Filters</label>
          </b-input-group-prepend>
          <b-btn-group v-if="role_code === 'LIAISON'" class="pt-2">
            <b-btn @click="officeFilterModal=true"
                   class="btn-sm btn-warning">Office # {{ officeNumber }} - {{ officeName }}</b-btn>
          </b-btn-group>
          <b-button-group horizontal
                          class="ml-2 pt-2"
                          label="Expired Exam Filters">
            <b-button size="sm"
                      :pressed="inventoryFilters.expiryFilter==='all'"
                      @click="handleFilter({type:'expiryFilter', value:'all'})"
                      variant="primary">
              <span class="mx-2">All</span>
            </b-button>
            <b-button size="sm"
                      :pressed="inventoryFilters.expiryFilter==='expired'"
                      @click="handleFilter({type:'expiryFilter', value:'expired'})"
                      variant="primary">Expired</b-button>
            <b-button size="sm"
                      :pressed="inventoryFilters.expiryFilter==='current'"
                      @click="handleFilter({type:'expiryFilter', value:'current'})"
                      variant="primary">Current</b-button>
          </b-button-group>
          <b-btn-group horizontal class="ml-2 pt-2">
            <b-btn size="sm"
                   :pressed="inventoryFilters.scheduledFilter==='both'"
                   @click="handleFilter({type:'scheduledFilter', value:'both'})"
                   variant="primary">
              <span class="mx-2">Both</span>
            </b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.scheduledFilter==='unscheduled'"
                   @click="handleFilter({type:'scheduledFilter', value:'unscheduled'})"
                   variant="primary">Un-Scheduled</b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.scheduledFilter==='scheduled'"
                   @click="handleFilter({type:'scheduledFilter', value:'scheduled'})"
                   variant="primary">Scheduled</b-btn>
          </b-btn-group>
          <b-btn-group horizontal class="ml-2 pt-2">
            <b-btn size="sm"
                   :pressed="inventoryFilters.groupFilter==='both'"
                   @click="handleFilter({type:'groupFilter', value:'both'})"
                   variant="primary"><span class="mx-2">Both</span></b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.groupFilter==='individual'"
                   @click="handleFilter({type:'groupFilter', value:'individual'})"
                   variant="primary">Individual</b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.groupFilter==='group'"
                   @click="handleFilter({type:'groupFilter', value:'group'})"
                   variant="primary">Group</b-btn>
          </b-btn-group>
          <b-btn-group horizontal class="ml-2 pt-2">
            <b-btn size="sm"
                   :pressed="inventoryFilters.returnedFilter==='both'"
                   @click="handleFilter({type:'returnedFilter', value:'both'})"
                   variant="primary"><span class="mx-2">Both</span></b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.returnedFilter==='returned'"
                   @click="handleFilter({type:'returnedFilter', value:'returned'})"
                   variant="primary">Returned</b-btn>
            <b-btn size="sm"
                   :pressed="inventoryFilters.returnedFilter==='notReturned'"
                   @click="handleFilter({type:'returnedFilter', value:'notReturned'})"
                   variant="primary">Not Returned</b-btn>
          </b-btn-group>
        </b-input-group>
      </b-form>
    </div>
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
               :current-page="page"
               :per-page="10"
               :filter="filter">
        <template slot="exam_received" slot-scope="row">
          {{ row.item.exam_received_date ? 'Yes' : 'No' }}
        </template>

        <template slot="exam_type_name" slot-scope="row">
          <div v-if="row.item.exam_type.exam_type_name.includes('Group')"
               :style="{color: row.item.exam_type.exam_color}">
            {{ row.item.exam_type.exam_type_name }}
          </div>
          <div v-else-if="row.item.exam_type.exam_type_name.includes('Single')"
               :style="{color: row.item.exam_type.exam_color}">
               {{ row.item.exam_type.exam_type_name }}
          </div>
          <div v-else>{{ row.item.exam_type.exam_type_name }}</div>
        </template>

        <template slot="expiry_date" slot-scope="row">
          <span v-if="row.item.exam_type.exam_type_name === 'Challenger Exam Session'">–</span>
          <span v-else-if="row.item.examinee_name === 'group exam'">–</span>
          <span v-else>{{ formatDate(row.item.expiry_date) }}</span>
        </template>

        <template slot="scheduled" slot-scope="row">
          <template v-if="row.item.exam_type.exam_type_name === 'Challenger Exam Session'">
            <b-button v-if="checkChallenger(row.item)"
                      class="btn-link"
                      style="border: none;"
                      @click.stop="handleDetails({row, origin: 'button'})">
              {{ row.detailsShowing ? 'Hide' : 'Show' }}
            </b-button>
            <template v-else>
              <font-awesome-icon v-if="!row.detailsShowing"
                                 icon="exclamation-triangle"
                                 @click.stop="handleDetails({row, origin: 'error'})"
                                 class="m-0 p-0 error-cursor-hover"
                                 style="font-size:1rem;color:#ffc32b"/>
              <b-button v-if="row.detailsShowing"
                        class="btn-link"
                        style="border: none;"
                        @click.stop="handleDetails({row, origin: 'button'})">Hide</b-button>
            </template>
          </template>
          <template v-if="row.item.exam_type.exam_type_name !== 'Challenger Exam Session'">
            <b-button v-if="row.item.booking && (row.item.booking.invigilator_id || row.item.booking.sbc_staff_invigilated)"
                      class="btn-link"
                      style="border: none;"
                      @click.stop="handleDetails({row, origin:'button'})">{{ row.detailsShowing ? 'Hide' : 'Show'}}
            </b-button>
            <template v-else>
              <font-awesome-icon v-if="!row.detailsShowing"
                                 icon="exclamation-triangle"
                                 @click.stop="handleDetails({row, origin: 'error'})"
                                 class="m-0 p-0 error-cursor-hover"
                                 style="font-size:1rem;color:#ffc32b"/>
              <b-button v-if="row.detailsShowing"
                        class="btn-link"
                        style="border: none;"
                        @click.stop="handleDetails({row, origin: 'button'})">Hide</b-button>
            </template>
          </template>
        </template>

        <template slot="row-details" slot-scope="row">
          <template v-if="detailsSetup === 'button'">
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
          <template v-if="detailsSetup === 'error'">
            <div class="details-slot-div">
              <div class="ml-3" style="font-size: 1rem;">Still Requires:</div>
              <template v-if="row.item.exam_type.exam_type_name.includes('Single')">
                <div v-if="!row.item.booking"
                     class="ml-3 mt-1">Scheduling</div>
                <div
                  v-if="row.item.booking && (!row.item.booking.invigilator_id || !row.item.booking.sbc_staff_invigilated)"
                  class="ml-3 mt-1">Assignment of Invigilator</div>
              </template>
              <template v-else-if="row.item.exam_type.exam_type_name.includes('Group')">
                <div v-if="!row.item.booking.invigilator_id"
                     class="ml-3 mt-1">Assignment of Invigilator</div>
              </template>
              <template v-else-if="row.item.exam_type.exam_type_name === 'Challenger Exam Session'">
                <div v-if="!row.item.booking.invigilator_id"
                     class="ml-3 mt-1">Assignment of Invigilator</div>
                <div v-if="!row.item.number_of_students"
                     class="ml-3 mt-1">Number of Students</div>
                <div v-if="!row.item.event_id"
                     class="ml-3 mt-1">Event ID</div>
              </template>
              <template v-else>
                <div v-if="!row.item.booking"
                     class="ml-3 mt-1">Scheduling</div>
                <div
                  v-if="row.item.booking && !row.item.booking.invigilator_id || !row.item.booking.sbc_staff_invigilated"
                  class="ml-3 mt-1">Assignment of Invigilator</div>
              </template>
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
            <template v-if="officeFilter == userOffice || officeFilter == 'default'">
              <template v-if="row.item.exam_type.exam_type_name === 'Challenger Exam Session'">
                <b-dropdown-item size="sm"
                                 v-if="row.item.offsite_location"
                                 @click="editGroupExam(row.item)">
                  {{ row.item.booking.invigilator_id ? 'Update Booking' : 'Add Invigilator' }}
                </b-dropdown-item>
                <b-dropdown-item size="sm"
                                 v-if="!row.item.offsite_location"
                                 @click="updateBookingRoute(row.item)">
                  {{ row.item.booking.invigilator_id ? 'Update Booking' : 'Add Invigilator' }}
                </b-dropdown-item>
              </template>
              <template v-if="row.item.exam_type.exam_type_name !== 'Challenger Exam Session'">
                <template v-if="row.item.offsite_location">
                  <b-dropdown-item size="sm"
                                   v-if="row.item.offsite_location"
                                   @click="editGroupExam(row.item)">
                    {{ row.item.booking.invigilator_id ? 'Update Booking jj' : 'Add Invigilator jj' }}</b-dropdown-item>
                </template>
                <template v-if="!row.item.offsite_location">
                  <b-dropdown-item v-if="!row.item.booking"
                                   size="sm"
                                   @click="addBookingRoute(row.item)">Schedule Exam</b-dropdown-item>
                  <b-dropdown-item v-else
                                   size="sm"
                                   @click="updateBookingRoute(row.item)">Update Booking</b-dropdown-item>
                </template>
              </template>
              <b-dropdown-item size="sm"
                               @click="editExam(row.item)">Edit Exam Details</b-dropdown-item>
              <b-dropdown-item size="sm"
                               @click="returnExamInfo(row.item)">Return Exam</b-dropdown-item>
            </template>
            <template v-if="officeFilter != userOffice && officeFilter != 'default'">
              <b-dropdown-item size="sm"
                               @click="editExam(row.item)">Edit Exam Details</b-dropdown-item>
            </template>
          </b-dropdown>
        </template>
      </b-table>
      <div v-if="filteredExams().length > 10 && !showReturnExamModalVisible"
           class="pagination-class">
        <b-pagination
          :total-rows="totalRows"
          :per-page="10"
          v-model="page" />
      </div>
      <div v-if="filteredExams().length > 10 && showReturnExamModalVisible">
          <b-pagination
            :total-rows="totalRows"
            :per-page="10"
            v-model="page" />
        </div>
    </div>
    <EditExamModal :examRow="examRow" :resetExam="resetEditedExam" />
    <ReturnExamModal v-if="showReturnExamModalVisible" />
    <EditGroupExamBookingModal :examRow="examRow" :resetExam="resetEditedExam" />
    <DeleteExamModal v-if="showDeleteExamModal" />
    <b-modal v-model="officeFilterModal"
               size="sm"
               centered
               hide-backdrop
               @hide="checkValid()"
               hide-header
               hide-footer>
        <h5>View Another Office</h5>
        <p>To search, start typing or enter an office #</p>
        <b-form>
          <b-form-row>
            <OfficeDrop columnW="8" :office_number="officeNumber" :setOffice="setOffice"/>
          </b-form-row>
        </b-form>
        <div style="display:flex; justify-content: space-between">
          <b-button class="mr-2 btn-secondary"
                    @click="handleFilter({type: 'office_number', value: 'default'})">This Office</b-button>
          <b-button class="ml-2 btn-primary"
                    @click="officeFilterModal=false">Ok</b-button>
        </div>
      </b-modal>
  </div>
</template>

<script>
  import moment from 'moment'
  import Vue from 'vue'
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import EditExamModal from './edit-exam-form-modal'
  import EditGroupExamBookingModal from './edit-group-exam-modal'
  import FailureExamAlert from './failure-exam-alert'
  import OfficeDrop from './office-drop'
  import ReturnExamModal from './return-exam-form-modal'
  import SuccessExamAlert from './success-exam-alert'
  import DeleteExamModal from './delete-exam-modal'

  export default {
    name: "ExamInventoryTable",
    components: {
      DeleteExamModal,
      EditExamModal,
      EditGroupExamBookingModal,
      FailureExamAlert,
      OfficeDrop,
      ReturnExamModal,
      SuccessExamAlert,
    },
    mounted() {
      this.getOffices()
      this.getInvigilators()
      this.getExams().then( () => { this.getBookings() })
      this.getWidth()
      this.$nextTick(function() {
        window.addEventListener('resize', () => { this.getWidth() })
      })
      this.handleFilter({type: 'office_number', value: 'default'})
    },
    data() {
      return {
        officeFilterModal: false,
        events: null,
        examRow: {},
        filter: null,
        page: 1,
        tableStyle: null,
        detailsSetup: null,
      }
    },
    computed: {
      ...mapGetters(['calendar_events', 'exam_inventory', 'role_code', ]),
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
      officeFilter() {
        if (this.inventoryFilters && this.inventoryFilters.office_number) {
          return this.inventoryFilters.office_number
        }
        return ''
      },
      userOffice() {
        if (this.user && this.user.office_id) {
          return this.user.office.office_number
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
      totalRows() {
        let exams = this.filteredExams() || null
        if (exams && exams.length > 0) {
          return exams.length
        }
        return 10
      },
      fields() {
        if (!this.showExamInventoryModal) {
          return [
            { key: 'office.office_name', label: 'Office', sortable: true, thStyle: 'width: 8%' },
            { key: 'event_id', label: 'Event ID', sortable: true, thStyle: 'width: 6%' },
            { key: 'exam_type_name', label: 'Exam Type', sortable: true },
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
            { key: 'exam_type.exam_type_name', label: 'Exam Type', sortable: true},
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
      },
    },
    methods: {
      ...mapActions(['getBookings', 'getExams', 'getInvigilators', 'getOffices',]),
      ...mapMutations([
        'setEditedBooking',
        'setEditedBookingOriginal',
        'setEditExamInfo',
        'setInventoryFilters',
        'setReturnExamInfo',
        'setSelectedExam',
        'toggleDeleteExamModalVisible',
        'toggleEditBookingModal',
        'toggleEditExamModal',
        'toggleEditGroupBookingModal',
        'toggleExamInventoryModal',
        'toggleReturnExamModalVisible',
        'toggleScheduling',
      ]),
      checkValid() {
        if  (this.officeName === 'Invalid Office') {
          this.handleFilter({type: 'office_number', value: 'default'})
        }
      },
      addBookingRoute(item) {
        this.toggleScheduling(true)
        item.referrer = 'scheduling'
        this.setSelectedExam(item)
        this.$router.push('/booking')
        this.toggleExamInventoryModal(false)
      },
      setOffice(office_number) {
        this.handleFilter({type:'office_number', value: office_number})
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
        this.examRow = item
        this.toggleEditExamModal(true)
      },
      editGroupExam(item) {
        this.examRow = item
        this.toggleEditGroupBookingModal(true)
      },
      handleDetails(item) {
        this.detailsSetup = item.origin
        item.row.toggleDetails()
      },
      filteredExams() {
        let examInventory = this.exam_inventory
        let filtered = []
        if (examInventory.length > 0) {
          if (this.showExamInventoryModal) {
            filtered = examInventory.filter(ex => moment(ex.expiry_date).isSameOrAfter(moment(), 'day'))
            let moreFiltered = filtered.filter(ex => !ex.booking)
            let evenMoreFiltered = moreFiltered.filter(ex => !ex.offsite_location)
            let { office_id } = this.user
            return evenMoreFiltered.filter(ex => ex.office_id == office_id)
          }
          let office_number = this.inventoryFilters.office_number === 'default' ?
                          this.user.office.office_number : this.inventoryFilters.office_number
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
              evenMoreFiltered = moreFiltered.filter(ex => !this.groupFilter(ex))

              break
            case 'group':
              evenMoreFiltered = moreFiltered.filter(ex => this.groupFilter(ex))
              break
            default:
              evenMoreFiltered = moreFiltered
              break
          }
          let manyMoreFiltered = []
          switch (this.inventoryFilters.returnedFilter) {
            case 'both':
              manyMoreFiltered = evenMoreFiltered
              break
            case 'returned':
              manyMoreFiltered = evenMoreFiltered.filter(ex => ex.exam_returned_ind === 1)
              break
            case 'notReturned':
              manyMoreFiltered = evenMoreFiltered.filter(ex => ex.exam_returned_ind === 0)
              break
            default:
              manyMoreFiltered = evenMoreFiltered
              break
          }
          return manyMoreFiltered
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
      checkChallenger(item) {
        if (item.event_id && item.booking.invigilator_id && item.number_of_students) {
          return true
        }
        return false
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
      groupFilter(ex) {
        if (ex.exam_type.exam_type_name === 'Challenger Exam Session') {
          return true
        }
        if (ex.exam_type.exam_type_name !== 'Challenger Exam Session' && ex.offsite_location) {
          return true
        }
        return false
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
  .error-cursor-hover {
    cursor: pointer !important;
  }
  .btn:active, .btn.active {
   background-color: #184368 !important;
   color: white !important;
 }
</style>
