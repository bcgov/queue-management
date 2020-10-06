<template>
  <b-modal
    v-model="modal"
    :no-close-on-backdrop="true"
    ok-title="Submit"
    ok-variant="primary"
    @ok="submit"
    @cancel="cancel"
    hide-ok
    hide-header
    size="md"
  >
    <b-container
      style="font-size: 1.1rem; border-radius: 10px"
      class="mb-2 pb-3"
      fluid
    >
      <b-row>
        <b-col>
          <h3>Generate Exam Report</h3>
        </b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="4"><label>Start Date:</label></b-col>
        <b-col sm="5.5">
          <DatePicker
            v-model="startDate"
            input-class="form-control"
            class="w-100 less-10-mb"
            lang="en"
          />
        </b-col>
      </b-row>
      <b-row class="my-1">
        <b-col sm="4"><label>End Date:</label></b-col>
        <b-col sm="5.5">
          <DatePicker
            v-model="endDate"
            input-class="form-control"
            class="w-100 less-10-mb"
            lang="en"
          />
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="4"><label>Exam Types:</label></b-col>
        <b-col sm="5.5>">
          <b-form-group v-if="selectedExamFilter !== ''">
            <b-dropdown
              id="exam_filter_types_wo_filter"
              :text="this.selectedExamFilter"
              class="w-100 mb-3"
              variant="primary"
              v-model="selectedExamType"
            >
              <b-dropdown-item
                v-for="option in options"
                @click="
                  selectedExamType = option.value;
                  selectedExamFilter = option.text;
                "
                :key="option.value"
              >
                {{ option.text }}</b-dropdown-item
              >
            </b-dropdown>
          </b-form-group>
          <b-form-group v-else>
            <b-dropdown
              id="exam_filter_types_w_filter"
              text="Click for Filter Options"
              class="w-100 mb-3"
              variant="primary"
              v-model="selectedExamType"
            >
              <b-dropdown-item
                v-for="option in options"
                @click="
                  selectedExamType = option.value;
                  selectedExamFilter = option.text;
                "
                :key="option.value"
              >
                {{ option.text }}</b-dropdown-item
              >
            </b-dropdown>
          </b-form-group>
        </b-col>
      </b-row>
    </b-container>
  </b-modal>
</template>

<script>
import { mapActions, mapMutations, mapState } from 'vuex'
import DatePicker from 'vue2-datepicker'
import moment from 'moment'
const FileDownload = require('js-file-download')
export default {
  name: 'FinancialReportModal',
  components: { DatePicker },
  data () {
    return {
      startDate: '',
      endDate: '',
      options: [
        { text: 'All Exams', value: 'all_exams' },
        { text: 'All Booking Events', value: 'all_bookings' },
        { text: 'ITA Individual and Group Exams', value: 'ita' },
        { text: 'All Non-ITA Exams', value: 'all_non_ita' }
      ],
      selectedExamType: '',
      selectedExamFilter: ''
    }
  },
  methods: {
    ...mapActions([
      'getExamsExport',
      'getExamTypes'
    ]),
    ...mapMutations([
      'toggleGenFinReport'
    ]),
    cancel () {
      this.selectedExamType = ''
      this.selectedExamFilter = ''
    },
    submit () {
      const form_start_date = moment.utc(this.startDate).format('YYYY-MM-DD')
      const form_end_date = moment.utc(this.endDate).format('YYYY-MM-DD')
      const url = '/exams/export/?start_date=' + form_start_date + '&end_date=' + form_end_date + '&exam_type=' +
        this.selectedExamType
      const today = moment().format('YYYY-MM-DD_HHMMSS')
      const filename = 'export-csv-' + today + '.csv'
      this.getExamsExport(url)
        .then(resp => {
          FileDownload(resp.data, filename)
        })
      this.startDate = ''
      this.endDate = ''
      this.selectedExamType = ''
      this.selectedExamFilter = ''
    }
  },
  computed: {
    ...mapState({
      showGenFinReportModal: state => state.showGenFinReportModal
    }),
    modal: {
      get () {
        return this.showGenFinReportModal
      },
      set (e) {
        this.selectedExamFilter = ''
        this.toggleGenFinReport(e)
      }
    }
  }
}
</script>

<style scoped>
</style>
