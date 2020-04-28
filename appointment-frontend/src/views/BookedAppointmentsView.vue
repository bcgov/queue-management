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
    <v-card v-for="booking in bookingData" :key="booking.id" class="my-4">
      <v-card-text>
        <v-row>
          <v-col
            cols="12"
            sm="5"
          >
            <GmapMap
              :center="booking.coordinates"
              :zoom="14"
              class="map-view"
              :options="mapConfigurations"
            >
              <GmapMarker
                :position="booking.coordinates"
                :clickable="true"
                :draggable="false"
                :label='{text: booking.locationName, fontWeight: "600"}'
              />
            </GmapMap>
          </v-col>
          <v-col
            cols="6"
            sm="4"
          >
            <p>
              <strong>Service: </strong> {{booking.serviceName}}
            </p>
            <p>
              <strong>Location: </strong> {{booking.locationName}}
            </p>
            <p>
              <strong>Date: </strong> {{booking.bookingDate}}
            </p>
            <p>
              <strong>Time: </strong> {{booking.bookingTime}}
            </p>
            <p class="appointment-confirmed" v-if="booking.isAppointmentConfirmed">
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
              min-width="180"
            >
              Change Appointment
            </v-btn>
            <v-btn
              text
              color="error lighten-1"
              class="mt-4"
              min-width="180"
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
import { Appointment } from '@/models/appointment'
import { AppointmentModule } from '@/store/modules'
import ConfigHelper from '@/utils/config-helper'
import { mapActions } from 'vuex'

@Component({
  components: {
  },
  methods: {
    ...mapActions('appointment', [
      'getAppointmentList'
    ])
  }
})
export default class Home extends Vue {
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private showEmailAlert: boolean = true

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
