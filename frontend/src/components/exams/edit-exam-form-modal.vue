<template>
  <b-modal v-model="showModal" :no-close-on-backdrop="true" hide-header hide-footer @hidden="reset"
    @shown="populateForm" :size="(examType === 'pest') ? 'lg' : 'md'">
    <FailureExamAlert class="m-0 p-0" />
    <div v-if="exam">
      <span style="font-size: 1.4rem; font-weight: 600">Edit/Print Exam Details</span>

      <!--  Start of template for pesticide exams  -->
      <template v-if="examType === 'pest'">
        <b-form>
          <b-form-row>
            <b-col>
              <b-form-group>
                <label class="mb-0 mt-1">Exam Type</label>
                <b-form-input :value="exam.exam_name" class="less-10-mb form-control" disabled id="exam_name"
                  type="text" />
              </b-form-group>
            </b-col>
            <b-col>
              <label class="my-0">Retrieve Exam and Print</label>
              <b-btn class="btn-success w-100" @click="checkAndDownloadExam()">Print</b-btn>
            </b-col>
            <b-col :col="!this.fields.exam_received_date" :cols="this.exam_received ? '' : 3">
              <b-form-group>
                <label class="my-0">Exam Printed?</label>
                <b-select id="exam_received" v-model="exam_received" @input="updateExamReceived" class="less-10-mb"
                  :options="examReceivedOptions" />
              </b-form-group>
            </b-col>
            <b-col v-if="exam_received">
              <b-form-group>
                <label class="my-0">Printed Date</label><br />
                <DatePicker :value="fields.exam_received_date" @input="handleDate" format="YYYY-MM-DD"
                  value-type="format" lang="en" id="exam_received_date" input-class="form-control"
                  class="w-100 my-0 less-10-mb">
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row v-if="examNotReady">
            <b-col cols="12" style="color: red">
              This exam is not yet ready for retrieval. Please try again in no
              less than 15 minutes.
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group>
                <label class="my-0">Candidate's Name</label>
                <b-form-input id="examinee_name" class="less-10-mb" type="text" v-model="fields.examinee_name" />
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group>
                <label class="my-0">Telephone</label><br />
                <b-form-input id="examinee_phone" class="less-10-mb" type="text" v-model="fields.examinee_phone" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group>
                <label class="my-0">Candidate's Email</label>
                <b-form-input id="examinee_email" class="less-10-mb" type="text" v-model="fields.examinee_email" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row class="mt-2">
            <b-col>
              <b-form-group class="mb-0">
                <label class="mb-0">Notes</label><br />
                <b-textarea v-model="fields.notes" :maxlength="400" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label class="my-0">Event ID</label>
                <b-form-input id="event_id" type="text" class="less-10-mb" v-model="fields.event_id" />
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label class="my-0">Expiry Date</label><br />
                <DatePicker v-model="fields.expiry_date" lang="en" id="exam_expiry" format="YYYY-MM-DD"
                  value-type="format" input-class="form-control" class="w-100 less-10-mb">
                  <template slot="calendar-icon">
                    <font-awesome-icon icon="clock" class="m-0 p-0" style="font-size: 0.9rem" />
                  </template>
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col :cols="feesOptions === 'collect' ? 12 : 5">
              <b-form-group><label class="my-0">Fees</label>
                <b-form-select v-model="feesOptions" :disabled="feesOptions === 'liaison'">
                  <option value="liaison" disabled>Collected By Liason</option>
                  <option value="paid">Collect Now</option>
                  <option value="collect">Collect at Exam Time</option>
                </b-form-select>
              </b-form-group>
            </b-col>
            <b-col cols="7" v-if="feesOptions !== 'collect'">
              <b-form-group><label class="my-0">Receipt</label>
                <b-input :disabled="feesOptions === 'liaison'" v-model="fields.receipt" />
              </b-form-group>
            </b-col>
            <b-col cols="12" v-if="feesOptions !== 'collect'">
              <b-form-group>
                <b-form-checkbox id="receipt-sent" v-model="fields.receipt_sent_ind" name="receipt-sent" value="1"
                  unchecked-value="0">
                  Confirmation/Receipt Sent?
                </b-form-checkbox>
              </b-form-group>
            </b-col>
          </b-form-row>
        </b-form>
      </template>
      <!--  End of template for pesticide exams  -->

      <!--  Start of template for all non-pesticide exams -->
      <template v-else>
        <!-- All fields are to be shown.  Not sure what this means just now. -->
        <b-form v-if="showAllFields">
          <!--  For group exams, except Monthly Sessional (Challenger)  -->
          <b-form-row v-if="is_ita2_designate && examType === 'group'">
            <OfficeDrop :columnW="10" :office_number="office_number" :setOffice="setOffice" />
          </b-form-row>

          <!-- The Event ID and Exam Method labels row -->
          <b-form-row>
            <!-- The Event ID label and data colum -->
            <b-col cols="6">
              <b-form-group>
                <label class="my-0">Event ID</label>
                <b-form-input id="event_id" type="text" class="less-10-mb" v-model="fields.event_id" />
              </b-form-group>
            </b-col>

            <!-- The Exam method label and data colum -->
            <b-col cols="6">
              <b-form-group>
                <label class="my-0">Exam Method</label><br />
                <b-select id="exam_method" class="less-10-mb" v-model="fields.exam_method" :options="methodOptions" />
              </b-form-group>
            </b-col>
          </b-form-row>

          <!-- The Exam Type row -->
          <b-form-row>
            <b-col>
              <!-- If not a challenger exam, display the exam type -->
              <b-form-group v-if="!['challenger'].includes(examType)">
                <label class="my-0">Exam Type1</label><br />
                <div>
                  <b-input v-if="!isITAExam" :style="examInputStyle" :value="examInputText" class="less-15-mb"
                    placeholder="click here to see options" read-only :disabled="true" />
                  <model-list-select v-if="isITAExam" :list="iTAExamTypes" v-model="objectItem" option-value="exam_type_id"
                  option-text="exam_type_name"  id="type.exam_type_id" name="type.exam_type_id"
                  placeholder="click here to see options">
                </model-list-select>
                </div>
                <div :class="examTypeDropClass" style="border: 1px solid grey" @click="handleExamInputClick">
                  <template v-for="(type, i) in examTypeDropItems">
                    <b-dd-header v-if="type.header" :key="i + 'exam-type-dd-h'" :style="
                        type.exam_color !== '#FFFFF'
                          ? { backgroundColor: type.exam_color }
                          : null
                      ">
                      {{ type.exam_type_name }}
                    </b-dd-header>
                    <b-dd-item v-else :id="type.exam_type_id" :key="i + 'exam-type-dd'" :style="
                        type.exam_color !== '#FFFFF'
                          ? { backgroundColor: type.exam_color }
                          : null
                      " :value="type.exam_type_id" @click="handleExamDropClick">{{ type.exam_type_name }}
                    </b-dd-item>
                  </template>
                </div>
              </b-form-group>

              <!-- A Monthly Session (Challenger) exam  -->
              <b-form-group v-else>
                <label class="mb-0 mt-1">Exam Type</label>
                <b-form-input :value="exam.exam_type.exam_type_name" class="less-10-mb form-control" disabled
                  id="exam_name" type="text" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <!-- End of the Exam Type row -->

          <!-- The Exam Name label and data row -->
          <b-form-row>
            <b-col>
              <b-form-group>
                <label v-if="!lengthError" class="mb-0 mt-1">Exam Name</label>
                <label v-if="lengthError" style="color: red" class="mb-0 mt-1">Maximum field length reached.</label>
                <b-form-input id="exam_name" type="text" class="less-10-mb" @blur="removeError"
                  v-on:keydown="checkInputLength" v-model="fields.exam_name" />
              </b-form-group>
            </b-col>
          </b-form-row>

          <!-- The Exam Received and number of writers row -->
          <b-form-row v-if="!otherOfficeExam">
            <!--  The Exam received flag label and data column, if exam not received yet -->
            <b-col :col="!this.fields.exam_received_date" :cols="this.exam_received ? 3 : ''">
              <b-form-group>
                <label class="my-0">Exam Received?</label>
                <b-select id="exam_received" v-model="exam_received" @input="updateExamReceived" class="less-10-mb"
                  :options="examReceivedOptions" />
              </b-form-group>
            </b-col>

            <!--  The Exam received date and data column, if the exam has been received -->
            <b-col v-if="exam_received">
              <b-form-group>
                <label class="my-0">Received Date</label><br />
                <DatePicker :value="fields.exam_received_date" @input="handleDate" format="YYYY-MM-DD"
                  value-type="format" lang="en" id="exam_received_date" input-class="form-control"
                  class="w-100 my-0 less-10-mb">
                </DatePicker>
              </b-form-group>
            </b-col>

            <!-- If a group or Monthly Session (challenger) exam, display number of writers. -->
            <b-col v-if="examType === 'group' || examType === 'challenger'" col>
              <b-form-group>
                <label class="my-0"># of Writers</label><br />
                <b-input v-model="fields.number_of_students" id="number_of_students" />
              </b-form-group>
            </b-col>

            <!--  If an individual exam, display the expiry date  -->
            <b-col class="w-100" v-if="examType === 'individual'">
              <b-form-group>
                <label class="my-0">Expiry Date</label><br />
                <DatePicker v-model="fields.expiry_date" lang="en" id="exam_expiry" format="YYYY-MM-DD"
                  value-type="format" input-class="form-control" class="w-100 less-10-mb">
                  <template slot="calendar-icon">
                    <font-awesome-icon icon="clock" class="m-0 p-0" style="font-size: 0.9rem" />
                  </template>
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <!-- End of the Exam Received and number of writers row -->

          <!-- An individual or other exam  -->
          <b-form-row v-if="examType === 'individual' || examType === 'other'">
            <b-col>
              <b-form-group>
                <label class="my-0">Candidate's Name</label>
                <b-form-input id="examinee_name" class="less-10-mb" type="text" v-model="fields.examinee_name" />
              </b-form-group>
            </b-col>
          </b-form-row>

          <!-- The notes field. -->
          <b-form-row>
            <b-col>
              <b-form-group>
                <label class="my-0">Notes</label><br />
                <b-textarea id="notes" v-model="fields.notes" :maxlength="400" :rows="2" />
              </b-form-group>
            </b-col>
          </b-form-row>
        </b-form>
        <!-- End of the all fields are to be shown form.  Not sure what this means just now. -->

        <!-- All fields are not to be shown form.  Not sure what this means just now. -->
        <b-form v-if="!showAllFields">
          <b-form-row>
            <b-col class="mb-2">
              <div class="q-info-display-grid-container">
                <div class="q-id-grid-outer">
                  <div class="q-id-grid-head">Exam Details:</div>
                  <div class="q-id-grid-col">
                    <div>Exam:</div>
                    <div>{{ exam.exam_name }}</div>
                  </div>
                  <div class="q-id-grid-col">
                    <div>Event ID:</div>
                    <div>{{ exam.event_id }}</div>
                  </div>
                  <div class="q-id-grid-col">
                    <div>Type:</div>
                    <div v-if="isITAGroupOrSingleExam(exam)" :style="{
                        backgroundColor: exam.exam_type.exam_color,
                        height: 10 + 'px',
                        margin: '4px 0px 0px 0px',
                        width: 10 + 'px',
                      }"></div>
                    <div>{{ exam.exam_type.exam_type_name }}</div>
                  </div>
                  <div class="q-id-grid-col">
                    <div>Method:</div>
                    <div>{{ exam.exam_method }}</div>
                  </div>
                </div>
              </div>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-form-group>
                <label class="my-0">Exam Received?</label>
                <b-select id="exam_received" class="less-10-mb" @input="updateExamReceived"
                  :options="examReceivedOptions" v-model="exam_received" />
              </b-form-group>
            </b-col>

            <b-col v-if="exam_received" cols="6">
              <b-form-group>
                <label class="my-0">Date Received</label><br />
                <DatePicker v-model="fields.exam_received_date" id="exam_received_date" format="YYYY-MM-DD"
                  value-type="format" input-class="form-control" class="w-100 my-0 less-10-mb" type="date" lang="en" />
              </b-form-group>
            </b-col>
          </b-form-row>

          <b-form-row>
            <b-col>
              <b-form-group>
                <label class="my-0">Notes</label><br />
                <b-textarea id="notes" v-model="fields.notes" :maxlength="400" :rows="2" />
              </b-form-group>
            </b-col>
          </b-form-row>
        </b-form>
        <!-- End of the all fields are not to be shown form.  Not sure what this means just now. -->
      </template>
      <!--  End of template for all non-pesticide exams -->

      <!--  Placeholder for any message -->
      <div v-if="showMessage" class="mb-3" style="color: red">
        {{ this.message }}
      </div>

      <!--  Row of buttons, delete, edit, submit -->
      <div style="display: flex; justify-content: flex-end; width: 100%">
        <b-btn v-if="canDelete" class="btn-danger mr-2" @click="deleteExam()">Delete Exam
        </b-btn>
        <b-btn class="btn-secondary mr-2" @click="toggleEditExamModal(false)">Cancel
        </b-btn>
        <b-btn v-if="!allowSubmit" id="edit_submit_not_allow" class="btn-primary disabled" @click="setMessage">Submit
        </b-btn>
        <b-btn v-else-if="allowSubmit" id="edit_submit_allow" class="btn-primary" @click="submit">Submit
        </b-btn>
      </div>
    </div>
  </b-modal>
