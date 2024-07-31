<template>
  <b-container>
    <div class="row">
      <div class="col-5">
        <form inline>
          <b-button class="btn-primary mx-2" @click="today">Today</b-button>
          <b-button class="btn-primary mx-2" v-if="toggleAppCalenderView" @click="agendaWeek">Week View</b-button>
          <b-button class="btn-primary mx-2" v-if="!toggleAppCalenderView" @click="agendaDay"> Day View</b-button>
          <b-button variant="primary" class="ml-0 mx-2" v-if="csrOfficeEqualSelectedOffice" @click="clickBlackout">Create Blackout</b-button>
        </form>
      </div>
      <div class="col-1">
        <label class="mb-0">Select Office</label>
      </div>
      <div class="col-3">
        <b-form-select  :value="selected_office_id" :options="officeList" @change="onChangeOffice">
        </b-form-select>
      </div>
      <div class="col-3">
        <b-button variant="primary" class="ml-0 mx-2 fl-right" @click="clickNewApp">
          <font-awesome-icon icon="plus" class="m-0 p-0" style="font-size: 1rem" />
          New Appointment
        </b-button>
      </div>
    </div>
    <div class="row" style="text-align: center;">
      <span class="col-12 q-inline-title">
        {{ calendar_setup.title }}
        {{ calendar_setup.titleRef && calendar_setup.titleRef.title }}
      </span>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="align-center-arrow">
          <b-button class="btn-primary" @click="prev">
            <font-awesome-icon icon="angle-left" class="m-0 p-0" style="font-size: 1rem" /> Last</b-button>
          <b-button class="btn-primary ml-1" @click="next">
            Next
            <font-awesome-icon icon="angle-right" class="m-0 p-0" style="font-size: 1rem" /></b-button>
        </div>
      </div>
    </div>
  </b-container>
</template>

<script lang="ts">
/* eslint-disable */
import { Component, Vue } from 'vue-property-decorator'
import { namespace, State } from 'vuex-class'

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

  @appointmentsModule.Getter('getSelectedOfficeId') public selected_office_id!: any;
  @appointmentsModule.Mutation('setAppointmentsOfficeId') public setAppointmentsOfficeId: any
  @appointmentsModule.Action('getAppointments') private getAppointments: any;
  @State('offices') private offices!: any;
  get csrOfficeEqualSelectedOffice () {
    return this.$store.state.user.office.office_id === this.selected_office_id;
  }
  get dropdownText() {
    if (this.calendar_setup.name === 'day') {
      return 'Day View'
    }
    if (this.calendar_setup.name === 'week') {
      return 'Week View'
    }
    return 'Week View'
  }

  agendaDay() {
    this.$root.$emit('agendaDay')
    this.setToggleAppCalenderView(true)
  }

  agendaWeek() {
    this.$root.$emit('agendaWeek')
    this.setToggleAppCalenderView(false)
  }

  next() {
    this.$root.$emit('next')
  }

  prev() {
    this.$root.$emit('prev')
  }

  today() {
    this.$root.$emit('today')
  }

  clickBlackout() {
    this.toggleAppointmentBlackoutModal(true)
  }

  clickNewApp() {
    this.setAgendaClickedTime(null)
    this.setAgendaClickedAppt(null)
    this.toggleApptBookingModal(true)
  }
  get officeList() {
    return this.offices.map(p => ({ text: p.office_name, value: p.office_id }))
  }
  onChangeOffice(office_id) {
    this.setAppointmentsOfficeId(office_id)
    this.getAppointments();
  }
  mounted(){
    this.setAppointmentsOfficeId(this.$store.state.user.office_id)
    this.getAppointments();
    console.log("Onload Office Id ", this.selected_office_id);
  }
}
</script>

<style scoped>
.align-center-text {
  padding-left: 40%;
  margin-top: -46px;
}

.full-div {
  width: 100%;
}

.align-center-arrow {
  padding-left: 48%;
}

.fl-right {
  float: right;
}
</style>
