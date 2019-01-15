<template>
  <div class="scheduling-indicator"
       v-if="showSchedulingIndicator">
    <div style="display: flex; justify-content: flex-start; border-radius: 24">
      <div class="m-2 flex-min" style="font-weight:600; font-size:1.2rem">Now Scheduling | </div>
      <div style="font-size: 1.1rem;" class="flex-min ml-1 mr-2 mt-2">
        {{ scheduling ? 'Exam Event | ' : 'Non-Exam Event' }}
      </div>
      <div class="mr-1 mt-2 flex-min" v-if="scheduling" style="font-size: 1.1rem">
        <span>{{ `Duration: ${selectedExam.exam_type.number_of_hours} HRS | ` }}</span><br>
      </div>
      <div class="m-2 flex-min" v-if="scheduling">
        <span><b>Exam: </b> {{ selectedExam.exam_name }}</span><br>
        <span><b>Expiry Date: </b>{{ expiryDateFormat }}</span><br>
      </div>
      <div v-if="schedulingOther" class="flex-min mx-3 mt-1">
        <span class="smaller-font">Click and Drag to select</span><br>
        <span class="smaller-font">a time on the calendar</span><br>
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
  import { mapState } from 'vuex'
  import moment from 'moment'

  export default {
    name: "SchedulingIndicator",
    computed: {
      ...mapState(['showSchedulingIndicator', 'scheduling', 'schedulingOther', 'selectedExam',]),
      expiryDateFormat() {
        if (this.selectedExam && this.selectedExam.expiry_date) {
          return moment(this.selectedExam.expiry_date).format('MMM-DD-YYYY')
        }
      }
    },
    methods: {
      cancel() {
        this.$root.$emit('cancel')
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