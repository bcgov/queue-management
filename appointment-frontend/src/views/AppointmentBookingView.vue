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
          <div class="step-label" v-bind:class="{'font-weight-bold': (bookingStep.step === stepCounter)}">
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
        v-for="(bookingStep) in bookingSteppers"
        :key="`${bookingStep.step}-content`"
        :step="bookingStep.step"
      >
        <v-card v-if="bookingStep.code === 'location'">
          <v-card-title class="justify-center">
            <h3>Location Selection</h3>
          </v-card-title>
          <v-divider class="mx-4"></v-divider>
          <LocationsList
            v-bind="getPropsForStep(bookingStep)"
            :key="stepCounter"
          />
        </v-card>
        <component
          v-else
          :is="bookingStep.component"
          v-bind="getPropsForStep(bookingStep)"
          keep-alive
          :key="stepCounter"
          transition="fade"
          mode="out-in"
        />
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script lang="ts">
import { AppointmentSummary, DateSelection, LocationsList, LoginToConfirm, ServiceSelection } from '@/components/appointment'
import { Component, Vue } from 'vue-property-decorator'
import { AuthModule } from '@/store/modules'
import StepperMixin from '@/mixins/StepperMixin.vue'
import { mapGetters } from 'vuex'

@Component({
  components: {
    AppointmentSummary,
    DateSelection,
    ServiceSelection,
    LoginToConfirm,
    LocationsList
  },
  computed: {
    ...mapGetters('auth', ['isAuthenticated'])
  }
})
export default class AppointmentBookingView extends Vue {
  private readonly isAuthenticated!: boolean
  private stepCounter = 1
  private updateViewCounter = 0
  private bookingSteppers = [
    {
      step: 1,
      label: 'Select Location',
      code: 'location',
      component: LocationsList,
      componentProps: {}
    },
    {
      step: 2,
      label: 'Select Service',
      code: 'service',
      component: ServiceSelection,
      componentProps: {}
    },
    {
      step: 3,
      label: 'Select a Date',
      code: 'date',
      component: DateSelection,
      componentProps: {}
    },
    {
      step: 4,
      label: 'Login to Confirm Appointment',
      code: 'login',
      component: LoginToConfirm,
      componentProps: {
        isStepperView: true
      }
    },
    {
      step: 5,
      label: 'Appointment Summary',
      code: 'summary',
      component: AppointmentSummary,
      componentProps: {}
    }
  ]

  private stepNext () {
    this.updateViewCounter++
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
    this.$store.commit('setStepperCurrentStep', this.stepCounter)
  }

  private async mounted () {
    if (this.isAuthenticated) {
      this.bookingSteppers = this.bookingSteppers.filter(step => !(step.code === 'login'))
      this.bookingSteppers[this.bookingSteppers.length - 1].step = this.bookingSteppers.length
    }
    this.stepCounter = this.$store.state.stepperCurrentStep
  }

  private getPropsForStep (step): Record<string, any> {
    return { ...step.componentProps, stepNext: this.stepNext, stepBack: this.stepBack }
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
