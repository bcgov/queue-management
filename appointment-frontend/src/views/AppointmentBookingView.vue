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
          edit-icon="mdi-check"
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
        <template v-if="bookingStep.code === 'location'">
          <v-card>
            <v-card-title class="justify-center">
              <h3>Location Selection</h3>
            </v-card-title>
            <v-divider class="mx-4"></v-divider>
            <LocationsList></LocationsList>
          </v-card>
        </template>

        <ServiceSelection v-if="bookingStep.code === 'service'"></ServiceSelection>

        <DateSelection v-if="bookingStep.code === 'date'"></DateSelection>

        <AppointmentSummary v-if="bookingStep.code === 'summary'"></AppointmentSummary>

        <LoginToConfirm v-if="bookingStep.code === 'login'"></LoginToConfirm>

        <!-- <v-card
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

        <v-btn text>Cancel</v-btn> -->
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script lang="ts">
import { AppointmentSummary, DateSelection, LocationsList, LoginToConfirm, ServiceSelection } from '@/components/appointment'
import { Component, Vue } from 'vue-property-decorator'

@Component({
  components: {
    AppointmentSummary,
    DateSelection,
    ServiceSelection,
    LoginToConfirm,
    LocationsList
  }
})
export default class AppointmentBookingView extends Vue {
  private stepElement = 1
  private bookingSteppers = [
    {
      step: 1,
      label: 'Select Location',
      code: 'location'
    },
    {
      step: 2,
      label: 'Select Service',
      code: 'service'
    },
    {
      step: 3,
      label: 'Select a Date',
      code: 'date'
    },
    {
      step: 4,
      label: 'Appointment Summary',
      code: 'summary'
    },
    {
      step: 5,
      label: 'Login to Confirm Appointment',
      code: 'login'
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