</template>

<script lang="ts">

import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'

import DatePicker from 'vue2-datepicker'

import DeleteExamModal from './delete-exam-modal.vue'
import FailureExamAlert from './failure-exam-alert.vue'
import OfficeDrop from './office-drop.vue'

import moment from 'moment'
import { ModelListSelect } from "vue-search-select"

const FileDownload = require('js-file-download')

@Component({
  components: {
    DatePicker,
    DeleteExamModal,
    FailureExamAlert,
    OfficeDrop,
    ModelListSelect
  }
})
export default class EditExamModal extends Vue {
  @Prop()
  private actionedExam!: any

  @Prop()
  private resetExam!: any

  @State('editExamFailure') private editExamFailure!: any
  @State('editExamSuccess') private editExamSuccess!: any
  @State('examTypes') private examTypes!: any
  @State('offices') private offices!: any
  @State('showEditExamModal') private showEditExamModal!: any
  @State('showDeleteExamModal') private showDeleteExamModal!: any
  @State('user') private user!: any

  @Getter('exam_object_id') private exam_object_id!: any;
  @Getter('role_code') private role_code!: any;
  @Getter('is_ita2_designate') private is_ita2_designate!: any;
  @Getter('is_office_manager') private is_office_manager!: any;
  @Getter('is_pesticide_designate') private is_pesticide_designate!: any;

