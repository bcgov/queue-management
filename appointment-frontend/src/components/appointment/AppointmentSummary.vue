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
            <p>{{appointmentData.reasonForAppointment}}</p>
          </v-col>
          <v-col cols="12" sm="6">
            <v-label>Date of Appointment</v-label>
            <p>{{appointmentData.appointmentDate}}</p>
          </v-col>
          <v-col cols="12">
            <v-label>Location</v-label>
            <p>{{appointmentData.locationName}}, <small>{{appointmentData.locationAddress}}</small></p>
          </v-col>
          <v-col cols="12">
            <GmapMap
              :center="appointmentData.coordinates"
              :zoom="14"
              class="map-view"
              :options="mapConfigurations"
            >
              <GmapMarker
                :position="appointmentData.coordinates"
                :clickable="true"
                :draggable="false"
                :label='{text: appointmentData.locationName, fontWeight: "600"}'
              />
            </GmapMap>
          </v-col>
          <v-col cols="12">
            <div class="d-flex justify-center">
              <v-btn large color="primary">Confirm Appointment</v-btn>
            </div>
          </v-col>
        </v-row>
      </v-card>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import ConfigHelper from '@/utils/config-helper'

@Component
export default class AppointmentSummary extends Vue {
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private appointmentData = {
    reasonForAppointment: 'Legal Name Change',
    appointmentDate: 'Apr 20, 2020 9:15am - 9:30am',
    locationName: 'Service BC Centre Victoria(Gateway Village)',
    locationAddress: '4000 Seymour Pl, Victoria, BC V8X 4S7',
    coordinates: {
      lat: 48.452540,
      lng: -123.369040
    }
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
