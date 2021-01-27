<template>
  <v-stepper
    v-model="stepCounter"
    alt-labels
    :class="{'stepper-mobile': $vuetify.breakpoint.xs}"
  >
    <v-stepper-header>
      <template v-for="bookingStep in bookingSteppers">
        <v-stepper-step
          :key="`${bookingStep.step}-step`"
          :complete="stepCounter > bookingStep.step"
          :step="bookingStep.step"
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
        <v-card>
          <v-card-title class='flex-column flex-sm-row'>
            <v-btn
              text
              large
              @click="stepBack"
              v-if="showBackButton(bookingStep)"
              class="stepper-back-button"
            >
              <v-icon left class="mr-1">mdi-arrow-left</v-icon>
              {{(!$vuetify.breakpoint.xs) ? 'Back' : ''}}
            </v-btn>
            <v-spacer></v-spacer>
            <h3
              :class="{'mobile-step-title': (bookingStep.code === 'summary')}"
            >{{bookingStep.title}}</h3>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-divider class="mx-4"></v-divider>
          <p v-if="bookingStep.subTitle" class="step-desc mt-2">{{bookingStep.subTitle}}
          </p>
          <p v-if="bookingStep.beforeIconText|| bookingStep.afterIconText" class="step-desc mt-2">
            {{bookingStep.beforeIconText}}
            <v-btn
                class="ma-2"
                text
                icon
                color="red lighten-2"
                @click="fetchCurrentLocation()"
            >
              <v-icon v-if="bookingStep.icon"
                    large
                    color="blue darken-2"
                  >
                {{bookingStep.icon}}
              </v-icon>
            </v-btn>
            {{bookingStep.afterIconText}}
          </p>
          <component
            :is="bookingStep.component"
            v-bind="getPropsForStep(bookingStep)"
            keep-alive
            :key="stepCounter"
            transition="fade"
            mode="out-in"
          />
        </v-card>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script lang="ts">
import { AppointmentSummary, DateSelection, LocationsList, LoginToConfirm, ServiceSelection } from '@/components/appointment'
import { Component, Vue } from 'vue-property-decorator'
import { GeolocatorSuccess, LatLng } from '@/models/geo'
import { locationBus, locationBusEvents } from '@/events/locationBus'
import { mapActions, mapGetters } from 'vuex'
import { AuthModule } from '@/store/modules'
import StepperMixin from '@/mixins/StepperMixin.vue'

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
  },
  methods: {
    ...mapActions('geo', [
      'getCurrentLocation'
    ])
  }
})

export default class AppointmentBookingView extends Vue {
  private readonly isAuthenticated!: boolean
  private stepCounter = 1
  private updateViewCounter = 0
  private readonly getCurrentLocation!: () => Promise<GeolocatorSuccess>
  private bookingSteppers = [
    {
      step: 1,
      label: 'Location Selection',
      title: 'Book an Appointment',
      subTitle: '',
      icon: 'mdi-map-marker-radius',
      beforeIconText: `Click the`,
      afterIconText: `to find your closest Service BC Centre`,
      code: 'location',
      component: LocationsList,
      componentProps: {}
    },
    {
      step: 2,
      label: 'Select Service',
      title: 'Service Selection',
      subTitle: `Please select the service you'd like to receive`,
      code: 'service',
      component: ServiceSelection,
      componentProps: {}
    },
    {
      step: 3,
      label: 'Select Date',
      title: 'Select a Date',
      subTitle: `What day would you like to have the appointment?`,
      code: 'date',
      component: DateSelection,
      componentProps: {}
    },
    {
      step: 4,
      label: 'Login to Confirm Appointment',
      title: 'Login',
      subTitle: `To complete your appointment booking, please login using one of the following`,
      code: 'login',
      component: LoginToConfirm,
      componentProps: {
        isStepperView: true
      }
    },
    {
      step: 5,
      label: 'Appointment Summary',
      title: 'Appointment Summary',
      subTitle: '',
      code: 'summary',
      component: AppointmentSummary,
      componentProps: {}
    }
  ]

  private showBackButton (bookingStep) {
    if (bookingStep.step <= 1) {
      return false
    } else if (bookingStep.step === 3 && this.$store.state.isAppointmentEditMode) {
      return false
    }
    return true
  }

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
    /**  NOTE: isOnCurrentStep is used to identify the stepper view loaded is in the current step, and execute the steps inside mounted.
     * otherwise, mounted cycle of all views will executed during a step change
    */
    return { ...step.componentProps, stepNext: this.stepNext, stepBack: this.stepBack, isOnCurrentStep: this.isOnCurrentStep(step) }
  }

  private isOnCurrentStep (step) {
    return !!(step.step === this.stepCounter)
  }

  private async fetchCurrentLocation () {
    locationBus.$emit(locationBusEvents.ClosestLocationEvent)
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.step-label {
  text-align: center;
  line-height: 1.25;
}
.step-desc {
  text-align: center!important;
  font-size: 1rem!important;
  letter-spacing: .009375em!important;
  line-height: 1.75rem;
  color: $gray7;
}
.stepper-back-button {
  position: absolute;
  left: 0;
  top: 10px;
}
.stepper-mobile {
  .v-stepper__content {
    padding: 4px;
    .step-desc {
      padding: 0 16px;
      margin-bottom: 0;
    }
  }
  .v-stepper__step {
    padding: 12px;
    .v-stepper__step__step {
      margin-bottom: 3px;
    }
  }
  .v-stepper__header {
    flex-wrap: nowrap; // For super small mobile <340px;
    .v-divider {
      margin-top: 23px;
    }
  }
  .mobile-step-title {
    font-size: 1.25rem;
  }
}
</style>