  @Action('downloadExam') public downloadExam: any
  @Action('getBookings') public getBookings: any
  @Action('getExams') public getExams: any
  @Action('getOffices') public getOffices: any
  @Action('putExamInfo') public putExamInfo: any
  @Action('getExamTypes') public getExamTypes: any

  @Mutation('setEditExamFailure') public setEditExamFailure: any
  @Mutation('setEditExamSuccess') public setEditExamSuccess: any
  @Mutation('setSelectedExam') public setSelectedExam: any
  @Mutation('setReturnExamInfo') public setReturnExamInfo: any
  @Mutation('setReturnDeleteExamInfo') public setReturnDeleteExamInfo: any
  @Mutation('toggleEditExamModal') public toggleEditExamModal: any
  @Mutation('toggleDeleteExamModalVisible') public toggleDeleteExamModalVisible: any

  public examNotReady: boolean = false
  public feesOptions: any = 'collect'
  public clickedMenu: boolean = false
  public fields: any = {
    exam_received_date: null,
    notes: null,
    event_id: null,
    exam_name: null,
    receipt: null,
    receipt_sent_ind: null
  }

  public lengthError: boolean = false
  public message: any = ''
  public methodOptions: any = [
    { text: 'paper', value: 'paper' },
    { text: 'online', value: 'online' }
  ]

