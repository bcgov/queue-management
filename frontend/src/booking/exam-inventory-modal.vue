<template>
  <div id="examModal" class="q-custom-modal">
    <div class="q-custom-modal-content">
      <div class="modal_header">
        <div>
          <div style="q-inline-title">Select an Exam to Schedule</div>
        </div>
      </div>
      <ExamInventoryTable />
        <div class="button-flex-end">
          <div><b-button @click="cancel" class="mt-3">Cancel</b-button></div>
        </div>
    </div>
  </div>
</template>

<script>
  import { mapMutations } from 'vuex'
  import ExamInventoryTable from '../exams/exam-inventory-table'

  export default {
    name: "ExamInventoryModal",
    components: { ExamInventoryTable },
    methods: {
      ...mapMutations(['toggleExamInventoryModal', 'navigationVisible', 'toggleScheduling']),
      cancel() {
        this.toggleExamInventoryModal(false)
        this.navigationVisible(true)
        this.toggleScheduling(false)
      }
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

