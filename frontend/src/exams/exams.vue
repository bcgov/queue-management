<template>
  <div>
    <span class="title margin-left mt-3">Exam Inventory</span><br>
    <span class="subheader margin-left">Click an exam in the table to review its details and fulfill the exam process</span>
    <ExamInventoryTable mode="inventory" />
  </div>

</template>

<script>
  import ExamInventoryTable from './exam-inventory-table'

  export default {
    name: "Exams",
    components: { ExamInventoryTable }
  }
</script>

<style scoped>
  .subheader {
    font-size: 1.0rem !important;
  }
  .margin-left {
    margin-left: 20px;
  }
  .title {
    font-size: 2rem;
    font-weight: 600;
  }
</style>