  public exam_received: any = null
  public office_number: any = null
  public officeChoices: any = []
  public showMessage: any = false
  public search: string = ''
  public searching: boolean = false
  public showSearch: boolean = false
  private objectItem:any  = {};

  get canDelete () {
    let examCanBeDeleted = false

    //  If an individual pesticide exam, can only delete if a pesticide liaison
    if (this.examType === 'pest' && this.is_pesticide_designate) {
      examCanBeDeleted = true
    }

    //  If not an individual pesticide exam, do the old, standard test.
    if (this.examType !== 'pest') {
      examCanBeDeleted = this.is_office_manager || this.role_code === 'GA' || this.is_ita2_designate
    }
    return examCanBeDeleted
  }

  get isITAExam() {
    const examType = this.examTypes.filter((examType) => examType.exam_type_id === this.actionedExam.exam_type_id);
    if (!examType) {
      return false;
    }
    return examType[0].ita_ind ===1 && examType[0].group_exam_ind === 0 && !examType[0].exam_type_name.includes('Monthly');
  }

  get iTAExamTypes() {
    this.objectItem = {
      exam_type_id: this.actionedExam.exam_type_id
    }
    const exams = this.examTypes.filter(type =>
        type.ita_ind === 1 &&
        type.group_exam_ind === 0 &&
        !type.exam_type_name.includes('Monthly'))
      return exams.sort((a, b) => a.exam_type_name - b.exam_type_name)
  }

