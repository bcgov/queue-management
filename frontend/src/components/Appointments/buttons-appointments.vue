<template>
  <b-container>
    <div class="full-div">
      <div>
        <form inline>
          <b-button class="btn-primary mx-2" @click="today">Today</b-button>
          <b-button class="btn-primary mx-2" v-if="toggleAppCalenderView" @click="agendaWeek">Week View</b-button>
          <b-button class="btn-primary mx-2" v-if="!toggleAppCalenderView" @click="agendaDay"> Day View</b-button>
          <b-button
            variant="primary"
            class="ml-0 mx-2"
            @click="clickBlackout"
            >Create Blackout</b-button
          >
          <b-button
      variant="primary"
      class="ml-0 mx-2 fl-right"
      @click="clickNewApp"
      >
      <font-awesome-icon
        icon="plus"
        class="m-0 p-0"
        style="font-size: 1rem"
    />
      New Appointment
    </b-button>
        </form>
      </div>
      <div class="align-center-text">
        <span class="q-inline-title">
          {{ calendar_setup.title }}
          {{ calendar_setup.titleRef && calendar_setup.titleRef.title }}
        </span>
      </div>
      <div class="align-center-arrow">
          <b-button class="btn-primary" @click="prev">
            <font-awesome-icon
              icon="angle-left"
              class="m-0 p-0"
              style="font-size: 1rem"
          /> Last</b-button>
          <b-button class="btn-primary ml-1" @click="next">
            Next
            <font-awesome-icon
              icon="angle-right"
              class="m-0 p-0"
              style="font-size: 1rem"
          /></b-button>
      </div>
    </div>
  </b-container>
</template>

<script lang="ts">
/* eslint-disable */
import { Component, Vue } from 'vue-property-decorator'
import { namespace } from 'vuex-class'

import ApptBookingModal from './appt-booking-modal/appt-booking-modal.vue'

const appointmentsModule = namespace('appointmentsModule')

@Component({
  components: {
    ApptBookingModal
  }
})
export default class ButtonsAppointments extends Vue {
  @appointmentsModule.State('showAppointmentBlackoutModal') private showAppointmentBlackoutModal!: any
  @appointmentsModule.Getter('calendar_setup') private calendar_setup!: any;
  // @appointmentsModule.Getter('is_GA') private is_GA!: any;
  @appointmentsModule.Getter('is_Support') private is_Support!: any;

  @appointmentsModule.Action('beginAppointment') public beginAppointment: any

  @appointmentsModule.Mutation('toggleApptBlackoutModal') public toggleApptBlackoutModal: any
  @appointmentsModule.Mutation('toggleAppointmentBlackoutModal') public toggleAppointmentBlackoutModal: any

  @appointmentsModule.State('clickedAppt') public clickedAppt: any
  @appointmentsModule.Mutation('setAgendaClickedAppt') public setAgendaClickedAppt: any

  @appointmentsModule.State('clickedTime') public clickedTime: any
  @appointmentsModule.Mutation('setAgendaClickedTime') public setAgendaClickedTime: any
  @appointmentsModule.Mutation('toggleApptBookingModal') public toggleApptBookingModal: any

  
  @appointmentsModule.State('toggleAppCalenderView') public toggleAppCalenderView: any
  @appointmentsModule.Mutation('setToggleAppCalenderView') public setToggleAppCalenderView: any

  get dropdownText () {
    if (this.calendar_setup.name === 'day') {
      return 'Day View'
    }
    if (this.calendar_setup.name === 'week') {
      return 'Week View'
    }
    return 'Week View'
  }

  agendaDay () {
    this.$root.$emit('agendaDay')
    this.setToggleAppCalenderView(true)
  }

  agendaWeek () {
    this.$root.$emit('agendaWeek')
    this.setToggleAppCalenderView(false)
  }

  next () {
    this.$root.$emit('next')
  }

  prev () {
    this.$root.$emit('prev')
  }

  today () {
    this.$root.$emit('today')
  }

  clickBlackout () {
    this.toggleAppointmentBlackoutModal(true)
  }

  clickNewApp () {
    this.setAgendaClickedTime(null)
    this.setAgendaClickedAppt(null)
    this.toggleApptBookingModal(true)
  }
}
</script>
<style scoped>
.align-center-text {
  padding-left: 40%;
  margin-top: -46px;
}​
.full-div {
  width: 100%;
}
.align-center-arrow { 
  padding-left: 48%;
}
.fl-right{
  float: right;
}
</style>
