<template>
  <b-modal v-model="modal"
           :no-close-on-backdrop="true"
           ok-title="Submit"
           ok-variant="warning"
           hide-ok
           @ok="submit"
           hide-header
           hide-cancel
           size="md">
    <b-container style="font-size:1.1rem; border:1px solid lightgrey; border-radius: 10px" class="mb-2 pb-3" fluid>
      <b-row>
        <b-col>
          <h3>Generate Exam Report</h3>
        </b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="4"><label>Start Date:</label></b-col>
        <b-col sm="6"><b-form-input id="startDate" type="date" v-model=startDate></b-form-input></b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="4"><label>End Date:</label></b-col>
        <b-col sm="6"><b-form-input id="endDate" type="date" v-model=endDate></b-form-input></b-col>
      </b-row>
    </b-container>
  </b-modal>
</template>

<script>
    import { mapState, mapMutations, mapActions } from 'vuex'
    export default {
        name: "FinancialReportModal",
        data() {
          return {
            startDate: '',
            endDate: '',
          }
        },
        methods: {
          ...mapActions([
            'getExamsExport'
          ]),
          ...mapMutations([
            'toggleGenFinReport'
          ]),
          submit() {
            console.log("Pressed Submit")
            let form_start_date = this.startDate
            let form_end_date = this.endDate
            let url= '/exams/export/?start_date=' + form_start_date + '&end_date=' + form_end_date
            this.getExamsExport(url)
          },
        },
        computed: {
          ...mapState({
            showGenFinReportModal: state => state.showGenFinReportModal,
          }),
          modal: {
            get() {
              return this.showGenFinReportModal
            },
            set(e) {
              this.toggleGenFinReport(e)
            }
          },
        },
    }
</script>

<style scoped>

</style>