  get fieldsEdited() {
    const fieldsEdited: any = []
    const data = Object.assign({}, this.fields)
    if (data.exam_received_date) {
      data.exam_received_date = moment(data.exam_received_date).utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
    }
    if (data.expiry_date) {
      data.expiry_date = moment(data.expiry_date).utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
    }
    for (const key in data) {
      if (data[key] != this.actionedExam[key]) {
        fieldsEdited.push(key)
      }
    }
    if (fieldsEdited.length === 1 && fieldsEdited.includes('notes')) {
      if (!data.notes && !this.actionedExam.notes) {
        return false
      }
    }
    return fieldsEdited
  }

  get allowSubmit () {
    if (this.actionedExam) {
      const fieldsEdited: any = []
      const data = Object.assign({}, this.fields)
      this.formatExamDates(data)
      for (const key in data) {
        if (data[key] != this.actionedExam[key]) {
          fieldsEdited.push(key)
        }
      }
      if (fieldsEdited.length === 1 && fieldsEdited.includes('notes')) {
        if (!data.notes && !this.actionedExam.notes) {
          return false
        }
      }
      return (fieldsEdited.length > 0)
    }
    return false
  }

  formatExamDates (data: any) {
    if (data.exam_received_date) {
      data.exam_received_date = moment(data.exam_received_date).utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
    }
    if (data.expiry_date) {
      data.expiry_date = moment(data.expiry_date).utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
    }
  }

  get otherOfficeExam () {
    if (!this.is_ita2_designate) {
      return false
    }
    if (this.actionedExam && this.actionedExam.office_id != this.user.office_id) {
      return true
    }
    return false
  }

  get exam () {
    if (Object.keys(this.actionedExam).length > 0) {
      this.feesOptions = (this.actionedExam.receipt) ? 'liaison' : 'collect'
      this.fields.receipt = this.actionedExam.receipt
      this.fields.receipt_sent_ind = this.actionedExam.receipt_sent_ind
      return this.actionedExam
    }
    return false
  }

