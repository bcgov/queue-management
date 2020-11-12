<template>
  <fragment>
    <AddPesticideFinalStep
      :submitMsg="submitMsg"
      v-if="modalSetup === 'pesticide'"
    />
    <AddExamFinalStep :submitMsg="submitMsg" v-else />
  </fragment>
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator'

import AddExamFinalStep from './add-exam-final-step.vue'
import AddPesticideFinalStep from './add-pesticide-final-step.vue'
import { State } from 'vuex-class'

@Component({
  components: {
    AddPesticideFinalStep,
    AddExamFinalStep
  }
})
export default class AddExamFormConfirm extends Vue {
  @Prop()
  private submitMsg!: any

  @State('addExamModal') private addExamModal!: any

  get modalSetup () {
    if (this.addExamModal && this.addExamModal.setup) {
      return this.addExamModal.setup
    }
    return null
  }

  //   computed: {
  //     ...mapState ({
  //     modalSetup (state) {
  //   if (state.addExamModal && state.addExamModal.setup) return state.addExamModal.setup
  //   return null
  // }
  //     })
  //   }
}
</script>
