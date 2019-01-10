<template>
  <div class="scheduling-indicator"
       v-if="showSchedulingIndicator">
    <div style="display: flex; justify-content: flex-start; border-radius: 24">
      <div class="mr-2 flex-min ">
        <span class="vertical-margins"
              style="font-weight:600; font-size:1.2rem">Now Scheduling</span><br>
      </div>
      <div style="font-size: 1.1rem;" class="flex-min  mx-3">
        {{ scheduling ? 'Exam Event' : 'Non-Exam Event' }}
      </div>
      <div class="mr-3  flex-min" v-if="scheduling" style="font-size: 1.1rem">
        <span>Duration: {{ selectedExam.exam_type.number_of_hours }} HRS</span><br>
      </div>
      <div class="mr-3 flex-min " v-if="scheduling">
        <span><b>Exam: </b> {{ selectedExam.exam_name }}</span><br>
        <span><b>Expiry Date: </b>{{ expiryDateFormat }}</span><br>
      </div>
      <div v-if="schedulingOther" class="w-10 flex-min mx-3 ">
        <span class="smaller-font">Click and Drag to select</span><br>
        <span class="smaller-font">a time on the calendar</span><br>
      </div>
      <div class="flex-fill " />
      <div style="margin-top: auto; margin-bottom: auto;" class="flex-min">
        <b-button @click="cancel"
                  class="btn-danger ml-3">Cancel</b-button>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import moment from 'moment'

  export default {
    name: "SchedulingIndicator",
    props: ['cancel'],
    computed: {
      ...mapState(['showSchedulingIndicator', 'scheduling', 'schedulingOther', 'selectedExam',]),
      expiryDateFormat() {
        console.log(this.selectedExam)
        if (this.selectedExam && this.selectedExam.expiry_date) {
          return moment(this.selectedExam.expiry_date).format('MMM-DD-YYYY')
        }
      }
    }
  }
</script>

<style scoped>
  flex-min {
    flex-basis: min-content;
  }
  flex-fill {
    flex-basis: fill;
  }
  .scheduling-indicator {
    width: 300;
    background-color: #a9fcc6;
    padding: 8px 16px 8px 16px;
    margin: -5px 15px 10px 15px;
  }
</style>