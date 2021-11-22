<template>
  <b-form>
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
    <b-row no-gutters class="summary-box my-3" align-v="end">
      <template v-if="isGroupExam">
        <b-col
          cols="12"
          class="summary-box-col group-exam"
          v-for="(candidate, i) of candidateTableData"
          :key="i + 'groupsumary'"
        >
          <div class="summary-heading" v-if="candidate.exam_type_name">
            {{ candidate.exam_type_name }}
            <span class="qty">candidates: {{ candidate.qty }}</span>
          </div>
          <div class="summary-text" v-if="candidate.name">
            - {{ candidate.name }}
          </div>
        </b-col>
      </template>
      <b-col
        cols="6"
        class="summary-box-col"
        v-for="(item, i) of displayData"
        :key="i + 'sumary'"
      >
        <div class="summary-heading">{{ item.heading }}:</div>
        <div class="summary-text">{{ item.text }}</div>
      </b-col>
    </b-row>
    <!-- for SBC Based exam flow -->
    <template>
      <b-row class="mt-2" align-v="end">
        <b-col cols="12">
          <b-button
            variant="primary"
            @click="requestExam()"
            :disabled="isRequestExamBtnLoading || !!examBcmpJobId"
          >
            <span v-if="isRequestExamBtnLoading">
              <b-spinner small></b-spinner>
              Please Wait...
            </span>
            <span v-else> Request Exam </span>
          </b-button>
        </b-col>
        <b-col cols="12" class="mt-4" v-if="examBcmpJobId">
          <b-alert variant="success" show>
            Job Id generated from BCMP: {{ examBcmpJobId }} <br /><br />
            <strong
              >Click on the "Submit" button to finish adding the Environment
              exam</strong
            >
          </b-alert>
        </b-col>
      </b-row>
      <b-row class="mt-4" align-v="end" v-if="isExamReqFailed">
        <b-col cols="12">
          <b-alert variant="warning" show>
            Failed to request exam from BCMP, please follow the manual steps and
            enter the generated job id in the input below, then
            <br />
            <strong
              >Click on the "Submit" button to finish adding the Environment
              exam</strong
            >
          </b-alert>
          <label for="bcmp-job-id">BCMP Job Id:</label>
          <b-form-input
            id="bcmp-job-id"
            v-model="bcmpJobId"
            type="text"
            aria-describedby="generated-bcmp-jobid"
            placeholder="Enter generated BCMP job id"
            trim
            @blur="addBCMPJobId()"
          ></b-form-input>
        </b-col>
        <b-col> </b-col>
      </b-row>
    </template>
  </b-form>
</template>

<script lang="ts">
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'

import { mapState } from 'vuex'

import moment from 'moment'

@Component({
  computed: {
    ...mapState({
      candidateTableData: (state: any) => state.addExamModule.candidateTableData
    })

  }
})
export default class AddPesticideFinalStep extends Vue {
  @Prop({ default: '' })
  private submitMsg!: any

  @State('capturedExam') private exam!: any
  @State('examTypes') private examTypes!: any
  @State('captureITAExamTabSetup') private tab!: any
  @State('user') private user!: any
  @State('addExamModal') private addExamModal!: any
  @State('offices') private offices!: any
  @State('examBcmpJobId') private examBcmpJobId!: any

  @Getter('exam_object') private exam_object!: any;
  @Getter('is_pesticide_designate') private is_pesticide_designate!: any;

  @Action('clickPesticideRequestExam') public clickPesticideRequestExam: any
  @Mutation('setBCMPJobId') public setBCMPJobId: any

  public headings: any = {
    exam_type_name: 'Exam Type',
    fees: 'Exam Fees',
    examinee_name: 'Candidate',
    examinee_phone: "Candidate's Phone",
    examinee_email: "Candidate's Email",
    receipt_number: 'Receipt Number',
    payee_name: 'Payee Name',
    payee_email: 'Payee Email',
    payee_phone: 'Payee Phone',
    offsite_location: 'Location',
    exam_time_str: 'Exam Date',
    notes: 'Notes'
  }

  public bcmpJobId: any = ''
  public isExamReqFailed: boolean = false
  public generatedJobId: any = ''
  public isGroupExam: boolean = false
  public isRequestExamBtnLoading: boolean = false

  get displayData () {
    this.isGroupExam = (this.exam.ind_or_group == 'group')
    const examObj = this.exam
    if (this.exam.exam_type_id) {
      const examType = this.examTypes.find(examType => (examType.exam_type_id == this.exam.exam_type_id))
      examObj.exam_type_name = (examType) ? examType.exam_type_name : ''
    }
    if (this.exam.exam_time) {
      examObj.exam_time_str = `${moment(this.exam.expiry_date).format('YYYY-MMM-DD')} ${moment(this.exam.exam_time).format('hh:mm A')}`
    }
    const keys = Object.keys(examObj)
    const headings = Object.keys(this.headings)
    const output: any = []
    keys.forEach(key => {
      if (headings.includes(key)) {
        if (examObj[key]) {
          output.push({
            heading: this.headings[key],
            text: examObj[key]
          })
        }
      }
    })
    return output
  }

  get officeName () {
    if (this.addExamModal.setup === 'group' || this.addExamModal.setup === 'pesticide' && this.exam.office_id) {
      const office = this.offices.find(o => o.office_id == this.exam.office_id)
      return `#${office.office_id} - ${office.office_name}`
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

  formatDate (d) {
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    return moment(d).format('MMM D, YYYY')
  }

  requestExam () {
    this.isRequestExamBtnLoading = true
    this.clickPesticideRequestExam().then(bcmp_job_id => {
      console.log('bcmp_job_id: ', bcmp_job_id)
      this.setBCMPJobId(bcmp_job_id)
      this.generatedJobId = bcmp_job_id
      this.isRequestExamBtnLoading = false
    }).catch(error => {
      console.log(error)
      this.isExamReqFailed = true
      this.isRequestExamBtnLoading = false
    })
  }

  addBCMPJobId () {
    console.log(this.bcmpJobId)
    this.setBCMPJobId(this.bcmpJobId)
  }
}
</script>

<style scoped>
.confirm-item {
  font-weight: 500;
  font-size: 1.05rem;
}

.summary-box {
  padding: 10px 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.summary-box-col {
  padding-bottom: 8px;
}
.summary-heading {
  font-weight: 700;
}
.summary-text {
  padding-left: 12px;
}
.group-exam .summary-heading {
  background: #ddd;
  padding: 3px 6px;
  border-radius: 4px;
}
.group-exam .summary-heading .qty {
  float: right;
}
.group-exam .summary-box-col {
  padding-bottom: 4px;
}
</style>
