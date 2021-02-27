<template>
  <fragment>
    <div class="d-flex butttons-appointments">
      <div>
        <form inline>
          <b-button class="btn-primary" @click="prev">
            <font-awesome-icon
              icon="angle-left"
              class="m-0 p-0"
              style="font-size: 1rem"
          /></b-button>
          <b-button class="btn-primary ml-1" @click="next">
            <font-awesome-icon
              icon="angle-right"
              class="m-0 p-0"
              style="font-size: 1rem"
          /></b-button>
          <b-button class="btn-primary mx-2" @click="today">Today</b-button>
          <b-dropdown variant="primary" class="mr-2" :text="dropdownText">
            <b-dropdown-item @click="agendaWeek"> Week View </b-dropdown-item>
            <b-dropdown-item @click="agendaDay"> Day View </b-dropdown-item>
          </b-dropdown>
          <b-button
            variant="primary"
            class="ml-0"
            @click="clickBlackout"
            >Create Blackout</b-button
          >
        </form>
      </div>
      <div>
        <span class="q-inline-title">
          {{ calendar_setup.title }}
          {{ calendar_setup.titleRef && calendar_setup.titleRef.title }}
        </span>
      </div>
    </div>
  </fragment>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import { namespace } from 'vuex-class'

const appointmentsModule = namespace('appointmentsModule')

@Component
export default class ButtonsAppointments extends Vue {
  @appointmentsModule.State('showAppointmentBlackoutModal') private showAppointmentBlackoutModal!: any
  @appointmentsModule.Getter('calendar_setup') private calendar_setup!: any;
  // @appointmentsModule.Getter('is_GA') private is_GA!: any;
  @appointmentsModule.Getter('is_Support') private is_Support!: any;

  @appointmentsModule.Action('beginAppointment') public beginAppointment: any

  @appointmentsModule.Mutation('toggleApptBlackoutModal') public toggleApptBlackoutModal: any
  @appointmentsModule.Mutation('toggleAppointmentBlackoutModal') public toggleAppointmentBlackoutModal: any

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
  }

  agendaWeek () {
    this.$root.$emit('agendaWeek')
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
}
</script>
<style scoped>
.butttons-appointments {
  margin-right: auto;
}
</style>
