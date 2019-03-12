<template>
  <b-modal v-model="showModal"
           :no-close-on-backdrop="true"
           hide-header
           hide-footer
           @hidden="reset"
           @shown="populateForm"
           size="md">
    <div v-if="exam">
      <b-table v-show="false"
               v-if="role_code==='LIAISON'"
               :items="offices"
               :fields="{key: 'office_name'}"
               :filter="search"
               @filtered="getFilteredOffices" />
      <span style="font-size: 1.4rem; font-weight: 600;">Edit Exam</span>
      <b-form v-if="showAllFields">
        <b-form-row v-if="role_code === 'LIAISON' && examType === 'group'">
          <b-col>
            <b-form-group>
              <label class="my-0">Office (Start typing below to search or enter Office Number )</label>
              <div>
                <b-form-input id="office_name"
                              type="text"
                              class="less-10-mb"
                              :value="officeSearch"
                              @focus.native="officeSearchOnFocus"
                              @blur.native="officeSearchOnBlur"
                              @input.native="handleOfficeInput" />
              </div>
              <div :class="officeDropClass"
                   style="border: 1px solid grey">
                <template v-for="office in officeChoices">
                  <b-dropdown-item-button v-on:click.prevent="handleOfficeDropClick"
                                          :name="office.office_name"
                                          :value="office.office_number"
                                          :id="office.office_id">{{ office.office_name }}</b-dropdown-item-button>
                </template>
              </div>
            </b-form-group>
          </b-col>
          <b-col cols="2">
            <b-form-group>
              <label class="my-0">Office #</label>
              <b-form-input id="office_id"
                            type="number"
                            class="less-10-mb"
                            :value="office_number"
                            @input.native="handleOfficeNumberInput" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col cols="6">
            <b-form-group>
              <label class="my-0">Event ID</label>
              <b-form-input id="event_id"
                            type="text"
                            class="less-10-mb"
                            v-model="fields.event_id" />
            </b-form-group>
          </b-col>
          <b-col cols="6">
            <b-form-group>
              <label class="my-0">Exam Method</label><br>
              <b-select id="exam_method"
                        class="less-10-mb"
                        v-model="fields.exam_method"
                        :options="methodOptions" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row v-if="examType !== 'challenger' ">
            <b-col>
              <b-form-group>
                <label class="my-0">Exam Type</label><br>
                <div @click="handleExamInputClick">
                  <b-input read-only
                           class="less-15-mb"
                           :value="examInputText"
                           placeholder="click here to see options"
                           :style="examInputStyle" />
                </div>
                <div :class="examTypeDropClass"
                     style="border: 1px solid grey"
                     @click="handleExamInputClick">
                  <template v-for="type in examTypeDropItems">
                    <b-dd-header v-if="type.header"
                                 :style="{backgroundColor: type.exam_color}"
                                 :class="type.class">{{ type.exam_type_name }}</b-dd-header>
                    <b-dd-item v-else :style="{backgroundColor: type.exam_color}"
                               @click="handleExamDropClick"
                               :value="type.exam_type_id"
                               :id="type.exam_type_id"
                               :class="type.class">{{ type.exam_type_name }}</b-dd-item>
                  </template>
                </div>
              </b-form-group>
            </b-col>
          </b-form-row>
        <b-form-row v-if="examType === 'challenger'">
          <b-col>
            <b-form-group>
              <label class="mb-0 mt-1">Exam Type</label>
              <b-form-input id="exam_name" type="text"
                            class="less-10-mb"
                            disabled
                            value="Challenger Exam Session" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group>
              <label class="mb-0 mt-1">Exam Name</label>
              <b-form-input id="exam_name" type="text"
                            class="less-10-mb"
                            v-model="fields.exam_name" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col :col="!this.fields.exam_received_date" :cols="this.exam_received ? 3 : '' ">
            <b-form-group>
              <label class="my-0">Exam Received?</label>
              <b-select id="exam_received"
                        v-model="exam_received"
                        @input="updateExamReceived"
                        class="less-10-mb"
                        :options="examReceivedOptions" />
            </b-form-group>
          </b-col>
          <b-col v-if="exam_received">
            <b-form-group>
              <label class="my-0">Received Date</label><br>
              <DatePicker v-model="fields.exam_received_date"
                          id="exam_received_date"
                          input-class="form-control"
                          class="w-100 my-0 less-10-mb"
                          lang="en">
                <template slot="calendar-icon">
                  <font-awesome-icon icon="clock"
                                     class="m-0 p-0"
                                     style="font-size: .9rem;"/>
                </template>
              </DatePicker>
            </b-form-group>
          </b-col>
          <b-col v-if="examType === 'group' || examType === 'challenger'" col>
            <b-form-group>
              <label class="my-0"># of Writers</label><br>
              <b-input v-model="fields.number_of_students"
                       id="number_of_students" />
            </b-form-group>
          </b-col>
          <b-col class="w-100" v-if="examType === 'individual'">
            <b-form-group>
              <label class="my-0">Expiry Date</label><br>
              <DatePicker v-model="fields.expiry_date"
                          id="exam_expiry"
                          input-class="form-control"
                          class="w-100 less-10-mb"
                          lang="en">
                <template slot="calendar-icon">
                  <font-awesome-icon icon="clock"
                                     class="m-0 p-0"
                                     style="font-size: .9rem;"/>
                </template>
              </DatePicker>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row v-if="examType === 'individual' || examType === 'other'">
          <b-col>
            <b-form-group>
              <label class="my-0">Writer's Name</label>
              <b-form-input id="examinee_name"
                            class="less-10-mb"
                            type="text"
                            v-model="fields.examinee_name" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group>
              <label class="my-0">Notes</label><br>
              <b-textarea id="notes" v-model="fields.notes" :rows="2" />
            </b-form-group>
          </b-col>
        </b-form-row>
      </b-form>
      <b-form v-if="!showAllFields">
        <b-form-row>
          <b-col class="mb-2">
            <div class="q-info-display-grid-container">
              <div class="q-id-grid-outer">
                <div class="q-id-grid-head">Exam Details:</div>
                <div class="q-id-grid-col">
                  <div>Exam:</div>
                  <div>{{ this.exam.exam_name }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Event ID:</div>
                  <div>{{ this.exam.event_id }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Type:</div>
                  <div v-if="isITAGropOrSingleExam(exam)"
                       :style="{color: exam.exam_type.exam_color}">{{ exam.exam_type.exam_type_name }}</div>
                  <div v-else>{{ exam.exam_type.exam_type_name }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Method:</div>
                  <div>{{ this.exam.exam_method }}</div>
                </div>
              </div>
            </div>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group>
              <label class="my-0">Exam Received?</label>
              <b-select id="exam_received"
                        class="less-10-mb"
                        @input="updateExamReceived"
                        :options="examReceivedOptions"
                        v-model="exam_received" />
            </b-form-group>
          </b-col>
          <b-col v-if="exam_received" cols="6">
            <b-form-group>
              <label class="my-0">Date Received</label><br>
              <DatePicker v-model="fields.exam_received_date"
                          id="exam_received_date"
                          input-class="form-control"
                          class="w-100 my-0 less-10-mb"
                          lang="en"/>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group>
              <label class="my-0">Notes</label><br>
              <b-textarea id="notes" v-model="fields.notes" :rows="2" />
            </b-form-group>
          </b-col>
        </b-form-row>
      </b-form>
      <div v-if="showMessage"
           class="mb-3"
           style="color: red;">{{ this.message }}</div>
      <div style="display: flex; justify-content: flex-end; width: 100%">
        <b-btn class="btn-danger mr-2"
               @click="deleteExam()">Delete Exam</b-btn>
        <b-btn class="btn-secondary mr-2"
               @click="toggleEditExamModal(false)">Cancel</b-btn>
        <b-btn v-if="!allowSubmit()"
               class="btn-primary disabled"
               @click="setMessage">Submit</b-btn>
        <b-btn v-else-if="allowSubmit()"
               class="btn-primary"
               @click="submit">Submit</b-btn>
      </div>
    </div>
  </b-modal>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import DatePicker from 'vue2-datepicker'
  import moment from 'moment'
  import Vue from 'vue'
  import DeleteExamModal from './delete-exam-modal'

  export default {
    name: "EditExamModal",
    components: { DatePicker,
                  DeleteExamModal},
    props: ['examRow', 'resetExam'],
    data () {
      return {
        clickedMenu: false,
        examReceivedOptions: [
          { value: false, text: 'No' },
          { value: true, text: 'Yes' },
        ],
        fields: {},
        message: '',
        methodOptions: [
          { text: 'paper', value: 'paper'},
          { text: 'online', value: 'online'},
        ],
        exam_received: false,
        office_number: null,
        officeChoices: [],
        showMessage: false,
        showSearch: false,
        searching: false,
        search: '',
      }
    },
    computed: {
      ...mapGetters(['exam_object_id', 'role_code']),
      ...mapState(['editExamFailure',
                   'editExamSuccess',
                   'examTypes',
                   'offices',
                   'showEditExamModal',
                   'showDeleteExamModal', ]),
      exam() {
        if (Object.keys(this.examRow).length > 0) {
          return this.examRow
        }
        return false
      },
      examInputStyle() {
        if (this.examObject) {
          let { exam_color } = this.examObject
          return { border: `1px solid ${exam_color}`, boxShadow: `inset 0px 0px 0px 3px ${exam_color}`, }
        }
        return ''
      },
      examInputText() {
        if (this.examObject) {
          return this.examObject.exam_type_name
        }
        return ''
      },
      examObject() {
        if (this.fields && this.fields.exam_type_id) {
          return this.exam_object_id(this.fields.exam_type_id)
        }
        return ''
      },
      examType() {
        if (this.exam && this.exam.exam_type && this.exam.exam_type.ita_ind) {
          if (this.exam.exam_type.exam_type_name === 'Challenger Exam Session') {
            return 'challenger'
          }
          if (this.exam.offsite_location) {
            return 'group'
          }
          return 'individual'
        }
        return 'other'
      },
      examTypeDropClass() {
        if (!this.clickedMenu) {
          return 'dropdown-menu'
        }
        if (this.clickedMenu) {
          return 'dropdown-menu show py-0 my-0 w-100'
        }
      },
      examTypeDropItems() {
        if (this.exam) {
          if (this.exam.offsite_location) {
            return this.examTypes.filter(type => type.exam_type_name.includes('Group'))
          }
          if (!this.exam.offsite_location) {
            return this.examTypes.filter(type => type.exam_type_name.includes('Single'))
          }
        }
        return []
      },
      officeDropClass() {
        if (!this.showSearch) {
          return 'dropdown-menu'
        }
        if (this.showSearch) {
          return 'dropdown-menu show py-0 my-0 w-100'
        }
      },
      officeSearch() {
        if (!this.searching && this.office_number) {
          return this.offices.find(office=>office.office_number == this.office_number).office_name
        }
        return this.search
      },
      showAllFields() {
        if (this.exam) {
          if (this.exam.exam_type.exam_type_name === 'Challenger Exam Session') {
            if (this.role_code === 'GA') {
              return true
            }
            return false
          }
          if (!this.exam.offsite_location) {
            return true
          }
          if (this.exam.offsite_location) {
            if (this.role_code === 'GA' || this.role_code === 'LIAISON') {
              return true
            }
          }
        }
        return false
      },
      showModal: {
        get() {
          return this.showEditExamModal
        },
        set(e) {
          this.toggleEditExamModal(e)
        }
      }
    },
    methods: {
      ...mapActions(['getBookings', 'getExams', 'getOffices', 'putExamInfo',]),
      ...mapMutations(['setEditExamFailure',
                       'setEditExamSuccess',
                       'setSelectedExam',
                       'setReturnExamInfo',
                       'setReturnDeleteExamInfo',
                       'toggleEditExamModal',
                       'toggleDeleteExamModalVisible']),
      allowSubmit() {
        if (this.examRow) {
          let fieldsEdited = false
          let fields = Object.keys(this.fields)
          for (let key of fields) {
            if (this.fields[key] != this.examRow[key]) {
              fieldsEdited = true
              this.showMessage = false
              break
            }
          }
          return fieldsEdited
        }
        return false
      },
      isITAGropOrSingleExam(ex) {
        if (ex.exam_type.exam_type_name.includes('Group') || ex.exam_type.exam_type_name.includes('Single') ) {
          return true
        }
        return false
      },
      deleteExam() {
        let deleteExamInfo = {}

        if (this.fields.booking_id) {
          deleteExamInfo = {
            booking_id: this.fields.booking_id,
            exam_id: this.fields.exam_id,
            exam_name: this.fields.exam_name,
            examinee_name: this.fields.examinee_name,
            event_id: this.fields.event_id,
          }
        }else {
          deleteExamInfo = {
            booking_id: null,
            exam_id: this.fields.exam_id,
            exam_name: this.fields.exam_name,
            examinee_name: this.fields.examinee_name,
            event_id: this.fields.event_id,
          }
        }
        this.toggleDeleteExamModalVisible(true)
        this.setReturnExamInfo(deleteExamInfo)
      },
      getFilteredOffices(offices) {
        if (offices.length === 0) {
          this.officeChoices = [{office_id: null, office_name: 'No offices found with those letters'}]
          return
        }
        this.officeChoices = offices.length >= 4 ? offices.slice(0,4) : offices
      },
      handleExamDropClick(e) {
        this.fields.exam_type_id = e.target.id
      },
      handleExamInputClick() {
        if (!this.clickedMenu) {
          this.clickedMenu = true
          return
        }
        this.clickedMenu = false
      },
      handleOfficeDropClick(e) {
        this.showSearch = false
        this.fields.office_id = e.target.id
        this.search = e.target.name
        this.office_number = e.target.value
        this.searching = false
      },
      handleOfficeInput(e) {

        this.searching = true
        this.search = e.target.value
        if (this.search.length > 1 && this.searching === true) {
          this.showSearch = true
        }
        if (this.search.length <= 1) {
          this.showSearch = false
        }
      },
      handleOfficeNumberInput(e) {
        let { value } = e.target
        if (value.length <= 2) {
          this.office_number = value
        } else {
          this.office_number = value.slice(value.length-2, value.length)
        }
        if (this.offices.find(office=>office.office_number == this.office_number)) {
          let office = this.offices.find(office=>office.office_number == this.office_number)
          this.search = office.office_name
          this.fields.office_id = office.office_id
        } else {
          this.search = 'Invalid office number entered.'
          this.fields.office_id = null
        }
      },
      officeSearchOnBlur() {
        this.searching = false
      },
      officeSearchOnFocus() {
        this.searching = true
        this.search = ''
      },
      populateForm() {
        let exam = this.examRow
        Object.keys(this.examRow).forEach( key => {
          if (typeof exam[key] === 'string' || typeof exam[key] === 'number') {
            Vue.set(
              this.fields,
              key,
              exam[key]
            )
          }
          if ( key === 'exam_received_date' ) {
            this.fields[key] = this.exam[key]
          }
        })
        if (this.fields.exam_received_date) {
          this.exam_received = true
        }
        if (this.role_code === 'LIAISON') {
          let office = this.offices.find(office => office.office_id == this.exam.office_id)
          this.search = office.office_name
          this.office_number = office.office_number
        }
      },
      reset() {
        Object.keys(this.fields).forEach(key => {
          Vue.set(
            this.fields,
            key,
            null
          )
        })
        this.clickedMenu = false
        this.message = null
        this.office_number = null
        this.exam_received = false
        this.search = ''
        this.searching = false
        this.showMessage = false
        this.showSearch = false
        this.resetExam()
      },
      setMessage() {
        if (!this.allowSubmit()) {
          if (!this.fields.office_id) {
            this.message = 'Please specify a valid office.'
          } else {
            this.message = 'Nothing has changed.  All fields contain their original values.'
          }
          this.showMessage = true
        }
      },
      submit() {
        let putRequest = {
          exam_id: this.fields.exam_id
        }
        Object.keys(this.fields).forEach( key => {
          if (this.fields[key] != this.examRow[key]) {
            putRequest[key] = this.fields[key]
          }
        })
        if (!this.exam_received && this.examRow.exam_received_date) {
          putRequest['exam_received_date'] = null
        }
        this.putExamInfo(putRequest).then( () => {
          this.getExams()
          this.setEditExamSuccess(true)
          this.toggleEditExamModal(false)
        })
      },
      updateExamReceived(e) {
        let { exam_received_date } = this.fields
        if (e && !exam_received_date) {
          this.fields['exam_received_date'] = new moment().utc().format('YYYY-MM-DD[T]hh:mm:ssZ')
          return
        }
        if (!e && exam_received_date) {
          this.fields['exam_received_date'] = null
        }
      }
    },
  }
</script>

<style scoped>
  .less-10-mb {
    margin-bottom: -10px !important;
  }
  .less-15-mb {
    margin-bottom: -15px !important;
  }
  .id-grid-1st-col {
    margin-left: auto;
    margin-right: 20px;
  }
  .id-grid-1st-col {
    grid-column: 1 / span 2;
    margin-right: 20px;
  }
</style>
