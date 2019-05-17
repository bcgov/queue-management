<template>
  <b-modal v-model="modal"
           :no-close-on-backdrop="true"
           :ok-only="okButton.title === 'Cancel'"
           :ok-title="okButton.title"
           :ok-variant="okButton.title === 'Cancel' ? 'secondary' : 'primary'"
           :ok-disabled="okButton.disabled"
           hide-header
           :size="returned ? 'md' : 'sm' "
           id="return_exam_modal"
           @shown="show"
           @hidden="resetModal()"
           @cancel="resetModal()"
           @ok.prevent="submit">
    <FailureExamAlert />
    <b-form autocomplete="off">
      <b-form-row>
        <b-col class="q-modal-header">
          {{ modalUse === 'return' ? 'Return Exam' : 'Edit Return Details' }}</b-col>
      </b-form-row>
      <b-form-row>
        <b-col :cols="returned ? 3 : 12">
          <b-form-group class="mb-0">
            <label class="mb-0">Exam Status</label><br>
            <b-select id="exam-returned-select"
                      v-model="returned"
                      @input="handleReturnedStatus"
                      :options="returnOptions" />
          </b-form-group>
        </b-col>
        <template v-if="returned">
          <b-col cols="3" >
            <b-form-group class="mb-0">
              <label class="mb-0">Written?</label><br>
              <b-form-select id="exam-written-select"
                             v-model="exam_written_ind"
                             @input="handleReturnedStatus"
                             :options="writtenOptions" />
            </b-form-group>
          </b-col>
          <b-col>
          <b-form-group class="mb-0">
            <label class="mb-0">Date of Return</label><br>
            <DatePicker v-model="exam_returned_date"
                        class="w-100"
                        input-class="form-control"
                        lang="en" />
          </b-form-group>
          </b-col>
        </template>
      </b-form-row>
      <template v-if="returned">
        <b-form-row>
          <b-col>
            <b-form-group class="mb-0 mt-2">
              <label v-if="!errorText"
                     class="mb-0">Action Taken</label>
              <label v-if="errorText"
                     style="color: red"
                     class="mb-0">Maximum field length reached.  Use Notes field if needed.</label>
              <br>
              <b-form-input v-model="exam_returned_tracking_number"
                            id="action_taken"
                            placeholder="Include tracking info or disposition"
                            ref="returnactiontaken"
                            v-on:keydown="handleActionInput"
                            @blur="removeError()"
                            />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Notes</label><br>
              <b-input v-model="notes"
                          id="notes"
                          :rows="2"/>
            </b-form-group>
          </b-col>
        </b-form-row>
      </template>
    </b-form>
  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState } from 'vuex'
  import DatePicker from 'vue2-datepicker'
  import moment from 'moment'
  import FailureExamAlert from './failure-exam-alert'

  export default {
    name: "ReturnExamModal",
    props: ['actionedExam', 'resetExam'],
    components: { FailureExamAlert, DatePicker },
    data() {
      return {
        exam: null,
        returned: false,
        exam_written_ind: true,
        exam_returned_date: null,
        errorText: false,
        notes: null,
        exam_returned_tracking_number: '',
        returnOptions: [
          { value: false, text: 'Not Returned' },
          { value: true, text: 'Returned' },
        ],
        writtenOptions: [
          { value: 1, text: 'Yes' },
          { value: 0, text: 'No' },
        ],
        modalUse: 'return'
      }
    },
    computed: {
      ...mapState({
        showModal: 'showReturnExamModal',
        editExamSuccess: 'editExamSuccess',
        editExamFailure: 'editExamFailure',
      }),
      changesMadeInEditMode() {
        if (this.exam && this.exam.exam_id) {
          let fields = [ 'exam_returned_tracking_number', 'exam_written_ind', 'notes', 'exam_returned_date' ]
          let result = false
          fields.forEach(field => {
            if (this[field] != this.exam[field]) {
              result = true
            }
          })
          return result
        }
        return false
      },
      okButton() {
        if (!this.returned && this.modalUse === 'edit') {
          return {title: 'Submit', disabled: false}
        }
        if (this.returned && this.modalUse === 'edit') {
          if (this.changesMadeInEditMode) {
            return {title: 'Submit', disabled: false}
          }
          return {title: 'Submit', disabled: true}
        }
        if (this.returned && this.modalUse === 'return') {
          if (this.exam_returned_date && this.exam_returned_tracking_number) {
            return {title: 'Submit', disabled: false}
          }
          return {title: 'Submit', disabled: true}
        }
        return {title: 'Cancel', disabled: false}
      },
      modal: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleReturnExamModal(e)
        },
      },
    },
    methods: {
      ...mapActions(['putExamInfo', 'getExams', ]),
      ...mapMutations(['toggleReturnExamModal', 'setEditExamFailure',  ]),
      handleActionInput(e) {
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
      },
      handleReturnedStatus(value) {
        if (value) {
          if (!this.exam_returned_date) {
            this.exam_returned_date = moment()
          }
          if (this.modalUse === 'return') {
            this.$nextTick( () => {
              this.$refs.returnactiontaken.focus()
            })
          }
        }
      },
      show() {
        this.exam = this.actionedExam
        let tempValues = Object.assign({}, this.actionedExam)
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
      },
      resetModal() {
        this.toggleReturnExamModal(false)
        this.exam = null
        this.errorText = false
        this.returned = false
        this.exam_returned_date = null
        this.exam_returned_tracking_number = ''
        this.notes  = null
        this.resetExam()
      },
      removeError() {
        this.errorText = false
      },
      submit() {
        if (this.okButton.title === 'Cancel') {
          this.resetModal()
          return
        }
        let putData = {
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
        this.putExamInfo(putData).then( () => {
          this.getExams().then( () => {
            this.resetModal()
          })
        }).catch( () => {
          this.setExamEditFailureMessage(10)
        })
      }
    },
  }
</script>
