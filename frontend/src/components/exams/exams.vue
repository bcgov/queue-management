<template>
  <div v-if="user.username" style="min-height: 350px">
    <div v-if="showExams">
      <span class="title margin-left mt-3">Exam Inventory</span><br />
      <span class="subheader margin-left"
        >Click an exam in the table to review its details and fulfill the exam
        process</span
      >
      <ExamInventoryTable mode="inventory" />
    </div>
    <div class="center" v-else>
      <h1>Coming Soon!</h1>
    </div>
  </div>
  <div v-else>
    <div class="q-loader"></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Getter, Mutation, State } from 'vuex-class'

import ExamInventoryTable from './exam-inventory-table.vue'

@Component({
  components: {
    ExamInventoryTable
  }
})
export default class Exams extends Vue {
  @State('serviceBegun') private serviceBegun!: any
  @State('showServiceModal') private showServiceModal!: any
  @State('serviceModalPath') private serviceModalPath!: any
  @State('user') private user!: any

  @Getter('showExams') private showExams!: any;

  @Mutation('toggleServiceModal') public toggleServiceModal: any

  filterKeyPress (e) {
    if (e.keyCode === 13) {
      e.preventDefault()
    }
  }

  mounted () {
    document.addEventListener('keydown', this.filterKeyPress)
    this.$store.dispatch('getOffices')
  }
}
</script>

<style scoped>
.subheader {
  font-size: 1rem !important;
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
