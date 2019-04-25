<template>
  <div class="scheduling-indicator"
       v-if="show_scheduling_indicator">
    <div style="display: flex; justify-content: flex-start; border-radius: 24">
      <div class="m-2 flex-min" style="font-weight:600; font-size:1.2rem">Now Scheduling | </div>
      <div style="font-size: 1.1rem;" class="flex-min ml-1 mr-2 mt-2">
        {{ examAssociated ? 'Exam Event | ' : 'Non-Exam Event' }}
      </div>
      <div class="mr-1 mt-2 flex-min" v-if="examAssociated" style="font-size: 1.1rem">
        <span>{{ `Duration: ${selectedExam.exam_type.number_of_hours} HRS | ` }}</span><br>
      </div>
      <div class="m-2 flex-min" v-if="examAssociated">
        <span><b>Exam: </b> {{ selectedExam.exam_name }}</span><br>
        <span><b>Expiry Date: </b>{{ expiryDateFormat }}</span><br>
      </div>
      <div v-if="!examAssociated" class="flex-min mx-3 mt-1">
        <span class="smaller-font">Select date and time</span><br>
        <span class="smaller-font">on the calendar</span><br>
      </div>
      <div class="flex-fill " />
      <div class="flex-min">
        <b-button @click="cancel"
                  class="btn-danger mx-3 mt-1">Cancel</b-button>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import moment from 'moment'

  export default {
    name: "SchedulingIndicator",
    computed: {
      ...mapGetters(['show_scheduling_indicator']),
      ...mapState([
        'editedBooking',
        'rescheduling',
        'scheduling',
        'selectedExam',
        'showEditBookingModal',
        'showBookingModal',
        'showOtherBookingModal'
      ]),
      examAssociated() {
        if (this.selectedExam && Object.keys(this.selectedExam).length > 0) {
          return true
        }
        return false
      },
      bookingModalsHidden() {
        if (!this.showOtherBookingModal && !this.showBookingModal && !this.showEditBookingModal) {
          return true
        }
        return false
      },
      expiryDateFormat() {
        if (this.examAssociated && this.selectedExam.expiry_date) {
          let d = moment(this.selectedExam.expiry_date)
          if (d.isValid()) {
            return d.format('MMM-DD-YYYY')
          }
        }
        return 'not applicable'
      }
    },
    methods: {
      ...mapActions(['finishBooking', ]),
      ...mapMutations(['toggleEditBookingModal']),
      cancel() {
        if (this.rescheduling) {
          this.toggleEditBookingModal(true)
          return
        }
        let pushToExams = false
        if (this.selectedExam && this.selectedExam.referrer === 'scheduling') {
          pushToExams = true
        }
        this.finishBooking()
        if (pushToExams) {
          this.$router.push('/exams')
        }
      }
    }
  }
</script>

<style scoped>
  .flex-min {
    flex-basis: min-content;
  }
  .flex-fill {
    flex-basis: fill;
  }
  .scheduling-indicator {
    border: 1px solid darkgoldenrod;
    background-color: #f5dc31;
    width: 100%;
    bottom: 36px;
    height: 50px;
    position: fixed;
    z-index: 1039;
  }
</style>
