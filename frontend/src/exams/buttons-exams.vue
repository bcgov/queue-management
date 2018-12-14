<template>
  <div>
    <b-button v-if="showExams" class="btn-primary" @click="clickAddIndividual">Add Individual ITA Exam</b-button>
    <AddExamFormModal />
  </div>
</template>

<script>
  import { mapMutations, mapState } from 'vuex'
  import AddExamFormModal from './add-exam-form-modal'

  export default {
    name: "ButtonsExams",
    computed: {
      ...mapState([
        'user'
      ]),
      showExams() {
        if (this.user.office.exams_enabled_ind === 1) {
          return true
        }
        return false
      }
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
