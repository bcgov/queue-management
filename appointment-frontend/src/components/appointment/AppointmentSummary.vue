<template>
  <div>
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
              <p>{{appointmentDateTime}}</p>
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
    <v-dialog
      v-model="dialogPopup.showDialog"
      max-width="540"
      persistent
    >
      <v-card>
        <v-card-title
          v-bind:class="{'green': dialogPopup.isSuccess, 'red': !dialogPopup.isSuccess}"
          class="lighten-3 d-block"
          primary-title
        >
          <h5 class="mb-3">
            {{dialogPopup.title}}
          </h5>
          <div class="body-2">
            {{dialogPopup.subTitle}}
          </div>
        </v-card-title>

        <v-card-text v-if="dialogPopup.isSuccess">
          <v-row>
            <v-col cols="6">
              <div class="caption">Service</div>
              <div class="body-1 font-weight-bold">{{appointmentDisplayData.serviceForAppointment}}</div>
            </v-col>
            <v-col cols="6">
              <div class="caption">Location</div>
              <div class="body-1 font-weight-bold">{{appointmentDisplayData.locationName}}</div>
            </v-col>
            <v-col cols="6">
              <div class="caption">Phone</div>
              <div class="body-1 font-weight-bold">{{appointmentDisplayData.phoneNumber}}</div>
            </v-col>
            <v-col cols="6">
              <div class="caption">Time</div>
              <div class="body-1 font-weight-bold">{{appointmentDateTime}}</div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            :color="(dialogPopup.isSuccess) ? 'success' : 'error'"
            large
            @click="clickOk"
          >
            Ok
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { Appointment, AppointmentSlot } from '@/models/appointment'
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import ConfigHelper from '@/utils/config-helper'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import StepperMixin from '@/mixins/StepperMixin.vue'
import { format } from 'date-fns'
import { utcToZonedTime } from 'date-fns-tz'

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
  private readonly createAppointment!: () => Appointment
  private dialogPopup = {
    showDialog: false,
    isSuccess: false,
    title: '',
    subTitle: ''
  }

  private get appointmentDisplayData () {
    // eslint-disable-next-line no-console
    console.log(this.currentAppointmentSlot)
    return {
      serviceForAppointment: this.currentService?.external_service_name,
      locationName: this.currentOffice?.office_name || '',
      locationAddress: this.currentOffice?.civic_address || '',
      phoneNumber: '',
      locationCoordinates: {
        lat: this.currentOffice?.latitude || 0,
        lng: this.currentOffice?.longitude || 0
      }
    }
  }

  private get appointmentDateTime () {
    let date = this.dateTimeFormatted(this.currentAppointmentSlot?.start_time, 'MMM dd, yyyy')
    let start = this.dateTimeFormatted(this.currentAppointmentSlot?.start_time, 'hh:mmaaaa')
    let end = this.dateTimeFormatted(this.currentAppointmentSlot?.end_time, 'hh:mmaaaa')
    return `${date} ${start} - ${end}`
  }

  dateTimeFormatted (date, formatStr) {
    if (!date) {
      return ''
    }
    return format(utcToZonedTime(date, 'America/Vancouver'), formatStr)
  }

  private async confirmAppointment () {
    try {
      const resp = await this.createAppointment()
      if (resp.appointment_id) {
        this.dialogPopup.showDialog = true
        this.dialogPopup.isSuccess = true
        this.dialogPopup.title = 'Success! Your appointment has been booked.'
        this.dialogPopup.subTitle = `Please review your booking in the details below.
            If you need to cancel or reschedule your appointment, please contact Service BC`
      }
    } catch (error) {
      this.dialogPopup.showDialog = true
      this.dialogPopup.isSuccess = false
      this.dialogPopup.title = 'Failed!'
      this.dialogPopup.subTitle = 'Unable to book the appointment.'
      // eslint-disable-next-line no-console
      console.log(error)
    }
  }

  private clickOk () {
    this.dialogPopup.showDialog = false
    if (this.dialogPopup.isSuccess) {
      // TODO Clear all selected states before navigating
      this.$router.push('/booked-appointments')
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
