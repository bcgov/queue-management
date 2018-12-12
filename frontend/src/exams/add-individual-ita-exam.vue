<template>
  <b-modal v-model="modalVisible"
           hide-header
           ok-only
           ok-title="Close">
    This will be the exam capture form
  </b-modal>
</template>

<script>
  import { mapState, mapMutations } from 'vuex'

  export default {
    name: "AddIndividualItaExam",
    computed: {
      ...mapState(['addIndividualITAExamModalVisibe']),
      modalVisible: {
        get() {
          return this.addIndividualITAExamModalVisibe
        },
        set(e) {
          this.toggleAddIndividualITAExam(e)
        }
      }
    },
    methods: {
      ...mapMutations(['toggleAddIndividualITAExam'])
    }
  }
</script>

<style scoped>

</style>
