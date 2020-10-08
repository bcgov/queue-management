<template>
  <div id="examModal" class="q-custom-modal">
    <div class="q-custom-modal-content">
      <div class="modal_header">
        <div>
          <h5>Select an Exam to Schedule</h5>
        </div>
      </div>
      <ExamInventoryTable />
      <div class="button-flex-end">
        <div><b-button @click="cancel" class="mt-3">Cancel</b-button></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import ExamInventoryTable from '../exams/exam-inventory-table.vue'
import { Mutation } from 'vuex-class'

@Component({
  components: {
    ExamInventoryTable
  }
})
export default class ExamInventoryModal extends Vue {
  @Mutation('toggleExamInventoryModal') public toggleExamInventoryModal: any
  @Mutation('toggleScheduling') public toggleScheduling: any

  cancel () {
    this.toggleExamInventoryModal(false)
    this.toggleScheduling(false)
  }
}
</script>

<style scoped>
.button-flex-end {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}
</style>
