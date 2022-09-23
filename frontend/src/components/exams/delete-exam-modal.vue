<template>
  <b-modal
    v-model="deleteModalVisible"
    :no-close-on-backdrop="true"
    hide-header
    hide-footer
    hide-cancel
    size="md"
  >
    <b-container>
      <h5>Are you sure you want to delete this Exam?</h5>
      <div style="font-size: 0.9rem; display: flex; justify-content: center">
        <b-col>
          <ul>
            <strong>Exam Name: {{ this.returnExam.exam_name }}</strong>
          </ul>
          <ul>
            <strong>Examinee Name:</strong>
            {{
              this.returnExam.examinee_name
            }}
          </ul>
          <ul>
            <strong>Event ID:</strong>
            {{
              this.returnExam.event_id
            }}
          </ul>
        </b-col>
      </div>
      <b-row>
        <b-col>
          <b-form-group>
            <b-btn class="w-100 btn-danger" @click="clickNo">No</b-btn>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group>
            <b-btn class="w-100 btn-primary" @click="clickYes">Yes</b-btn>
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>
  </b-modal>
</template>

<script lang="ts">
import { Action, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class DeleteExamModal extends Vue {
  [x: string]: any
  @State('showDeleteExamModal') private showDeleteExamModal!: any
  @State('returnExam') private returnExam!: any

  @Action('deleteBooking') public deleteBooking: any
  @Action('deleteExam') public deleteExam: any
  @Action('getExams') public getExams: any

  @Mutation('toggleDeleteExamModalVisible') public toggleDeleteExamModalVisible: any
  @Mutation('toggleEditExamModal') public toggleEditExamModal: any

  get deleteModalVisible () {
    return this.showDeleteExamModal
  }

  set deleteModalVisible (e) {
    this.toggleDeleteExamModalVisible(e)
  }

  get exam () {
    if (Object.keys(this.actionedExam).length > 0) {
      return this.actionedExam
    }
    return false
  }

  clickYes () {
    const exam_id = this.returnExam.exam_id
    this.deleteExam(exam_id)
      .then(() => { this.getExams() })
    this.toggleDeleteExamModalVisible(false)
    this.toggleEditExamModal(false)
    if (this.returnExam.booking_id) {
      this.deleteBooking(this.returnExam.booking_id)
    }
  }

  clickNo () {
    this.toggleDeleteExamModalVisible(false)
  }
}
</script>
