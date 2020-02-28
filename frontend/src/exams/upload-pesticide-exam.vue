<template>
  <b-modal v-model="modal"
           @shown="showModal"
           :no-close-on-backdrop="true"
           hide-header
           size="md"
           @hidden="resetModal()">
    <template slot="modal-footer">
      <div style="display: flex; justify-content: flex-end; width: 100%">
        <b-btn class="btn-secondary mr-2"
               @click="resetModal()">{{ submitted ? 'Done' : 'Cancel' }}</b-btn>
        <b-btn class="btn-primary"
               v-if="!submitted"
               @click.prevent="submitted = true"
               @click="submit()">Submit</b-btn>
      </div>
    </template>

    <b-form autocomplete="off">
      <b-form-row>
        <b-col class="q-modal-header">Upload Completed Exam</b-col>
      </b-form-row>
      <b-form-row>
        <b-col v-if="submitted" class="text-center mt-2">
          <font-awesome-icon icon="check"
                             class="m-0 p-0"
                             style="font-size: 5rem; color: green" />
          <h4>Success!</h4>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col class="mb-2">
          <div class="q-info-display-grid-container">
            <div class="q-id-grid-outer">
              <div class="q-id-grid-head">Exam Details</div>
              <div class="q-id-grid-col px-2">
                <div>Exam:</div>
                <div>{{ this.exam.examinee_name }}</div>
              </div>
              <div class="q-id-grid-col px-2">
                <div>Upload Status:</div>
                <div style="color: red">Not Received</div>
              </div>
            </div>
          </div>
        </b-col>
      </b-form-row>
      <template v-if="!submitted">
        <b-form-row>
          <b-col :cols="6">
            <b-form-group class="mb-0">
              <label class="mb-0">Exam Status</label><br>
              <b-select id="exam-returned-select"
                        v-model="status"
                        :options="statusOptions" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row class="mt-2" v-if="status === 'written'">
          <b-col>
            <b-form-group class="mb-0">
              <label class="mb-0">Attach Scanned Exam</label><br>
              <b-form-file
                v-model="file"
                :state="file"
                placeholder="Choose a file or drop it here..."
                no-drop
              ></b-form-file>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group class="mb-0 mt-1" v-if="status === 'noshow'">
              <label class="mb-0">Exam Destroyed?</label><br>
              <b-select id="exam-returned-select"
                        v-model="destroyed">
                <option value="true">Yes</option>
                <option value="false">No</option>
              </b-select>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row class="mt-2">
          <b-col>
            <b-form-group class="mb-0">
              <label class="mb-0">Notes</label><br>
              <b-textarea v-model="examNotes"/>
            </b-form-group>
          </b-col>
        </b-form-row>
      </template>
    </b-form>

  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState } from 'vuex'

  export default {
    name: "UploadPesticideModal",
    props: ['actionedExam', 'resetExam'],
    data() {
      return {
        file: null,
        examNotes: this.actionedExam.notes,
        status: this.actionedExam.exam_destroyed_date !== null ? 'noshow' : 'unwritten',
        destroyed: this.actionedExam.exam_destroyed_date !== null ? true : false,
        submitted: false,
        statusOptions: [
          { value: 'unwritten', text: 'Unwritten' },
          { value: 'written', text: 'Written' },
          { value: 'noshow', text: 'No Show' }
        ],
      }
    },
    computed: {
      ...mapState({
        showModal: state => state.addExamModule.uploadPesticideModalVisible,
      }),
      examNotes: {
        get() { return this.feedbackMessage },
        set(value) { this.examNotes = value }
      },
      exam() {
        if (this.actionedExam) {
          return this.actionedExam
        }
        return {}
      },
      modal: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleUploadExamModal(e)
        },
      },
    },
    methods: {
      ...mapActions(['putExamInfo', 'getExams', 'getBCMPlusExamStatus', 'submitExam', 'toggleUploadExamModal' ]),
      ...mapMutations(['toggleUploadExamModal', 'setEditExamFailure' ]),
      resetModal() {
        this.resetExam()
        this.toggleUploadExamModal(false)
      },
      submit() {
        let putData = {
          exam_id: this.exam.exam_id,
          exam_returned_tracking_number: this.exam_returned_tracking_number,
          notes: this.examNotes,
          exam_written_ind: 0,
          exam_destroyed_date: null
        }

        if (this.statusOptions === 'written') {
          putData.exam_written_ind = 1
        }
        if (this.destroyed) {
          putData.exam_destroyed_date = new Date().toISOString()
        }

        if (!this.written && this.modalUse === 'edit') {
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
          console.log(this.exam)
          this.submitExam({file: this.file, exam: this.exam})
            .then(() => {
              this.getExams()
                .then( () => {
                  this.resetModal()
                })
                .catch((error) => {
                  console.error(error)
                })
            })
            .catch( (error) => {
              console.error(error)
            })
        })
      }
    },
  }
</script>
