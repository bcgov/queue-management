<template>
  <b-modal
    size="sm"
    :centered="t"
    :hide-footer="t"
    :hide-header="t"
    :ok-disabled="t"
    :cancel-disabled="t"
    :visible="showResponseModal"
    @hidden="hideResponseModal"
  >
    Thank-you for submitting your feedback. We'll get right on it.
  </b-modal>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Mutation, State } from 'vuex-class'

@Component
export default class Response extends Vue {
  @State('showResponseModal') private showResponseModal!: any
  @Mutation('hideResponseModal') public hideResponseModal: any

  public t: boolean = true
  public f: boolean = false
}
</script>
