<template>
  <v-stepper
    v-model="stepCounter"
    alt-labels
  >
    <v-stepper-header>
      <template v-for="bookingStep in bookingSteppers">
        <v-stepper-step
          :key="`${bookingStep.step}-step`"
          :complete="stepCounter > bookingStep.step"
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
            <LocationsList
              :stepNext="stepNext"
              :stepBack="stepBack"
            />
          </v-card>
        </template>
        <template>
          <component
            :is="bookingStep.component"
            :stepNext="stepNext"
            :stepBack="stepBack"
            keep-alive
            transition="fade"
            mode="out-in"
          />
        </template>

      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script lang="ts">
import { AppointmentSummary, DateSelection, LocationsList, LoginToConfirm, ServiceSelection } from '@/components/appointment'
import { Component, Vue } from 'vue-property-decorator'
import StepperMixin from '@/mixins/StepperMixin.vue'

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
  private stepCounter = 1
  private bookingSteppers = [
    {
      step: 1,
      label: 'Select Location',
      code: 'location',
      component: LocationsList
    },
    {
      step: 2,
      label: 'Select Service',
      code: 'service',
      component: ServiceSelection
    },
    {
      step: 3,
      label: 'Select a Date',
      code: 'date',
      component: DateSelection
    },
    {
      step: 4,
      label: 'Login to Confirm Appointment',
      code: 'login',
      component: LoginToConfirm
    },
    {
      step: 5,
      label: 'Appointment Summary',
      code: 'summary',
      component: AppointmentSummary
    }
  ]

  private stepNext () {
    if (this.stepCounter < this.bookingSteppers.length) {
      this.stepCounter++
    } else {
      this.stepCounter = 1
    }
  }

  private stepBack () {
    if (this.stepCounter !== 1) {
      this.stepCounter--
    }
  }

  private async updated () {
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.step-label {
  text-align: center;
  line-height: 1.25;
}
</style>
