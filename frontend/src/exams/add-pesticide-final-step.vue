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
    <b-row no-gutters class="mt-2" align-v="end" v-for="(item, i) of displayData" :key="i+'sumary'">
      <b-col cols="1" />
      <b-col cols="3">
        <span class="confirm-header">{{ item.heading }}</span>
      </b-col>
      <b-col>
          {{ item.text }}
      </b-col>
    </b-row>
    <!-- for SBC Based exam flow -->
    <template>
      <b-row class="mt-2" align-v="end">
        <b-col cols="12">
          <b-button
            variant="primary"
            @click="requestExam()"
            :disabled="isExamReqFailed"
          >Request Exam</b-button>
        </b-col>
        <b-col cols="12" class="mt-4" v-if="generatedJobId">
          <b-alert variant="success" show>
            Job Id generated from BCMP: {{generatedJobId}}
            <br><br>
            <strong>Click on the "Submit" button to finish adding the pesticide exam</strong>
          </b-alert>
        </b-col>
      </b-row>
      <b-row class="mt-4" align-v="end" v-if="isExamReqFailed">
        <b-col cols="12">
          <b-alert variant="warning" show>
            Failed to request exam from BCMP, please follow the manual steps and enter the generated job id in the input below, then
            <br>
            <strong>Click on the "Submit" button to finish adding the pesticide exam</strong>
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
        <b-col>
        </b-col>
      </b-row>
    </template>

  </b-form>
</template>

<script>
  import { mapState, mapGetters, mapActions, mapMutations } from 'vuex'
  import moment from 'moment'

  export default {
    name: "AddPesticideFinalStep",
    props: ['submitMsg'],
    data() {
      return {
        headings: {
          pesticide_type: "Pesticide Exam Type",
          fees: "Fees",
          examinee_name: "Candidate",
          examinee_phone: "Candidate's Phone",
          examinee_email: "Candidate's Email",
          receipt_number: "Receipt Number",
          payee_name: "Payee Name",
          payee_email: "Payee Email",
          payee_phone: "Payee Phone",
          offsite_location: "Location"
        },
        bcmpJobId: '',
        isExamReqFailed: false,
        generatedJobId: '',
      }
    },
    computed: {
      ...mapState({
        exam: state => state.capturedExam,
        examTypes: state => state.examTypes,
        tab: state => state.captureITAExamTabSetup,
        user: state => state.user,
        addExamModal: state => state.addExamModal,
        offices: state => state.offices,
      }),
      displayData() {
        let keys = Object.keys(this.exam)
        let headings = Object.keys(this.headings)
        let output = []
        keys.forEach(key => {
          if (headings.includes(key)) {
            if (this.exam[key]) {
              output.push({
                heading: this.headings[key],
                text: this.exam[key]
              })
            }
          }
        })
        return output
      },
      ...mapGetters(['exam_object', 'is_pesticide_designate', ]),
      officeName() {
        if (this.addExamModal.setup === 'group' || this.addExamModal.setup === 'pesticide' && this.exam.office_id ) {
          let office = this.offices.find(o => o.office_id == this.exam.office_id)
          return `#${office.office_id} - ${office.office_name}`
        }
        return ''
      },

      errors() {
        if (this.tab.errors) {
          return this.tab.errors
        } else {
          this.submitMsg = ''
          return []
        }
      },

    },
    methods: {
      ...mapActions([
        'clickPesticideRequestExam',
      ]),
      ...mapMutations([
        'setBCMPJobId',
      ]),
      formatDate(d) {
        return new moment(d).format('MMM D, YYYY')
      },

      requestExam() {
        this.clickPesticideRequestExam().then(bcmp_job_id => {
          console.log("bcmp_job_id: ", bcmp_job_id)
          this.setBCMPJobId(bcmp_job_id);
          this.generatedJobId = bcmp_job_id;
        }).catch(error => {
          console.log(error)
          this.isExamReqFailed = true;
        })
      },

      addBCMPJobId() {
        console.log(this.bcmpJobId)
        this.setBCMPJobId(this.bcmpJobId)
      }
    }
  }
</script>

<style scoped>
  .confirm-item {
    font-weight: 500; font-size: 1.05rem;
  }

</style>
