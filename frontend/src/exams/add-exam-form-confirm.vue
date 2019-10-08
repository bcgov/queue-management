<template>
  <fragment>
    <AddPesticideFinalStep :submitMsg="submitMsg" v-if="modalSetup === 'pesticide'" />
    <AddExamFinalStep :submitMsg="submitMsg" v-else />

  </fragment>
</template>

<script>
  import { mapState } from 'vuex'
  import AddExamFinalStep from './add-exam-final-step'
  import AddPesticideFinalStep from './add-pesticide-final-step'

  export default {
    name: "AddExamFormConfirm",
    props: [ 'submitMsg' ],
    components: { AddPesticideFinalStep, AddExamFinalStep },
    computed: {
      ...mapState({
        modalSetup(state) {
          if (state.addExamModal && state.addExamModal.setup) return state.addExamModal.setup
          return null
        }
      })
    }
  }
</script>
