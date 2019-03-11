<template v-if="showExams">
  <div class="q-w100-flex-fs">
    <div style="flex-grow: 12">
      <b-form inline>
        <b-button v-if="financial_designate === 0 "
                  class="mr-1 btn-primary"
                  @click="clickAddIndividual">Add ITA Exam</b-button>
        <b-button v-if="role_code==='LIAISON' && financial_designate === 0 "
                  class="mr-1 btn-primary"
                  @click="clickAddGroup">Add Group Exam</b-button>
        <b-button v-if="financial_designate === 0 "
                  class="mr-1 btn-primary"
                  @click="clickAddNonITA">Add Other Exam</b-button>
        <!-- TODO re-implement v-if="pesticide_designate === 1 && financial_designate === 0" when pesticide modal is re-activated -->
        <b-button v-if="1 == 0"
                  class="btn-primary"
                  @click="clickAddPesticide">Add Pesticide Exam</b-button>
      </b-form>
    </div>
    <div style="flex-grow: 1">
      <b-button v-if="financial_designate === 1"
                class="btn-primary"
                @click="clickGenFinReport">Generate Financial Report</b-button>
    </div>
    <AddExamModal />
    <FinancialReportModal />
  </div>
</template>

<script>
  import { mapMutations, mapState, mapGetters } from 'vuex'
  import AddExamModal from './add-exam-modal'
  import FinancialReportModal from './generate-financial-report-modal'

  export default {
    name: "ButtonsExams",
    components: { AddExamModal, FinancialReportModal },
    computed: {
      ...mapState(['addNonITA', 'showGenFinReportModal', 'user',]),
      ...mapGetters([ 'showExams', 'role_code', 'pesticide_designate', 'financial_designate', ]),
    },
    created() {
      console.log(this.financial_designate)
    },
    methods: {
      ...mapMutations(['toggleAddExamModal', 'toggleGenFinReport',]),
      clickAddIndividual() {
        this.toggleAddExamModal({setup: 'individual'})
        this.toggleAddExamModal(true)
      },
      clickAddGroup() {
        this.toggleAddExamModal({setup: 'group'})
        this.toggleAddExamModal(true)
      },
      clickGenFinReport() {
        this.toggleGenFinReport(true)
      },
      clickAddNonITA() {
        this.toggleAddExamModal({setup: 'other'})
        this.toggleAddExamModal(true)
      },
      clickAddPesticide() {
        this.toggleAddExamModal({setup: 'pesticide'})
        this.toggleAddExamModal(true)
      }
    }
  }
</script>
