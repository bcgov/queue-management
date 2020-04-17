<template>
  <v-stepper
    v-model="stepElement"
    alt-labels
  >
    <v-stepper-header>
      <template v-for="bookingStep in bookingSteppers">
        <v-stepper-step
          :key="`${bookingStep.step}-step`"
          :complete="stepElement > bookingStep.step"
          :step="bookingStep.step"
          editable
        >
          <div class="step-label">
            {{bookingStep.label}}
          </div>
        </v-stepper-step>
        <v-divider
          v-if="bookingStep.step !== bookingSteppers.length"
          :key="`${bookingStep.step}-divider`"
        >
        </v-divider>
      </template>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content
        v-for="bookingStep in bookingSteppers"
        :key="`${bookingStep.step}-content`"
        :step="bookingStep.step"
      >
        <v-card
          class="mb-12"
          color="grey lighten-1"
          height="200px"
        >
          {{bookingStep.label}}
        </v-card>

        <v-btn
          color="primary"
          @click="nextStep(bookingStep.step)"
        >
          Continue
        </v-btn>

        <v-btn text>Cancel</v-btn>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script lang="ts">
// Libraries
import { Component, Vue } from 'vue-property-decorator'

// Components
import { HelloWorld } from '@/components/Home'

@Component({
  components: {
    HelloWorld
  }
})
export default class AppointmentBookingView extends Vue {
  private stepElement = 1
  private bookingSteppers = [
    {
      step: 1,
      label: 'Select Service'
    },
    {
      step: 2,
      label: 'Select Location'
    },
    {
      step: 3,
      label: 'Select a Date'
    },
    {
      step: 4,
      label: 'Appointment Summary'
    },
    {
      step: 5,
      label: 'Login to Confirm Appointment'
    }
  ]

  private nextStep (step) {
    if (step === this.bookingSteppers.length) {
      this.stepElement = 1
    } else {
      this.stepElement = step + 1
    }
  }
}
</script>

<style lang="scss" scoped>
.step-label {
  text-align: center;
  line-height: 1.25;
}
</style>
