<template>
  <div>
    <b-button class="btn-primary" @click="clickAddIndividual">Add Individual ITA Exam</b-button>
    <AddExamFormModal />
  </div>
</template>

<script>
  import { mapMutations } from 'vuex'
  import AddExamFormModal from './add-exam-form-modal'

  export default {
    name: "ButtonsExams",
    components: {AddExamFormModal },
    methods: {
      ...mapMutations(['toggleAddIndividualITAExam']),
      clickAddIndividual() {
        this.toggleAddIndividualITAExam(true)
      }
    }
  }
</script>

<style scoped>

</style>
