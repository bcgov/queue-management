<template>
  <div v-if="user.username" style="min-height: 350px">
    <div v-if="showExams">
      <span class="title margin-left mt-3">Exam Inventory</span><br>
      <span class="subheader margin-left">Click an exam in the table to review its details and fulfill the exam process</span>
      <ExamInventoryTable mode="inventory" />
    </div>
    <div class="center" v-else>
      <h1> Coming Soon! </h1>
    </div>
  </div>
  <div v-else>
    <div class="q-loader"></div>
  </div>

</template>

<script>
  import { mapMutations, mapGetters, mapState } from 'vuex'
  import ExamInventoryTable from './exam-inventory-table'

  export default {
    name: "Exams",
    components: { ExamInventoryTable },
    mounted() {
      this.$store.dispatch('getOffices')
    },
    computed: {
      ...mapState({
        serviceBegun: 'serviceBegun',
        showServiceModal: 'showServiceModal',
        serviceModalPath: 'serviceModalPath',
        user: 'user',
      }),
      ...mapGetters(['showExams', ]),
    },
    methods: {
      ...mapMutations(['toggleServiceModal', ]),
    }
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
</style>
