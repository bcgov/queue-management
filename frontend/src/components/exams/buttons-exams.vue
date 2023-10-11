<template v-if="showExams">
  <div class="q-w100-flex-fs">
    <b-form inline>
      <b-dd
        v-if="role_code === 'GA' || is_office_manager"
        id="add-ita"
        split
        class="mr-1"
        variant="primary"
        text="Add SkilledTradesBC Exam"
        @click="handleClick('individual')"
      >
        <b-dd-item id="add_session" @click="handleClick('challenger')"
          >Add Monthly Session Exam</b-dd-item
        >
      </b-dd>
      <b-button
        v-if="!(role_code === 'GA' || is_office_manager)"
        id="add_ita"
        class="mr-1 btn-primary"
        @click="handleClick('individual')"
        >Add ITA Exam</b-button
      >
      <b-button
        v-if="is_ita2_designate"
        id="add_group"
        class="mr-1 btn-primary"
        @click="handleClick('group')"
        >Add Group Exam</b-button
      >
      <b-button
        id="add_other"
        class="mr-1 btn-primary"
        @click="handleClick('other')"
        >Add Other Exam</b-button
      >
      <b-button
        v-if="is_pesticide_designate"
        class="mr-3 btn-primary"
        id="add_pesticide"
        @click="handleClick('pesticide')"
        >Add Environment Exam</b-button
      >
      <b-button
        v-if="is_financial_designate || role_code === 'GA' || is_office_manager"
        class="btn-primary mr-3"
        @click="clickGenFinReport"
        >Generate Financial Report</b-button
      >
      <FinancialReportModal />
    </b-form>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import { Getter, Mutation, State } from 'vuex-class'

import FinancialReportModal from './generate-financial-report-modal.vue'

@Component({
  components: {
    FinancialReportModal
  }
})
export default class ButtonsExams extends Vue {
  @State('addNonITA') private addNonITA!: any
  @State('showGenFinReportModal') private showGenFinReportModal!: any
  @State('user') private user!: any

  @Getter('is_financial_designate') private is_financial_designate!: any;
  @Getter('is_office_manager') private is_office_manager!: any;
  @Getter('is_ita2_designate') private is_ita2_designate!: any;
  @Getter('is_pesticide_designate') private is_pesticide_designate!: any;
  @Getter('role_code') private role_code!: any;
  @Getter('showExams') private showExams!: any;

  @Mutation('setAddExamModalSetting') public setAddExamModalSetting: any
  @Mutation('toggleGenFinReport') public toggleGenFinReport: any

  handleClick (type) {
    this.setAddExamModalSetting({ setup: type })
    this.setAddExamModalSetting(true)
    if (type === 'pesticide') {
      this.$store.dispatch('getPesticideExamTypes')
      this.$store.dispatch('getPesticideOfficeInvigilators')
      this.$store.dispatch('getPesticideOffsiteInvigilators')
    }
  }

  clickGenFinReport () {
    this.toggleGenFinReport(true)
  }
}
</script>
