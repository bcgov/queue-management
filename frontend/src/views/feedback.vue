<template>
  <b-modal
    size="md"
    :centered="t"
    :hide-footer="t"
    :hide-header="t"
    :ok-disabled="t"
    :cancel-disabled="t"
    :visible="showFeedbackModal"
    @hidden="toggleModal"
  >
    <div style="padding: 1rem">
      <h4>Submit Feedback</h4>
      Please use this form to submit any questions you have, or to report any
      issues that you are experiencing. Please try to include details such as
      the part of the app you were viewing and what you were doing at the time.
      <p style="margin-top: 9px">
        Please also use this form to submit feedback including any comments,
        suggestions, or feature requests.
      </p>
      <p class="feedback-warning" v-if="showWarning">
        You must provide a message
      </p>
      <b-textarea
        :rows="5"
        v-model="writeFeedback"
        class="mb-2 mt-1"
        placeholder="Please explain..."
        style="font-size: 0.9rem;"
      >
      </b-textarea>
      <div id="feedback-modal-buttons">
        <b-btn class="mr-1 btn-primary" @click="submitMessage"> Submit </b-btn>
        <b-btn @click="toggleModal"> Cancel </b-btn>
      </div>
    </div>
  </b-modal>
</template>

<script lang="ts">
import { Action, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Feedback extends Vue {
  @State('showFeedbackModal') private showFeedbackModal!: any
  @State('feedbackMessage') private feedbackMessage!: any

  @Action('messageFeedback') public messageFeedback: any

  @Mutation('toggleFeedbackModal') public toggleFeedbackModal: any
  @Mutation('setFeedbackMessage') public setFeedbackMessage: any
  @Mutation('showHideResponseModal') public showHideResponseModal: any
  // @Mutation('toggleFeedbackModal') public toggleFeedbackModal: any

  public t: boolean = true
  public f: boolean = false
  public showWarning: boolean = false

  get writeFeedback () { return this.feedbackMessage }
  set writeFeedback (value) { this.setFeedbackMessage(value) }

  toggleModal () {
    this.toggleFeedbackModal(false)
    this.showWarning = false
    this.setFeedbackMessage('')
  }

  submitMessage () {
    if (this.feedbackMessage.length <= 0) {
      this.showWarning = true
    } else {
      this.messageFeedback()
      this.showWarning = false
      this.toggleFeedbackModal(false)
      this.showHideResponseModal()
    }
  }
}
</script>

<style scoped>
.feedback-warning {
  font-size: 0.9rem;
  color: red;
  margin-top: 0px;
  margin-bottom: 0px;
}
#feedback-modal-buttons {
  display: flex;
  width: 100%;
  justify-content: flex-end;
}
</style>
