<template>
  <v-card>
    <v-card-title class="justify-center">
      <h3>Appointment Summary</h3>
    </v-card-title>
    <v-divider class="mx-4"></v-divider>
    <v-card-text>
      <v-card flat color="grey lighten-4">
        <v-row class="pa-8">
          <v-col cols="12" sm="6">
            <v-label>Reason for Appointment</v-label>
            <p>{{appointmentDisplayData.serviceForAppointment}}</p>
          </v-col>
          <v-col cols="12" sm="6">
            <v-label>Date of Appointment</v-label>
            <p>{{appointmentDisplayData.appointmentDate}}</p>
          </v-col>
          <v-col cols="12">
            <v-label>Location</v-label>
            <p>{{appointmentDisplayData.locationName}}, <small v-if="appointmentDisplayData.locationAddress">{{appointmentDisplayData.locationAddress}}</small></p>
          </v-col>
          <v-col cols="12">
            <GmapMap
              :center="appointmentDisplayData.locationCoordinates"
              :zoom="14"
              class="map-view"
              :options="mapConfigurations"
            >
              <GmapMarker
                :position="appointmentDisplayData.locationCoordinates"
                :clickable="true"
                :draggable="false"
                :label='{text: appointmentDisplayData.locationName, fontWeight: "600"}'
              />
            </GmapMap>
          </v-col>
          <v-col cols="12">
            <div class="d-flex justify-center">
              <v-btn
                large
                @click="confirmAppointment"
                color="primary"
              >Confirm Appointment</v-btn>
            </div>
          </v-col>
        </v-row>
      </v-card>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import { AppointmentSlot } from '@/models/appointment'
import ConfigHelper from '@/utils/config-helper'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import StepperMixin from '@/mixins/StepperMixin.vue'

@Component({
  computed: {
    ...mapState('office', [
      'currentOffice',
      'currentService',
      'currentAppointmentSlot'
    ])
  },
  methods: {
    ...mapActions('office', [
      'createAppointment'
    ])
  }
})
export default class AppointmentSummary extends Mixins(StepperMixin) {
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private readonly currentOffice!: Office
  private readonly currentService!: Service
  private readonly currentAppointmentSlot!: AppointmentSlot
  private readonly createAppointment!: () => void
  private appointmentDisplayData = {
    serviceForAppointment: '',
    appointmentDate: '',
    locationName: ' ',
    locationAddress: '',
    locationCoordinates: {
      lat: 0,
      lng: 0
    }
  }

  private updated () {
    this.appointmentDisplayData.serviceForAppointment = this.currentService.external_service_name
    // this.appointmentDisplayData = {
    //   serviceForAppointment: this.currentService.external_service_name,
    //   appointmentDate: 'Apr 20, 2020 9:15am - 9:30am',
    //   locationName: this.currentOffice.office_name,
    //   locationAddress: this.currentOffice.civic_address,
    //   locationCoordinates: {
    //     lat: this.currentOffice.latitude,
    //     lng: this.currentOffice.longitude
    //   }
    // }
  }

  private async confirmAppointment () {
    const resp = await this.createAppointment()
    // eslint-disable-next-line no-console
    console.log(resp)
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";

.v-label {
  font-weight: 600;
  margin-bottom: 4px;
  color: $gray9 !important;
}
.map-view {
  width: 100%;
  height: 45vh;
}
</style>
