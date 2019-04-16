<template v-if="showExams">
  <div class="q-w100-flex-fs">
    <b-form inline>
      <b-dd v-if="role_code === 'GA'"
            split
            class="mr-1"
            variant="primary"
            text="Add ITA Exam"
            @click="handleClick('individual')">
        <b-dd-item @click="handleClick('challenger')">Add Monthly Session Exam</b-dd-item>
      </b-dd>
      <b-button v-if="role_code!=='GA'"
                class="mr-1 btn-primary"
                @click="handleClick('individual')">Add ITA Exam</b-button>
      <b-button v-if="is_liaison_designate"
                class="mr-1 btn-primary"
                @click="handleClick('group')">Add Group Exam</b-button>
      <b-button class="mr-1 btn-primary"
                @click="handleClick('other')">Add Other Exam</b-button>
      <b-button v-if="is_pesticide_designate"
                class="mr-1 btn-primary"
                @click="handleClick('pesticide')">Add Pesticide Exam</b-button>
      <b-button v-if="is_financial_designate || role_code === 'GA' || is_ita_designate"
                class="btn-primary mr-3"
                @click="clickGenFinReport">Generate Financial Report</b-button>
    <FinancialReportModal />
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
      ...mapState(['addNonITA', 'showGenFinReportModal', 'user' ]),
      ...mapGetters([
        'is_financial_designate',
        'is_ita_designate',
        'is_liaison_designate',
        'is_pesticide_designate',
        'role_code',
        'showExams',
      ]),
    },
    methods: {
      ...mapActions(['actionRestoreAll']),
      ...mapMutations(['setAddExamModalSetting', 'toggleGenFinReport',]),
      handleClick(type) {
        this.setAddExamModalSetting({setup: type})
        this.setAddExamModalSetting(true)
      },
      clickGenFinReport() {
        this.toggleGenFinReport(true)
      },
    }
  }
</script>
