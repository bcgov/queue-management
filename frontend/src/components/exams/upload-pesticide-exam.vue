<template>
  <div data-app>
    <b-modal
      v-model="modalVisible"
      :no-close-on-backdrop="true"
      hide-header
      size="md"
      @hidden="resetModal"
    >
      <template slot="modal-footer">
        <div style="display: flex; justify-content: flex-end; width: 100%">
          <b-btn class="btn-secondary mr-2" @click="resetModal">{{
            submitted ? 'Done' : 'Cancel'
          }}</b-btn>
          <!-- This is the old button. Leaving it commented in case a rollback is needed. -->
          <!-- <b-btn class="btn-primary" v-if="!submitted" @click.once="submit"
            >Submit</b-btn
          > -->
          <b-btn class="btn-primary" v-if="!submitted" @click="examStatus"
            >Submit</b-btn
          >
        </div>
      </template>

      <b-form autocomplete="off">
        <b-form-row>
          <b-col class="q-modal-header">Upload Completed Exam</b-col>
        </b-form-row>
        <b-form-row v-if="submitted">
          <b-col class="text-center mt-2">
            <font-awesome-icon
              icon="check"
              class="m-0 p-0"
              style="font-size: 5rem; color: green"
            />
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
                  <div
                    style="color: green"
                    v-if="actionedExam.upload_received_ind"
                  >
                    Received
                  </div>
                  <div style="color: red" v-else>Not Received</div>
                </div>
              </div>
            </div>
          </b-col>
        </b-form-row>
        <template v-if="!submitted && !isLoading">
          <b-form-row v-if="actionedExam.upload_received_ind">
            <b-col :cols="12">
              <b-form-group class="mt-2 mb-0">
                <label class="mb-0">Upload Again?</label><br />
                <p>
                  This exam appears to be received, however you can submit it
                  again if needed.
                </p>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col :cols="6">
              <b-form-group class="mb-0">
                <label class="mb-0">Exam Status</label><br />
                <b-select
                  id="exam-status-select"
                  v-model="status"
                  :options="statusOptions"
                />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row class="mt-2" v-if="status === 'written'">
            <b-col>
              <b-form-group class="mb-0">
                <label class="mb-0">Attach Scanned Exam</label><br />
                <b-form-file
                  v-model="file"
                  placeholder="Choose a file or drop it here..."
                ></b-form-file>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group class="mb-0 mt-1" v-if="status === 'noshow'">
                <label class="mb-0">Exam Destroyed?</label><br />
                <b-select id="exam-returned-select" v-model="destroyed">
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </b-select>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-alert class="mt-2" :show="uploadFailed" variant="danger">
            File upload failed, please try again.
          </b-alert>
        </template>
        <div class="text-center" v-if="isLoading">
          <b-spinner variant="primary" label="Loading"></b-spinner>
        </div>
        <v-dialog
           v-model="confirmDialog"
           max-width="400"
           :retain-focus="false"
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
                 @click="confirmDialog = false"
               >
                 No
               </v-btn>
               <v-btn
                 color="red darken-1"
                 text
                 @click="confirmExam()"
               >
                 Yes
               </v-btn>
             </v-card-actions>
           </v-card>
         </v-dialog>
        <v-dialog
           v-model="noFileWarning"
           max-width="400"
           :retain-focus="false"
         >
           <v-card>
             <v-card-title class="headline">
              Warning
             </v-card-title>
             <v-card-text>
               {{ this.noFileText }}
             </v-card-text>
             <v-card-actions>
               <v-spacer></v-spacer>
               <v-btn
                 color="red darken-1"
                 text
                 @click="noFileWarning = false"
               >
                 OK
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
/* eslint-disable no-console */

import { Action, Mutation } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { mapState } from 'vuex'

@Component({

  computed: {
    ...mapState({
      showModal: (state: any) => state.addExamModule.uploadPesticideModalVisible
    })
  }
})
export default class UploadPesticideModal extends Vue {
  @Prop()
  private actionedExam!: any

  @Prop()
  private resetExam!: any

