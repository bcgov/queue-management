<template v-if="showExams">
  <div>
    <b-form inline>
      <b-button class="mr-1 btn-primary" @click="clickAddIndividual">Add Individual Exam</b-button>
      <b-button class="mx-2 btn-primary" v-if="liaison" @click="clickAddGroup">Add Group Exam</b-button>
    </b-form>
    <AddExamFormModal />
  </div>
</template>

<script>
  import { mapMutations, mapState, mapGetters } from 'vuex'
  import AddExamFormModal from './add-exam-form-modal'

  export default {
    name: "ButtonsExams",
    components: {AddExamFormModal },
    computed: {
      ...mapState(['user',]),
      ...mapGetters(['showExams',]),
      liaison() {
        if (this.user && this.user.role) {
          return (this.user.role.role_code === 'LIAISON')
        }
      }
    },
    methods: {
      ...mapMutations(['toggleAddITAExamModal']),
      clickAddIndividual() {
        this.toggleAddITAExamModal({visible: true, setup: 'individual'})
      },
      clickAddGroup() {
        this.toggleAddITAExamModal({visible: true, setup: 'group'})
      },
    }
  }
</script>
