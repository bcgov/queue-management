<template>
  <div class="scheduling-indicator" v-if="show_scheduling_indicator">
    <div style="display: flex; justify-content: flex-start; border-radius: 24">
      <div
        class="m-2 flex-min"
        style="font-weight: 600; font-size: 1.2rem"
        v-if="!isAppointmentEditMode"
      >
        Now Scheduling |
      </div>
      <div
        class="m-2 flex-min"
        style="font-weight: 600; font-size: 1.2rem"
        v-if="isAppointmentEditMode"
      >
        Now ReScheduling |
      </div>
      <div
        style="font-size: 1.1rem"
        class="flex-min ml-1 mr-2 mt-2"
        v-if="isAppointmentEditMode"
      >
        Appointment
      </div>
      <div
        style="font-size: 1.1rem"
        class="flex-min ml-1 mr-2 mt-2"
        v-if="!isAppointmentEditMode"
      >
        {{ examAssociated ? 'Exam Event | ' : 'Non-Exam Event' }}
      </div>
      <div
        class="mr-1 mt-2 flex-min"
        v-if="examAssociated && !isAppointmentEditMode"
        style="font-size: 1.1rem"
      >
        <span>{{
          `Duration: ${selectedExam.exam_type.number_of_hours} HRS | `
        }}</span>
        <br />
      </div>
      <div class="m-2 flex-min" v-if="examAssociated && !isAppointmentEditMode">
        <span>
          <strong>Exam:</strong>
          {{ selectedExam.exam_name }}
        </span>
        <br />
        <span>
          <strong>Expiry Date:</strong>
          {{ expiryDateFormat }}
        </span>
        <br />
      </div>
      <div v-if="!examAssociated" class="flex-min mx-3 mt-1">
        <span class="smaller-font">Select date and time</span>
        <br />
        <span class="smaller-font">on the calendar</span>
        <br />
      </div>
      <div class="flex-fill" />
      <div class="flex-min">
        <b-button @click="cancel" class="btn-danger mx-3 mt-1">Cancel</b-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'

import moment from 'moment'

@Component
export default class SchedulingIndicator extends Vue {
  @State('editedBooking') private editedBooking!: any
  @State('rescheduling') private rescheduling!: any
  @State('scheduling') private scheduling!: any
  @State('selectedExam') private selectedExam!: any
  @State('showEditBookingModal') private showEditBookingModal!: any
  @State('showBookingModal') private showBookingModal!: any
  @State('showOtherBookingModal') private showOtherBookingModal!: any
  @State('isAppointmentEditMode') private isAppointmentEditMode!: any

  @Getter('show_scheduling_indicator') private show_scheduling_indicator!: any;

  @Action('finishBooking') public finishBooking: any
  @Action('finishAppointment') public finishAppointment: any

  @Mutation('toggleEditBookingModal') public toggleEditBookingModal: any
  @Mutation('toggleEditApptModal') public toggleEditApptModal: any
  @Mutation('toggleRescheduling') public toggleRescheduling: any
  @Mutation('toggleApptRescheduleCancel') public toggleApptRescheduleCancel: any

  get examAssociated () {
    if (this.selectedExam && Object.keys(this.selectedExam).length > 0) {
      return true
    }
    return false
  }

  get bookingModalsHidden () {
    if (!this.showOtherBookingModal && !this.showBookingModal && !this.showEditBookingModal) {
      return true
    }
    return false
  }

  get expiryDateFormat () {
    if (this.examAssociated && this.selectedExam.expiry_date) {
      const d = moment(this.selectedExam.expiry_date)
      if (d.isValid()) {
        return d.format('MMM-DD-YYYY')
      }
    }
    return 'not applicable'
  }

  cancel () {
    if (this.isAppointmentEditMode) {
      if (this.rescheduling) {
        this.toggleEditApptModal(true)
        this.toggleRescheduling(false)
        this.toggleApptRescheduleCancel(true)
        return
      }
      this.finishAppointment()
    } else {
      if (this.rescheduling) {
        this.toggleEditBookingModal(true)
        return
      }

      let pushToExams = false
      if (this.selectedExam && this.selectedExam.referrer === 'inventory') {
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
