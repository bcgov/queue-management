<template>
<div data-app>
  <b-modal
    v-model="modal"
    :no-close-on-backdrop="true"
    hide-header
    :size="returned ? 'md' : 'sm'"
    id="return_exam_modal"
    @shown="show"
    @hidden="resetModal()"
  >
    <template slot="modal-footer">
      <div style="display: flex; justify-content: flex-end; width: 100%">
        <b-btn
          v-if="okButton.title !== 'Cancel'"
          class="btn-secondary mr-2"
          @click="resetModal()"
          >Cancel</b-btn
        >
        <b-btn
          v-if="okButton.disabled"
          class="btn-primary disabled"
          @click="showFieldErrors = false"
          >Submit</b-btn
        >
        <!-- This is the old button. Leaving it commented in case a rollback is needed. -->
        <!-- <b-btn
          v-if="!okButton.disabled"
          :class="okButton.title === 'Cancel' ? 'btn-secondary' : 'btn-primary'"
          @click.prevent="submit"
          >{{ okButton.title }}</b-btn
        > -->
        <b-btn
          v-if="!okButton.disabled"
          :class="okButton.title === 'Cancel' ? 'btn-secondary' : 'btn-primary'"
          @click.prevent="examStatus"
          >{{ okButton.title }}</b-btn
        >
      </div>
    </template>
    <FailureExamAlert />
    <b-form autocomplete="off">
      <b-form-row>
        <b-col class="q-modal-header">
          {{
            modalUse === 'return' ? 'Return Exam' : 'Edit Return Details'
          }}</b-col
        >
      </b-form-row>
      <b-form-row>
        <b-col :cols="returned ? 3 : 12">
          <b-form-group class="mb-0">
            <label class="mb-0">Exam Status</label><br />
            <b-select
              id="exam-returned-select"
              v-model="returned"
              @input="handleReturnedStatus"
              :options="returnOptions"
            />
          </b-form-group>
        </b-col>
        <template v-if="returned">
          <b-col cols="3">
            <b-form-group class="mb-0">
              <label class="mb-0">Written?</label><br />
              <b-form-select
                id="exam-written-select"
                v-model="exam_written_ind"
                @input="handleReturnedStatus"
                :options="writtenOptions"
              />
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group class="mb-0">
              <label class="mb-0">Date of Return</label><br />
              <DatePicker
                v-model="exam_returned_date"
                class="w-100"
                input-class="form-control"
                lang="en"
              />
            </b-form-group>
          </b-col>
        </template>
      </b-form-row>
      <template v-if="returned">
        <b-form-row>
          <b-col>
            <b-form-group class="mb-0 mt-2">
              <label v-if="!errorText" class="mb-0"
                >Action Taken
                <span
                  v-if="
                    typeof showFieldErrors === 'boolean' && !showFieldErrors
                  "
                  style="color: red"
                  >Required Field</span
                >
              </label>
              <label v-if="errorText" style="color: red" class="mb-0"
                >Maximum field length reached. Use Notes field if needed.</label
              >
              <br />
              <b-form-input
                v-model="exam_returned_tracking_number"
                id="action_taken"
                :state="showFieldErrors"
                placeholder="Include tracking info or disposition"
                ref="returnactiontaken"
                @input="showFieldErrors = null"
                v-on:keydown="handleActionInput"
                @blur="removeError()"
              />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Notes</label><br />
              <b-input v-model="notes" id="notes" :rows="2" />
            </b-form-group>
          </b-col>
        </b-form-row>
      </template>
    <v-dialog
      v-model="confirmDialog"
      max-width="400"
    >
      <v-card>
        <v-card-title class="headline">
         Confirm
        </v-card-title>
        <v-card-text>
          {{ this.warningText }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red darken-1"
            text
            @click="confirmExam(false)"
          >
            No
          </v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="confirmExam(true)"
          >
            Yes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </b-form>
  </b-modal>
</div>
</template>

<script lang="ts">
/* eslint-disable camelcase */
import { Action, Mutation, State } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'
import DatePicker from 'vue2-datepicker'
import FailureExamAlert from './failure-exam-alert.vue'
import moment from 'moment'

@Component({
  components: {
    FailureExamAlert,
    DatePicker
  }
})
export default class ReturnExamModal extends Vue {
  @Prop()
  private actionedExam!: any

  @Prop()
  private resetExam!: any

  @State('showReturnExamModal') private showModal!: any
  @State('editExamSuccess') private editExamSuccess!: any
  @State('editExamFailure') private editExamFailure!: any

  @Action('putExamInfo') public putExamInfo: any
  @Action('getExams') public getExams: any

  @Mutation('toggleReturnExamModal') public toggleReturnExamModal: any
  @Mutation('setEditExamFailure') public setEditExamFailure: any

  public exam: any = null
  public returned: any = false
  public exam_written_ind: any = true
  public exam_returned_date: any = null
  public errorText: any = false
  public notes: any = null
  public showFieldErrors: any = null
  public exam_returned_tracking_number: any = ''
  public warningText: any = 'Are you sure you want to return this exam?'
  private confirmDialog: any = false
  public returnOptions: any = [
    { value: false, text: 'Not Returned' },
    { value: true, text: 'Returned' }
  ]

  public writtenOptions: any = [
    { value: 1, text: 'Yes' },
    { value: 0, text: 'No' }
  ]

  public modalUse: any = 'return'

  get changesMadeInEditMode () {
    if (this.exam && this.exam.exam_id) {
      const fields = ['exam_returned_tracking_number', 'exam_written_ind', 'notes', 'exam_returned_date']
      let result = false
      fields.forEach(field => {
        // eslint-disable-next-line eqeqeq
        if (this[field] != this.exam[field]) {
          result = true
        }
      })
      return result
    }
    return false
  }

  get okButton () {
    if (!this.returned && this.modalUse === 'edit') {
      return { title: 'Submit', disabled: false }
    }
    if (this.returned && this.modalUse === 'edit') {
      if (this.changesMadeInEditMode) {
        return { title: 'Submit', disabled: false }
      }
      return { title: 'Submit', disabled: true }
    }
    if (this.returned && this.modalUse === 'return') {
      if (this.exam_returned_date && this.exam_returned_tracking_number) {
        return { title: 'Submit', disabled: false }
      }
      return { title: 'Submit', disabled: true }
    }
    return { title: 'Cancel', disabled: false }
  }

  get modal () {
    return this.showModal
  }

  set modal (e) {
    this.toggleReturnExamModal(e)
  }

  handleActionInput (e) {
    // eslint-disable-next-line eqeqeq
    if (e.keyCode == 8 || e.keyCode == 46) {
      this.removeError()
      return true
    }
    if (this.exam_returned_tracking_number && this.exam_returned_tracking_number.length >= 250) {
      this.errorText = true
      e.preventDefault()
      e.stopPropagation()
      return false
    }
  }

  handleReturnedStatus (value) {
    if (value) {
      if (!this.exam_returned_date) {
        this.exam_returned_date = moment()
      }
      if (this.modalUse === 'return') {
        this.$nextTick(() => {
          (this.$refs.returnactiontaken as any).focus()
        })
      }
    }
  }

  examStatus () {
    if (this.okButton.title === 'Cancel') {
      this.resetModal()
      return
    }
    if (this.modalUse === 'edit') {
      this.submit()
    } else if (this.returned) {
      this.confirmDialog = true
    }
  }

  private async confirmExam (isAgree: boolean) {
    if (isAgree) {
      this.submit()
    }
    this.confirmDialog = false
  }

  show () {
    this.exam = this.actionedExam
    const tempValues = Object.assign({}, this.actionedExam)
    this.notes = tempValues.notes
    this.exam_returned_tracking_number = tempValues.exam_returned_tracking_number
    if (tempValues.exam_returned_date) {
      this.modalUse = 'edit'
      this.returned = true
      this.exam_returned_date = moment(tempValues.exam_returned_date).format('ddd MMM DD YYYY HH:mm:ss [GMT]ZZ')
      this.exam_written_ind = tempValues.exam_written_ind
      return
    }
    this.modalUse = 'return'
    this.exam_written_ind = 1
  }

  resetModal () {
    this.toggleReturnExamModal(false)
    this.showFieldErrors = null
    this.exam = null
    this.errorText = false
    this.returned = false
    this.exam_returned_date = null
    this.exam_returned_tracking_number = ''
    this.notes = null
    this.resetExam()
  }

  removeError () {
    this.errorText = false
  }

  submit () {
    if (this.okButton.title === 'Cancel') {
      this.resetModal()
      return
    }
    let putData: any = {
      exam_id: this.exam.exam_id,
      exam_returned_date: moment(this.exam_returned_date).format('YYYY-MM-DD'),
      exam_returned_tracking_number: this.exam_returned_tracking_number,
      notes: this.notes,
      exam_written_ind: this.exam_written_ind
    }
    if (!this.returned && this.modalUse === 'edit') {
      putData = {
        exam_id: this.exam.exam_id,
        exam_returned_date: null,
        exam_returned_tracking_number: null,
        notes: ''
      }
    }
    if (this.notes) {
      putData.notes = this.notes
    }
    this.putExamInfo(putData).then(() => {
      this.getExams().then(() => {
        this.resetModal()
      })
    }).catch(() => {
      // JSTOTS This property not existing. now just commenting out. check
      // this.setExamEditFailureMessage(10)
    })
  }
}
</script>
