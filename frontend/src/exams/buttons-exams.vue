<template>
  <div>
    <b-button v-if="showExams" class="btn-primary" @click="clickAddIndividual">Add Individual ITA Exam</b-button>
    <AddExamFormModal v-if="showExams" />
  </div>
</template>

<script>
  import { mapMutations, mapState, mapGetters } from 'vuex'
  import AddExamFormModal from './add-exam-form-modal'

  export default {
    name: "ButtonsExams",
    computed: {
      ...mapState(['user', 'scheduling', 'selectedExam']),
      ...mapGetters([
        'showExams',
      ]),
    },
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
