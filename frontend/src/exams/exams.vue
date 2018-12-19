<template>
  <div v-if="user.username">
    <div v-if="showExams">
      <span class="title margin-left mt-3">Exam Inventory</span><br>
      <span class="subheader margin-left">Click an exam in the table to review its details and fulfill the exam process</span>
      <ExamInventoryTable mode="inventory" />
    </div>
    <div v-else class=center>
      <h1> Coming Soon! </h1>
    </div>
  </div>
  <div v-else>
    <div class="loader"></div>
  </div>

</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import ExamInventoryTable from './exam-inventory-table'
  export default {
    name: "Exams",
    computed: {
      ...mapState([
        'user',
      ]),
      ...mapGetters([
        'showExams',
      ])
    },
    components: { ExamInventoryTable },
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
  div.center {
    text-align: center;
  }

  .loader {
    position: relative;
    text-align: center;
    margin: 15px auto 35px auto;
    z-index: 9999;
    display: block;
    width: 80px;
    height: 80px;
    border: 10px solid rgba(0, 0, 0, .3);
    border-radius: 50%;
    border-top-color: #000;
    animation: spin 1s ease-in-out infinite;
    -webkit-animation: spin 1s ease-in-out infinite;
  }

  @keyframes spin {
    to {
      -webkit-transform: rotate(360deg);
    }
  }

  @-webkit-keyframes spin {
    to {
      -webkit-transform: rotate(360deg);
    }
  }
</style>
