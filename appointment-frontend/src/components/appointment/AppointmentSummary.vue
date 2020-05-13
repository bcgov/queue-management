<template>
  <div :class="{'summary-mobile': $vuetify.breakpoint.xs}">
    <v-card>
      <v-divider class="mx-4"></v-divider>
      <v-card-text>
        <v-card flat color="grey lighten-4">
          <v-row class="pa-8 summary-grid">
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
              <div class="d-flex justify-center">
                <v-checkbox
                  v-model="termsOfServiceConsent"
                >
                  <template v-slot:label>
                    <div>
                      I agree to the <span class='clickable-link' @click.stop.prevent='openToS'>Terms of Service</span>
                    </div>
                  </template>
                </v-checkbox>
              </div>
              <div class="d-flex justify-center">
                <v-btn
                  large
                  @click="confirmAppointment"
                  :disabled="!termsOfServiceConsent"
                  :loading="isLoading"
                  color="primary"
                >{{submitBtnText}}</v-btn>
              </div>
            </v-col>
            <v-col cols="12">
              <img :src='getMapUrl(staticMapData)' :alt="staticMapData.civic_address" class='map-view'>
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
          <v-row>
            <NoEmailAlert></NoEmailAlert>
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
    <terms-of-service-popup ref='TermsOfServicePopup'></terms-of-service-popup>
  </div>
</template>

<script lang="ts">
import { Appointment, AppointmentSlot } from '@/models/appointment'
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'
import { AuthModule } from '@/store/modules'
import CommonUtils from '@/utils/common-util'
import ConfigHelper from '@/utils/config-helper'
import GeocoderService from '@/services/geocoder.services'
import { NoEmailAlert } from '@/components/common'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import StepperMixin from '@/mixins/StepperMixin.vue'
import TermsOfServicePopup from './TermsOfServicePopup.vue'
import { User } from '@/models/user'
import { getModule } from 'vuex-module-decorators'

@Component({
  computed: {
    ...mapState('office', [
      'currentOffice',
      'currentService',
      'currentAppointmentSlot',
      'currentOfficeTimezone'
    ]),
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  methods: {
    ...mapActions('office', [
      'createAppointment',
      'clearSelectedValues'
    ])
  },
  components: {
    TermsOfServicePopup,
    NoEmailAlert
  }
})
export default class AppointmentSummary extends Mixins(StepperMixin) {
  private authModule = getModule(AuthModule, this.$store)
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private readonly currentOffice!: Office
  private readonly currentService!: Service
  private readonly currentAppointmentSlot!: AppointmentSlot
  private readonly currentOfficeTimezone!: string
  private readonly createAppointment!: () => Appointment
  private readonly clearSelectedValues!: () => void
  private readonly isAuthenticated!: boolean
  private showTermsOfServiceModal: boolean = false
  private termsOfServiceConsent: boolean = false
  private isLoading: boolean = false
  private dialogPopup = {
    showDialog: false,
    isSuccess: false,
    title: '',
    subTitle: ''
  }

  private get appointmentDisplayData () {
    return {
      serviceForAppointment: this.currentService?.external_service_name,
      locationName: this.currentOffice?.office_name || '',
      locationAddress: this.currentOffice?.civic_address || '',
      phoneNumber: this.currentOffice?.telephone,
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

  private get submitBtnText () {
    return (this.$store.state.isAppointmentEditMode) ? 'Update Appointment' : 'Confirm Appointment'
  }

  private get staticMapData () {
    return {
      civic_address: this.currentOffice?.civic_address || '',
      latitude: this.currentOffice?.latitude || 0,
      longitude: this.currentOffice?.longitude || 0
    }
  }

  dateTimeFormatted (date, formatStr) {
    if (!date) {
      return ''
    }
    return CommonUtils.getTzFormattedDate(date, this.currentOfficeTimezone, formatStr)
  }

  private async confirmAppointment () {
    this.isLoading = true
    try {
      const resp = await this.createAppointment()
      if (resp.appointment_id) {
        this.dialogPopup.showDialog = true
        this.dialogPopup.isSuccess = true
        this.dialogPopup.title = 'Success! Your appointment has been booked.'
        this.dialogPopup.subTitle = `Please review your booking in the details below.
            If you need to cancel or reschedule your appointment, please contact Service BC`
      }
      this.isLoading = false
    } catch (error) {
      this.isLoading = false
      this.dialogPopup.showDialog = true
      this.dialogPopup.isSuccess = false
      this.dialogPopup.title = 'Failed!'
      this.dialogPopup.subTitle = error?.response?.data?.message || 'Unable to book the appointment.'
    }
  }

  private clickOk () {
    this.dialogPopup.showDialog = false
    if (this.dialogPopup.isSuccess) {
      this.clearSelectedValues()
      this.$router.push('/booked-appointments')
    }
  }

  private getMapUrl (location) {
    return GeocoderService.generateStaticMapURL(location, { height: 200, width: 1200, scale: 2 })
  }

  private openToS () {
    (this.$refs.TermsOfServicePopup as TermsOfServicePopup).open()
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
  max-width: 100%;
  max-height: 100%
}
.clickable-link {
  text-decoration: underline;
  color: $BCgovBlue5;
  cursor: pointer;
}
.summary-mobile {
  .summary-grid {
    p {
      margin-bottom: 0;
    }
  }
}
</style>
