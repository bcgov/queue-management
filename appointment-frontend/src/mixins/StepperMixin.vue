<script lang="ts">
import { Component, Prop } from 'vue-property-decorator'
import Vue from 'vue'

@Component
export default class StepperMixin extends Vue {
  @Prop() stepForward!: () => void
  @Prop() stepBack!: () => void
}
</script>