  get examInputStyle () {
    if (this.examObject && this.examObject.exam_color !== '#FFFFFF') {
      const { exam_color } = this.examObject
      return { border: `1px solid ${exam_color}`, boxShadow: `inset 0px 0px 0px 3px ${exam_color}` }
    }
    return ''
  }

  get examInputText () {
    if (this.examObject) {
      return this.examObject.exam_type_name
    }
    return ''
  }

  get examObject () {
    if (this.fields && this.fields.exam_type_id) {
      return this.exam_object_id(this.fields.exam_type_id)
    }
    return ''
  }

  get examType () {
    if (this.exam && this.exam.exam_type) {
      const { exam_type } = this.exam

      if (exam_type.exam_type_name === 'Monthly Session Exam') {
        return 'challenger'
      }
      if (exam_type.pesticide_exam_ind) {
        return 'pest'
      }
      if (exam_type.group_exam_ind) {
        return 'group'
      }
      if (exam_type.ita_ind) {
        return 'individual'
      }
      return 'other'
    }
  }

  get examTypeDropClass () {
    if (!this.clickedMenu) {
      return 'dropdown-menu'
    }
    if (this.clickedMenu) {
      return 'dropdown-menu show py-0 my-0 w-100'
    }
  }

  get examTypeDropItems () {
    if (this.examType && this.examTypes) {
      const type = this.examType
      if (type === 'challenger' || type === 'pest') {
        return null
      }
      const types = this.examTypes.filter(t => t.exam_type_name !== 'Monthly Session Exam' && !t.pesticide_exam_ind)

      if (type === 'group') {
        return types.filter(t => t.group_exam_ind)
      }
      if (type === 'individual') {
        return types.filter(t => t.ita_ind && !t.group_exam_ind)
      }
      return types.filter(t => !t.ita_ind && !t.group_exam_ind)
    }
    return []
  }

  get examReceivedOptions () {
    this.exam_received = this.actionedExam.exam_received_date !== null
    this.fields.exam_received_date = this.actionedExam.exam_received_date
    return [
      { value: false, text: 'No' },
      { value: true, text: 'Yes' }
    ]
  }

  get showAllFields () {
    if (this.role_code === 'GA' || this.is_ita2_designate || this.is_office_manager) {
      return true
    }
    if (this.examType && ['individual', 'other'].includes(this.examType)) {
      return true
    }
    return false
  }

  get showModal () {
    return this.showEditExamModal
  }

  set showModal (e) {
    this.examNotReady = false
    this.toggleEditExamModal(e)
  }

  handleDate (date) {
    Vue.set(
      this.fields,
      'exam_received_date',
      date
    )
  }

  isITAGroupOrSingleExam (ex) {
    return !!ex.exam_type.ita_ind
  }

  checkAndDownloadExam () {
    this.downloadExam(this.exam)
      .then((resp) => {
        const filename = `${this.exam.exam_id}.pdf`
        FileDownload(resp.data, filename, 'application/pdf')
        this.updatePrintExamReceived('exam-downloaded')
      })
      .catch((error) => {
        console.log('===> edit-exam-form-modal====>error', error)
        console.error(error)
        this.examNotReady = true
        setTimeout(() => { this.examNotReady = false }, 15000)
      })
  }

  checkInputLength (e) {
    if (e.keyCode == 8 || e.keyCode == 46) {
      this.removeError()
      return true
    }
    if (this.fields.exam_name && this.fields.exam_name.length >= 50) {
      this.lengthError = true
      e.preventDefault()
      e.stopPropagation()
      return false
    }
  }

  deleteExam () {
    let deleteExamInfo = {}
    if (this.fields.booking_id) {
      deleteExamInfo = {
        booking_id: this.fields.booking_id,
        exam_id: this.fields.exam_id,
        exam_name: this.fields.exam_name,
        examinee_name: this.fields.examinee_name,
        event_id: this.fields.event_id
      }
    } else {
      deleteExamInfo = {
        booking_id: null,
        exam_id: this.fields.exam_id,
        exam_name: this.fields.exam_name,
        examinee_name: this.fields.examinee_name,
        event_id: this.fields.event_id
      }
    }
    this.toggleDeleteExamModalVisible(true)
    this.setReturnExamInfo(deleteExamInfo)
  }

