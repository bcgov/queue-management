<template>
  <div>
    <v-alert
      v-model="showEmailAlert"
      border="left"
      type="warning"
      close-text="Close Alert"
      color="warning"
      icon="mdi-alert-circle-outline"
      dense
      dismissible
    >
      Please <span class="clickable" @click="goToAccountSettings">configure your email address</span> to receive notifications
    </v-alert>
    <v-row>
      <v-col>
        <h2>Your Appointments</h2>
      </v-col>
      <v-col class="text-right">
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
            sm="5"
          >
            <GmapMap
              :center="getCoordinates(appointment)"
              :zoom="14"
              class="map-view"
              :options="mapConfigurations"
            >
              <GmapMarker
                :position="getCoordinates(appointment)"
                :clickable="true"
                :draggable="false"
                :label='{text: getOfficeName(appointment), fontWeight: "600"}'
              />
            </GmapMap>
          </v-col>
          <v-col
            cols="6"
            sm="4"
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
            cols="6"
            sm="3"
            align-self="center"
            class="text-right">
            <v-btn
              outlined
              color="primary"
              min-width="195"
            >
              <v-icon class="mr-1">mdi-pencil-outline</v-icon>
              Change Appointment
            </v-btn>
            <v-btn
              outlined
              color="error lighten-1"
              class="mt-4"
              min-width="195"
            >
              <v-icon class="mr-1">mdi-delete-outline</v-icon>
              Cancel Appointment
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import { Appointment } from '@/models/appointment'
import { AppointmentModule } from '@/store/modules'
import ConfigHelper from '@/utils/config-helper'
import { User } from '@/models/user'
import { getModule } from 'vuex-module-decorators'

@Component({
  computed: {
    ...mapState('auth', [
      'currentUserProfile'
    ])
  },
  methods: {
    ...mapActions('appointment', [
      'getAppointmentList'
    ])
  }
})
export default class Home extends Vue {
  private officeModule = getModule(AppointmentModule, this.$store)
  private readonly currentUserProfile!: User
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private showEmailAlert: boolean = false

  private readonly getAppointmentList!: () => Promise<Appointment[]>
  private appointmentList: Appointment[] = []

  private bookingData = [
    {
      id: 1,
      locationName: 'Service BC Victoria',
      coordinates: {
        lat: 48.452540,
        lng: -123.369040
      },
      serviceName: 'Legal Name Change',
      bookingDate: 'Apr 20, 2020',
      bookingTime: '9:15 am',
      isAppointmentConfirmed: true
    },
    {
      id: 2,
      locationName: 'Service BC Langford',
      coordinates: {
        lat: 48.452540,
        lng: -123.369040
      },
      serviceName: 'Legal Name Change',
      bookingDate: 'Apr 22, 2020',
      bookingTime: '10:45 am',
      isAppointmentConfirmed: false
    }
  ]

  private async beforeMount () {
    this.appointmentList = await this.getAppointmentList()
    // eslint-disable-next-line no-console
    console.log(this.appointmentList)
    this.showEmailAlert = !this.currentUserProfile?.email
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

  private getServiceName (appointment) {
    return appointment?.service?.external_service_name || ''
  }

  private goToAccountSettings () {
    this.$router.push('/account-settings')
  }

  private bookNewAppointment () {
    this.$router.push('/appointment')
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
.clickable {
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
}
</style>
