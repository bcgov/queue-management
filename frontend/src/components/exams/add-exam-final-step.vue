<template>
  <!--  Non challenger (Monthly Sessional) exams.  -->
  <b-form v-if="addExamModal.setup !== 'challenger'">
    <b-row no-gutters>
      <b-col cols="12">
        <span style="font-size: 1rem"
          >Please Review the Details You have Entered</span
        >
      </b-col>
    </b-row>
    <b-row v-if="errors.length > 0">
      <b-col cols="12">
        <span style="font-size: 1rem; color: red">{{ submitMsg }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters class="mt-2" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Type</span>
      </b-col>
      <b-col>
        <template
          v-if="
            addExamModal.setup === 'group' ||
            addExamModal.setup === 'individual'
          "
        >
          <span :style="{ color: exam_object.exam_color }">{{
            exam_object.exam_type_name
          }}</span>
        </template>
        <template v-else>
          {{ exam_object.exam_type_name }}
        </template>
      </b-col>
    </b-row>
    <b-row
      no-gutters
      align-h="between"
      align-v="end"
      v-if="setup === 'group' || is_pesticide_designate"
    >
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Office</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ officeName }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="start" align-v="end" v-if="exam.event_id">
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
    <b-row
      no-gutters
      align-h="between"
      align-v="end"
      v-if="setup === 'individual' || setup === 'other'"
    >
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Candidate's Name</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.examinee_name }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'group'">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Students</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.number_of_students }}</span>
      </b-col>
    </b-row>
    <b-row
      no-gutters
      align-h="between"
      align-v="end"
      v-if="setup === 'individual' || setup === 'other'"
    >
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Received Date</span>
      </b-col>
      <b-col align-self="end" v-if="setup === 'individual' || setup === 'other'">
        <span class="confirm-item">{{
          formatDate(exam.exam_received_date)
        }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">{{
          setup === 'group' ? 'Exam Date' : 'Expiry Date'
        }}</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ formatDate(exam.expiry_date) }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'group'">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Time </span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ displayTime }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end" v-if="setup === 'group'">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Location </span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.offsite_location }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Method</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.exam_method }}</span>
      </b-col>
    </b-row>
    <b-row
      no-gutters
      align-h="between"
      align-v="end"
      v-if="setup === 'pesticide'"
    >
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Notes</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.notes }}</span>
      </b-col>
    </b-row>
  </b-form>
  <!--  End of non challenger (Monthly Sessional) exams.  -->

  <!--  Challenger (Monthly Sessional) exams.  -->
  <b-form v-else>
    <b-row no-gutters>
      <b-col cols="12">
        <span style="font-size: 1rem"
          >Please Review the Details You have Entered</span
        >
      </b-col>
    </b-row>
    <b-row v-if="errors.length > 0">
      <b-col cols="12">
        <span style="font-size: 1rem; color: red">{{ submitMsg }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters class="mt-2" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Type</span>
      </b-col>
      <b-col> Monthly Session Exam </b-col>
    </b-row>
    <b-row no-gutters align-h="start" align-v="end" v-if="exam.event_id">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Event ID</span>
      </b-col>
      <b-col>
        <span class="confirm-item">{{ exam.event_id }}</span>
      </b-col>
    </b-row>
    <b-row
      no-gutters
      align-h="between"
      align-v="end"
      v-if="exam.number_of_students"
    >
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Students</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ exam.number_of_students }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="start" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Date</span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ formatDate(exam.expiry_date) }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Exam Time </span>
      </b-col>
      <b-col align-self="end">
        <span class="confirm-item">{{ displayTime }}</span>
      </b-col>
    </b-row>
    <b-row no-gutters align-h="between" align-v="end">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">Location </span>
      </b-col>
      <b-col align-self="end">
        <span v-if="exam.on_or_off === 'off'" class="confirm-item">{{
          exam.offsite_location
        }}</span>
        <span v-if="exam.on_or_off === 'on'" class="confirm-item"
          >ServiceBC Office<br />{{ exam.offsite_location.title }}</span
        >
      </b-col>
    </b-row>
  </b-form>
  <!--  End of Challenger (Monthly Sessional) exams.  -->
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator'
import { Getter, State } from 'vuex-class'

import moment from 'moment'

@Component
export default class AddExamFinalStep extends Vue {
  @Prop({ default: '' })
  private submitMsg!: string

  @State('capturedExam') private exam!: any
  @State('examTypes') private examTypes!: any
  @State('captureITAExamTabSetup') private tab!: any
  @State('user') private user!: any
  @State('addExamModal') private addExamModal!: any
  @State('offices') private offices!: any

  @Getter('exam_object') private exam_object!: any;
  @Getter('is_pesticide_designate') private is_pesticide_designate!: any;

  get officeName () {
    if (this.addExamModal.setup === 'group' || this.addExamModal.setup === 'pesticide' && this.exam.office_id) {
      const office = this.offices.find(o => o.office_id == this.exam.office_id)
      return `#${office.office_id} - ${office.office_name}`
    }
    return ''
  }

  get setup () {
    if (this.addExamModal && this.addExamModal.setup) {
      return this.addExamModal.setup
    }
    return ''
  }

  get errors () {
    if (this.tab.errors) {
      return this.tab.errors
    } else {
      this.submitMsg = ''
      return []
    }
  }

  get displayTime () {
    if (this.exam && this.exam.exam_time) {
      // JSTOTS TOCHECK removed new from moment. no need to use new with moment
      return moment(this.exam.exam_time).format('h:mm a')
    }
    return ''
  }

  formatDate (d) {
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    return moment(d).format('MMM D, YYYY')
  }
}
</script>

<style scoped>
.confirm-item {
  font-weight: 500;
  font-size: 1.05rem;
}
</style>
