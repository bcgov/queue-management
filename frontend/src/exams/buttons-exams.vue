<template v-if="showExams">
  <div>
    <b-form inline>
      <b-button variant="primary" class="mr-1" @click="clickAddIndividual">Add Individual Exam</b-button>
      <b-button variant="primary" class="mr-1" @click="clickAddNonITA">Add Non-ITA Exam</b-button>
      <b-button variant="primary" class="mx-2" v-if="liaison" @click="clickAddGroup">Add Group Exam</b-button>
      <b-button variant="primary" class="mr-1" @click="clickGenFinReport">Generate Financial Report</b-button>
    </b-form>
    <AddExamFormModal />
    <FinancialReportModal />
  </div>
</template>

<script>
  import { mapMutations, mapState, mapGetters } from 'vuex'
  import AddExamFormModal from './add-exam-form-modal'
  import FinancialReportModal from './generate-financial-report-modal'

  export default {
    name: "ButtonsExams",
    components: {AddExamFormModal, FinancialReportModal },
    computed: {
      ...mapState([ 'user',
                    'showGenFinReportModal',
                    'addNonITA' ]),
      ...mapGetters([ 'showExams', ]),
      liaison() {
        if (this.user && this.user.role) {
          return (this.user.role.role_code === 'LIAISON')
        }
      }
    },
    methods: {
      ...mapMutations(['toggleAddITAExamModal', 'toggleGenFinReport', 'toggleNonITAExamModal']),
      clickAddIndividual() {
        this.toggleNonITAExamModal(false)
        this.toggleAddITAExamModal({visible: true, setup: 'individual'})
      },
      clickAddGroup() {
        this.toggleNonITAExamModal(false)
        this.toggleAddITAExamModal({visible: true, setup: 'group'})
      },
      clickGenFinReport() {
        this.toggleGenFinReport(true)
      },
      clickAddNonITA() {
        this.toggleNonITAExamModal(true)
        this.toggleAddITAExamModal({visible: true, setup: 'individual'})
      }
    }
  }
</script>
