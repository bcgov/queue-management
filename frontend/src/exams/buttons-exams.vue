<template v-if="showExams">
  <div class="q-w100-flex-fe pr-3" v-if="financial_designate === 1">
    <b-button class="btn-primary mr-3"
              @click="clickGenFinReport">Generate Financial Report</b-button>
    <FinancialReportModal />
  </div>
  <div class="q-w100-flex-fs" v-else>
    <b-form inline>
      <b-dd v-if="role_code === 'GA'"
            split
            class="mr-2"
            variant="primary"
            text="Add ITA Exam"
            @click="handleClick('individual')">
        <b-dd-item @click="handleClick('challenger')">Add Challenger Exam</b-dd-item>
      </b-dd>
      <b-button v-if="role_code!=='GA'"
                class="mr-1 btn-primary"
                @click="handleClick('individual')">Add ITA Exam</b-button>
      <b-button v-if="role_code==='LIAISON'"
                class="mr-1 btn-primary"
                @click="handleClick('group')">Add Group Exam</b-button>
      <b-button class="mr-1 btn-primary"
                @click="handleClick('other')">Add Other Exam</b-button>
    </b-form>
    <AddExamModal />
  </div>
</template>

<script>
  import { mapActions, mapMutations, mapState, mapGetters } from 'vuex'
  import AddExamModal from './add-exam-modal'
  import FinancialReportModal from './generate-financial-report-modal'

  export default {
    name: "ButtonsExams",
    components: { AddExamModal, FinancialReportModal },
    computed: {
      ...mapState(['addNonITA', 'showGenFinReportModal', 'user', ]),
      ...mapGetters([ 'showExams', 'role_code', 'pesticide_designate', 'financial_designate', ]),
    },
    created() {
      console.log(this.financial_designate)
    },
    methods: {
      ...mapActions(['actionRestoreAll']),
      ...mapMutations(['toggleAddExamModal', 'toggleGenFinReport',]),
      handleClick(type) {
        this.toggleAddExamModal({setup: type})
        this.toggleAddExamModal(true)
      },
      clickGenFinReport() {
        this.toggleGenFinReport(true)
      },
    }
  }
</script>
