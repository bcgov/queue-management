<template>
  <v-container :class="{'booked-appointments-mobile': $vuetify.breakpoint.xs}">
    <NoEmailAlert></NoEmailAlert>
    <v-row class="page-heading">
      <v-col cols="12" sm="6">
        <h2>My Appointments</h2>
      </v-col>
      <v-col class="book-new-btn" cols="12" sm="6">
        <v-btn
          large
          color="primary"
          @click="bookNewAppointment"
        >
          <v-icon class="mr-1">mdi-plus</v-icon>
          Book a New Appointment
        </v-btn>
      </v-col>
    </v-row>
    <v-divider class="mb-4"></v-divider>
    <v-card v-for="appointment in appointmentList" :key="appointment.appointment_id" class="my-4">
      <v-card-text>
        <v-row>
          <v-col
            cols="12"
            md="5"
          >
          <img :src="require('@/assets/img/officemaps/' + getOfficeMap(appointment))" :alt="getMapAltText(appointment)" class='static-map'>
          </v-col>
          <v-col
            cols="12"
            sm="6"
            md="4"
          >
            <p>
              <strong>Service: </strong> {{getServiceName(appointment)}}
            </p>
            <p>
              <strong>Location: </strong> {{getOfficeName(appointment)}}
            </p>
            <p>
              <strong>Date: </strong> {{appointment.appointmentDate}}
            </p>
            <p>
              <strong>Time: </strong> {{`${appointment.appointmentStartTime} - ${appointment.appointmentEndTime} `}}
            </p>
            <p class="appointment-confirmed">
              Appointment Confirmed
            </p>
          </v-col>
          <v-col
            cols="12"
            sm="6"
            md="3"
            align-self="center"
            class="text-right d-flex flex-column">
            <v-btn
              outlined
              color="primary"
              min-width="195"
              @click="changeAppointment(appointment)"
            >
              <v-icon class="mr-1">mdi-pencil-outline</v-icon>
              Change Appointment
            </v-btn>
            <v-btn
              outlined
              color="error lighten-1"
              class="mt-4"
              min-width="195"
              @click="cancelAppointment(appointment)"
            >
              <v-icon class="mr-1">mdi-delete-outline</v-icon>
              Cancel Appointment
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-alert
      v-if="!appointmentList.length"
      outlined
      color="grey darken-3"
      class="text-center mt-10"
    >
      <v-icon>mdi-information-outline</v-icon>
      No appointments found!
    </v-alert>
    <!-- Confirmation dialog -->
    <v-dialog
      v-model="confirmDialog"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
          Are you sure?
        </v-card-title>
        <v-card-text>
          Are you sure that you want to cancel this appointment?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red darken-1"
            text
            @click="confirmDelete(false)"
          >
            No
          </v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="confirmDelete(true)"
          >
            Yes, Cancel it
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { AppointmentModule, OfficeModule } from '@/store/modules'
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapMutations, mapState } from 'vuex'
import { Appointment } from '@/models/appointment'
import ConfigHelper from '@/utils/config-helper'
import { NoEmailAlert } from '@/components/common'
import { User } from '@/models/user'
import { getModule } from 'vuex-module-decorators'

@Component({
  components: {
    NoEmailAlert
  },
  computed: {
    ...mapState('auth', [
      'currentUserProfile'
    ])
  },
  methods: {
    ...mapMutations('office', [
      'setCurrentOffice',
      'setCurrentService',
      'setSPStatus'
    ]),
    ...mapActions('appointment', [
      'getAppointmentList',
      'deleteAppointment'
    ]),
    ...mapActions('office', [
      'setAppointmentValues',
      'clearSelectedValues',
      'callSnowplow'
    ])
  }
})
export default class Home extends Vue {
  private appointmentModule = getModule(AppointmentModule, this.$store)
  private officeModule = getModule(OfficeModule, this.$store)
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private confirmDialog: boolean = false
  private appointmentList: Appointment[] = []
  private selectedAppointment: Appointment = null
  private readonly callSnowplow!: (mySP: any) => any
  private readonly getAppointmentList!: () => Promise<Appointment[]>
  private readonly deleteAppointment!: (appointmentId: number) => Promise<any>
  private readonly setAppointmentValues!: (appointment: Appointment) => void
  private readonly clearSelectedValues!: () => void
  private readonly setSPStatus!: (status: string) => void
  private readonly currentUserProfile!: User

  private async beforeMount () {
    this.setSPStatus('update')
    this.$store.commit('setNonStepperLocation', 'My Appointments')
    this.fetchAppointments()
  }

  private async fetchAppointments () {
    this.appointmentList = await this.getAppointmentList()
  }

  private getCoordinates (appointment) {
    return {
      lat: appointment?.office?.latitude || 0,
      lng: appointment?.office?.longitude || 0
    }
  }

  private getOfficeName (appointment) {
    return appointment?.office?.office_name || ''
  }

  private getOfficeMap (appointment) {
    return appointment?.office?.office_number ? appointment?.office?.office_number.toString() + '.png' : '999.png'
  }

  private getServiceName (appointment) {
    return appointment?.service?.external_service_name || ''
  }

  private callsp () {
    (window as any).snowplow('trackPageView')
  }

  private goToAccountSettings () {
    this.$router.push('/account-settings')
    this.callsp()
  }

  private bookNewAppointment () {
    this.clearSelectedValues()
    this.$router.push('/appointment')
    this.callsp()
  }

  private changeAppointment (appointment) {
    const mySP = { step: 'Change Appointment', loggedIn: true, apptID: appointment.appointment_id, clientID: this.currentUserProfile?.user_id, loc: appointment.office.office_name, serv: appointment.service.external_service_name }
    this.callSnowplow(mySP)
    this.setAppointmentValues(appointment)
    this.$store.commit('setStepperCurrentStep', 3)
    this.$store.commit('setAppointmentEditMode', true)
    this.$router.push('/appointment')
    this.callsp()
  }

  private cancelAppointment (appointment) {
    const mySP = { step: 'Cancel Appointment', loggedIn: true, apptID: appointment.appointment_id, clientID: this.currentUserProfile?.user_id, loc: appointment.office.office_name, serv: appointment.service.external_service_name }
    this.callSnowplow(mySP)
    this.confirmDialog = true
    this.selectedAppointment = appointment
  }

  private async confirmDelete (isAgree: boolean) {
    if (isAgree) {
      const resp = await this.deleteAppointment(this.selectedAppointment?.appointment_id)
      if (resp?.status === 204) {
        this.confirmDialog = false
      }
      this.fetchAppointments()
    } else {
      this.confirmDialog = false
    }
  }

  /* private getMapUrl (appointment) {
    if (!appointment.office) { return '' }
    return GeocoderService.generateStaticMapURL(appointment.office)
  } */

  private getMapAltText (appointment) {
    return appointment?.office?.civic_address || 'No address'
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.map-view {
  width: 100%;
  height: 180px;
}
.appointment-confirmed {
  font-weight: 600;
  color: $BCgovInputSuccess;
}
.book-new-btn {
  text-align: right;
}
.static-map {
  max-width: 100%;
}
.booked-appointments-mobile {
  .page-heading {
    margin-top: -1rem;
    text-align: center !important;
    .book-new-btn {
      padding-top: 0;
      text-align: center;
    }
  }
  .appointment-confirmed {
    margin-bottom: 0;
  }
}
</style>
