<template>
  <b-modal size="md"
           :centered="t"
           :hide-footer="t"
           :hide-header="t"
           :ok-disabled="t"
           :cancel-disabled="t"
           :visible="showFeedbackModal"
           @hidden="toggleModal"
           >
    <h5>Submit Feedback</h5>
    Please describe the issue you are experiencing, including the actions that cause it or what you were doing when
    it occurred, where in the app/what screen you were viewing, a description of the issue and how it differs from the
    expected behaviour.  Please don't include any private or personal information in your explanation.
    <p class="feedback-warning" v-if="showWarning">Please take a moment to explain in a bit more detail</p>
    <b-textarea :rows="5"
                v-model="writeFeedback"
                class="mb-2 mt-1"
                placeholder="Please explain what's happening"
                style="font-size: .9rem"
                >
    </b-textarea>
    <div id="feedback-modal-buttons">
      <b-btn class="mr-1 btn-primary" @click="submitMessage">
        Submit
      </b-btn>
      <b-btn @click="toggleModal">
        Cancel
      </b-btn>

    </div>

  </b-modal>
</template>

<script>
  import { mapState, mapMutations, mapActions } from 'vuex'

  export default {
    name: 'Feedback',

    data() {
      return {
        t: true,
        f: false,
        showWarning: false
      }
    },

    computed: {
      ...mapState(['showFeedbackModal', 'feedbackMessage']),

      writeFeedback: {
        get() { return this.feedbackMessage },
        set(value) { this.setFeedbackMessage(value) }
      }
    },

    methods: {
      ...mapMutations([
        'toggleFeedbackModal',
        'setFeedbackMessage',
        'showHideResponseModal',
        'toggleFeedbackModal'
      ]),
      ...mapActions(['messageSlack']),

      toggleModal() {
        this.toggleFeedbackModal(false)
        this.showWarning = false
        this.setFeedbackMessage('')
      },

      submitMessage() {
        if (this.feedbackMessage.length < 25) {
          this.showWarning = true
        } else {
          this.messageSlack()
          this.showWarning = false
          this.toggleFeedbackModal(false)
          this.showHideResponseModal()
        }
      }
    }
  }
</script>

<style scoped>
  .feedback-warning {
    font-size: .9rem; color: red; margin-top: 0px; margin-bottom: 0px;
  }
#feedback-modal-buttons {
  display: flex;
  width: 100%;
  justify-content: flex-end;
}
</style>