  private readonly showModal!: any

  @Action('putExamInfo') public putExamInfo: any
  @Action('getExams') public getExams: any
  @Action('getBCMPlusExamStatus') public getBCMPlusExamStatus: any
  @Action('submitExam') public submitExam: any

  @Mutation('toggleUploadExamModal') public toggleUploadExamModal: any
  @Mutation('setEditExamFailure') public setEditExamFailure: any

  public file: any = null
  public examNotes: any = this.actionedExam.notes
  public status: any = 'unwritten'
  public destroyed: any = this.actionedExam.exam_destroyed_date !== null
  public submitted: any = false
  public exam_printed: any = this.actionedExam.exam_received_date !== null
  public warningText: any = 'Are you sure you want to upload this exam?'
  public noFileText: any = 'Please provide a file to upload.'
  private confirmDialog: any = false
  private noFileWarning: any = false
  public statusOptions: any = this.exam_printed ? [
    { value: 'unwritten', text: 'Unwritten' },
    { value: 'written', text: 'Written' },
    { value: 'noshow', text: 'No Show' }
  ] : [
    { value: 'unwritten', text: 'Unwritten' },
    { value: 'noshow', text: 'No Show' }
  ]

  public uploadFailed: any = false
  public isLoading: any = false

  get exam () {
    if (this.actionedExam) {
      console.log('this.actionedExam ', this.actionedExam)
      return this.actionedExam
    }
    return {}
  }

  get modalVisible () {
    console.log('showModal', this.showModal)
    return this.showModal
  }

  set modalVisible (e) {
    this.toggleUploadExamModal(e)
  }

  resetModal () {
    this.resetExam()
    this.toggleUploadExamModal(false)
  }

  examStatus () {
    if (this.status === 'written' && this.file === null) {
      this.noFileWarning = true
    } else if (this.status === 'written' && this.file) {
      this.confirmDialog = true
    } else {
      this.submit()
    }
  }

  private async confirmExam () {
    this.confirmDialog = false
    this.submit()
  }

  submit () {
    this.uploadFailed = false
    this.isLoading = true
    const putData: any = {
      exam_id: this.exam.exam_id,
      notes: this.examNotes,
      exam_written_ind: (this.status === 'written') ? 1 : 0,
      exam_destroyed_date: (this.destroyed) ? new Date().toISOString() : null
    }

    console.log(this.exam)
    console.log(this.status)

    if (this.status === 'written' && this.file) {
      this.submitExam({ file: this.file, exam: this.exam })
        .then((bcmpResponse) => {
          this.submitted = true
          console.log(bcmpResponse)
          putData.upload_received_ind = this.actionedExam.upload_received_ind = 1
          putData.exam_returned_date = this.actionedExam.exam_returned_date = new Date().toISOString()
          console.log(this.actionedExam)
          this.updateExam(putData)
          this.isLoading = false
        })
        .catch((error) => {
          this.uploadFailed = true
          this.isLoading = false
          console.error(error)
        })
    } else {
      console.log('=====> Submit Exam ===> this.status', this.status)
      console.log('=====> Submit Exam ===> this.upload received_ind', this.actionedExam.upload_received_ind)
      console.log('=====> Submit Exam ===> this returned date', this.actionedExam.exam_returned_date)
      this.submitted = true
      putData.upload_received_ind = this.actionedExam.upload_received_ind = 0
      putData.exam_returned_date = this.actionedExam.exam_returned_date = new Date().toISOString()
      console.log(this.actionedExam)
      this.updateExam(putData)
      this.isLoading = false
    }
  }

  updateExam (putData) {
    this.putExamInfo(putData)
      .then(() => {
      })
      .catch((error) => {
        console.error(error)
      })
  }

  mounted () {
    this.uploadFailed = false
    if (this.actionedExam.exam_destroyed_date !== null) {
      this.status = 'noshow'
    } else if (this.actionedExam.upload_received_ind && this.actionedExam.exam_written_ind) {
      this.status = 'written'
    } else {
      this.status = 'unwritten'
    }
  }
}
</script>
