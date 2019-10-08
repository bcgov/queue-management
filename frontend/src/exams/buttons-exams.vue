<template v-if="showExams">
  <div class="q-w100-flex-fs">
    <b-form inline>
      <b-dd v-if="role_code === 'GA' || is_ita_designate"
            id="add-ita"
            split
            class="mr-1"
            variant="primary"
            text="Add ITA Exam"
            @click="handleClick('individual')">
        <b-dd-item id="add_session"
                   @click="handleClick('challenger')">Add Monthly Session Exam</b-dd-item>
      </b-dd>
      <b-button v-if="!(role_code === 'GA' || is_ita_designate)"
                id="add_ita"
                class="mr-1 btn-primary"
                @click="handleClick('individual')">Add ITA Exam</b-button>
      <b-button v-if="is_liaison_designate"
                id="add_group"
                class="mr-1 btn-primary"
                @click="handleClick('group')">Add Group Exam</b-button>
      <b-button id="add_other"
                class="mr-1 btn-primary"
                @click="handleClick('other')">Add Other Exam</b-button>
      <b-button v-if="is_pesticide_designate"
                class="mr-1 btn-primary"
                id="add_pesticide"
                @click="handleClick('pesticide')">Add Pesticide Exam</b-button>
      <b-button v-if="is_financial_designate || role_code === 'GA' || is_ita_designate"
                class="btn-primary mr-3"
                @click="clickGenFinReport">Generate Financial Report</b-button>
    <FinancialReportModal />
    </b-form>
  </div>
</template>

<script>
  import { mapMutations, mapState, mapGetters } from 'vuex'
  import FinancialReportModal from './generate-financial-report-modal'

  export default {
    name: "ButtonsExams",
    components: { FinancialReportModal },
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
      ...mapMutations(['setAddExamModalSetting', 'toggleGenFinReport',]),
      handleClick(type) {
        this.setAddExamModalSetting({setup: type})
        this.setAddExamModalSetting(true)
        if (type === 'pesticide') {
          this.$store.dispatch('getPesticideExamTypes')
        }
      },
      clickGenFinReport() {
        this.toggleGenFinReport(true)
      },
    }
  }
</script>