  handleExamDropClick (e) {
    this.fields.exam_type_id = e.target.id
  }

  handleExamInputClick () {
    if (!this.clickedMenu) {
      this.clickedMenu = true
      return
    }
    this.clickedMenu = false
  }

  populateForm () {
    const exam = this.actionedExam
    Object.keys(exam).forEach(key => {
      if (typeof exam[key] === 'string' || typeof exam[key] === 'number') {
        Vue.set(
          this.fields,
          key,
          exam[key]
        )
      }
    })
    if (exam.expiry_date) {
      // JSTOTS INFO removed new from moment. no need to use new with moment
      this.fields.expiry_date = moment(exam.expiry_date).format('YYYY-MM-DD')
    }
    // JSTOTS TOCHECK  changed usage of isValid. existing code is commented
    // if (exam.exam_received_date && moment().isValid(exam.exam_received_date)) {
    if (exam.exam_received_date && moment(exam.exam_received_date).isValid()) {
      // JSTOTS INFO removed new from moment. no need to use new with moment
      this.fields.exam_received_date = moment(exam.exam_received_date).format('YYYY-MM-DD')
      this.exam_received = true
    }
    this.office_number = exam.office.office_number
  }

  setOffice (officeNumber) {
    this.office_number = officeNumber
    this.fields.office_id = this.offices.find(office => office.office_number == officeNumber).office_id
  }

  removeError () {
    this.lengthError = false
  }

  reset () {
    Object.keys(this.fields).forEach(key => {
      Vue.set(
        this.fields,
        key,
        null
      )
    })
    this.lengthError = false
    this.clickedMenu = false
    this.message = null
    this.office_number = null
    this.exam_received = false
    this.search = ''
    this.searching = false
    this.showMessage = false
    this.showSearch = false
    this.resetExam()
  }

  setMessage () {
    if (!this.allowSubmit) {
      if (!this.fields.office_id) {
        this.message = 'Please specify a valid office.'
      } else {
        this.message = 'Nothing has changed.  All fields contain their original values.'
      }
      this.showMessage = true
    }
  }

  submit () {
    const data = Object.assign({}, this.fields)
    const putRequest: any = {
      exam_id: this.fields.exam_id
    }
    if (data.exam_received_date) {
      data.exam_received_date = moment(data.exam_received_date).utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
    }
    if (data.expiry_date) {
      data.expiry_date = moment(data.expiry_date).utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
    }
    Object.keys(data).forEach(key => {
      if (data[key] != this.actionedExam[key]) {
        putRequest[key] = data[key]
      }
    })
    if (!this.exam_received) {
      putRequest.exam_received_date = null
    }
    this.putExamInfo(putRequest).then(() => {
      this.toggleEditExamModal(false)
    }).catch(() => {
      this.setEditExamFailure(10)
    })
  }

  updateExamReceived (e) {
    const { exam_received_date } = this.fields
    if (e.type == 'exam-downloaded') {
      this.exam_received = true
    }
    if (e && !exam_received_date) {
      // JSTOTS INFO removed new from moment. no need to use new with moment
      this.fields.exam_received_date = moment().format('YYYY-MM-DD')
      return
    }
    if (!e) {
      this.fields.exam_received_date = null
    }
  }

  updatePrintExamReceived (strExam) {
    const { exam_received_date } = this.fields
    if (strExam == 'exam-downloaded') {
      this.exam_received = true
    }
    if (strExam && !exam_received_date) {
      // JSTOTS INFO removed new from moment. no need to use new with moment
      this.fields.exam_received_date = moment().format('YYYY-MM-DD')
    }
  }

  mounted () {
    console.log("Exam", this.actionedExam);
    this.exam_received = this.actionedExam.exam_received_date !== null
    this.getExamTypes()
  }
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
  grid-column: 1 / span 2;
  margin-right: 20px;
}
</style>
