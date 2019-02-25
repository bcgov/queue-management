<template>
  <b-modal v-model="modal"
           :no-close-on-backdrop="true"
           ok-title="Submit"
           ok-variant="primary"
           hide-ok
           @ok="submit"
           hide-header
           hide-cancel
           size="md">
    <b-container style="font-size:1.1rem; border-radius: 10px" class="mb-2 pb-3" fluid>
      <b-row>
        <b-col>
          <h3>Generate Exam Report</h3>
        </b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="4"><label>Start Date:</label></b-col>
        <b-col sm="6">
          <DatePicker v-model="startDate"
                      input-class="form-control"
                      class="w-100 less-10-mb"
                      lang="en"/>
        </b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="4"><label>End Date:</label></b-col>
        <b-col sm="6">
          <DatePicker v-model="endDate"
                      input-class="form-control"
                      class="w-100 less-10-mb"
                      lang="en"/>
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="4"><label>Exam Types:</label></b-col>
        <b-col sm="6>">
          <b-form-group>
            <b-form-radio-group :options="options"
                                stacked
                                v-model="selectedExamType" />
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>
  </b-modal>
</template>

<script>
    import { mapState, mapMutations, mapActions } from 'vuex'
    import DatePicker from 'vue2-datepicker'
    import moment from 'moment'
    const FileDownload = require('js-file-download')
    export default {
        name: "FinancialReportModal",
        components: { DatePicker },
        data() {
          return {
            startDate: '',
            endDate: '',
            options: [
              {text: 'All Exams', value: 'all'},
              {text: 'ITA - Individual and Group ', value: 'ita'},
              {text: 'All Non-ITA Exams', value: 'all_non_ita'},
              {text: 'Veterinary Exam', value: 'veterinary'},
              {text: 'Milk Grader', value: 'milk_tank'},
              {text: 'Pesticide', value: 'pesticide'}
            ],
            selectedExamType: '',
          }
        },
        methods: {
          ...mapActions([
            'getExamsExport',
            'getExamTypes',
          ]),
          ...mapMutations([
            'toggleGenFinReport',
          ]),
          submit() {
            let form_start_date = moment.utc(this.startDate).format('YYYY-MM-DD')
            let form_end_date = moment.utc(this.endDate).format('YYYY-MM-DD')
            let url = '/exams/export/?start_date=' + form_start_date + '&end_date=' + form_end_date + '&exam_type='
                      + this.selectedExamType
            let today = moment().format('YYYY-MM-DD_HHMMSS')
            let filename = 'export-csv-' + today + '.csv'
            this.getExamsExport(url)
              .then(resp => {
                FileDownload(resp.data, filename)
              })
            this.startDate = ''
            this.endDate = ''
            this.selectedExamType = ''
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
        }
    }
</script>

<style scoped>
</style>
