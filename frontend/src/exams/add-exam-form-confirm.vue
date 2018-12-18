<template>
  <b-form>
    <b-row no-gutters>
      <b-col cols="12">
        <span style="font-size:1rem">Please Review the Details You have Entered</span>
      </b-col>
    </b-row>
    <b-row v-if="errors.length > 0">
      <b-col cols="12">
        <span style="font-size:1rem; color: red">{{ submitMsg }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters class="mt-2" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Type</span>
      </b-col>
      <b-col>
        <span :style="{color: examObject.exam_type_colour}">
          {{ examObject.exam_type_name }}
        </span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="start" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Event ID</span>
      </b-col>
      <b-col>
        <span class="confirm-item">{{ exam.event_id }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="end" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Name</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.exam_name }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Writer's Name</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.examinee_name }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Received Date</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.exam_received_date }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Expiry Date</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.expiry_date }}</span>
      </b-col>
    </b-row>
  </b-form>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: "AddExamFormConfirm",
    props: ['submitMsg'],
    computed: {
      ...mapState({
        exam: state => state.capturedExam,
        examTypes: state => state.examTypes,
        tab: state => state.captureITAExamTabSetup,
      }),
      errors() {
        if (this.tab.errors) {
          return this.tab.errors
        } else {
          this.submitMsg = ''
          return []
        }
      },
      examObject() {
        if (this.exam && this.exam.exam_type_id) {
          return this.examTypes.find(type=>type.exam_type_id == this.exam.exam_type_id)
        }
      }
    }
  }
</script>

<style scoped>
  .confirm-item {
    font-weight: 500; font-size: 1.05rem;
  }

</style>
