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
          <b-form-input id="startDate"
                        type="date"
                        v-model=startDate />
        </b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="4"><label>End Date:</label></b-col>
        <b-col sm="6"><b-form-input id="endDate"
                                    type="date"
                                    v-model=endDate />
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
    import OfficeDropDownFilter from './office-dropdown-filter'
    import moment from 'moment'
    const FileDownload = require('js-file-download')
    export default {
        name: "FinancialReportModal",
        data() {
          return {
            startDate: '',
            endDate: '',
            options: [
              {text: 'ITA - Individual and Group ', value: 'ita'},
              {text: 'Pesticide', value: 'pesticide'},
              {text: 'Bulk Milk Tank Grader', value: 'milk_tank'}
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
            let form_start_date = this.startDate
            let form_end_date = this.endDate
            let exam_type = this.selectedExamType
            let url = '/exams/export/?start_date=' + form_start_date + '&end_date=' + form_end_date + '&exam_type='
                      + exam_type
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
