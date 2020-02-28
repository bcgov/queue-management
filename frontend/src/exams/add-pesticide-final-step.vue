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

  </b-form>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
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
        }
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
      formatDate(d) {
        return new moment(d).format('MMM D, YYYY')
      }
    }
  }
</script>

<style scoped>
  .confirm-item {
    font-weight: 500; font-size: 1.05rem;
  }

</style>
