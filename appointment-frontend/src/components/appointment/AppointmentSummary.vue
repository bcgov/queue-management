<template>
  <div :class="{'summary-mobile': $vuetify.breakpoint.xs}">
    <v-card>
      <v-divider class="mx-4"></v-divider>
      <v-card-text>
        <v-card flat color="grey lighten-4">
          <v-row class="pt-0 pa-4 summary-grid">
            <v-col cols="12">
              <div class="d-flex justify-center">
                <v-checkbox
                  v-model="termsOfServiceConsent"
                  data-cy="step-5-checkbox-consent"
                >
                  <template v-slot:label>
                    <div>
                      I agree to the <span class='clickable-link' @click.stop.prevent='openToS'>Terms of Use</span>
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
                  data-cy="step-5-button-confirm"
                >{{submitBtnText}}</v-btn>
              </div>
            </v-col>
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
              <p>{{appointmentDisplayData.locationName}}</p>
            </v-col>
            <v-col cols="3"></v-col>
            <v-col cols="12" md="6" class="text-center">
              <div>
                <v-switch v-if="currentUserProfile && currentUserProfile.telephone && !currentUserProfile.sendSmsReminders"
                  inset
                  v-model="isSendSmsReminders"
                  label="Send me appointment reminders via SMS text message"
                ></v-switch>
              </div>
              <div>
                <v-switch v-if="currentUserProfile && currentUserProfile.email && !currentUserProfile.sendEmailReminders"
                    inset
                    v-model="isSendEmailReminders"
                    label="Send me appointment reminders via email"
                  ></v-switch>
              </div>
            </v-col>
            <v-col cols="12">
              <template v-if='staticMapData.externalMapLink'>
                    <a class='link-w-icon mt-6' v-bind:href='staticMapData.externalMapLink' target="_blank" rel="noopener noreferrer" :alt='`Open link for ${ staticMapData.civicAddress}`'>
                      <img :src="require('@/assets/img/officemaps/' + staticMapData.officeNumber)" :alt="staticMapData.civicAddress" class='map-view'>
                    </a>
                  </template>
                  <template v-else><img
                    :src="require('@/assets/img/officemaps/' + staticMapData.officeNumber)"
                    :alt="staticMapData.civicAddress"
                    class='map-view'
                    data-cy="step-5-image-map"
                  ></template>
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
      <v-card data-cy="step-5-dialog-appointment">
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
            <v-col cols="12">
              <NoEmailAlert></NoEmailAlert>
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

          <v-btn
            large
            v-if="(dialogPopup.isSuccess === false) && (!anyActiveDLKT)"
            color="default"
            @click="goToTime"
          >
            Pick another time
          </v-btn>

          <v-btn
            large
            v-if="(dialogPopup.isSuccess === false) && (anyActiveDLKT)"
            color="default"
            @click="goToMyAppointments"
          >
            My Appointments
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
import { AppointmentModule, AuthModule } from '@/store/modules'
import { Component, Mixins } from 'vue-property-decorator'
import { User, UserUpdateBody } from '@/models/user'
import { mapActions, mapGetters, mapState } from 'vuex'
import CommonUtils from '@/utils/common-util'
import ConfigHelper from '@/utils/config-helper'
import { NoEmailAlert } from '@/components/common'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import StepperMixin from '@/mixins/StepperMixin.vue'
import TermsOfServicePopup from './TermsOfServicePopup.vue'
import { getModule } from 'vuex-module-decorators'

@Component({
  computed: {
    ...mapState('office', [
      'currentOffice',
      'currentService',
      'currentAppointmentSlot',
      'currentOfficeTimezone'
    ]),
    ...mapState('auth', ['currentUserProfile']),
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  methods: {
    ...mapActions('office', [
      'createAppointment',
      'clearSelectedValues',
      'deleteDraftAppointment',
      'callSnowplow'
    ]),
    ...mapActions('appointment', [
      'getAppointmentList'
    ]),
    ...mapActions('account', ['updateUserAccount'])
  },
  components: {
    TermsOfServicePopup,
    NoEmailAlert
  }
})
export default class AppointmentSummary extends Mixins(StepperMixin) {
  private appointmentModule = getModule(AppointmentModule, this.$store)
  private authModule = getModule(AuthModule, this.$store)
  private mapConfigurations = ConfigHelper.getMapConfigurations()
  private readonly currentOffice!: Office
  private readonly currentService!: Service
  private readonly currentUserProfile!: User
  private readonly currentAppointmentSlot!: AppointmentSlot
  private readonly currentOfficeTimezone!: string
  private readonly createAppointment!: () => Appointment
  private readonly deleteDraftAppointment!: () => Appointment
  private readonly clearSelectedValues!: () => void
  private readonly callSnowplow!: (mySP: any) => any
  private readonly isAuthenticated!: boolean
  private showTermsOfServiceModal: boolean = false
  private termsOfServiceConsent: boolean = false
  private isLoading: boolean = false
  private anyActiveDLKT: boolean = false
  private myappointmentList: Appointment[] = []
  private readonly getAppointmentList!: () => Promise<Appointment[]>
  private dialogPopup = {
    showDialog: false,
    isSuccess: false,
    title: '',
    subTitle: ''
  }

  private isSendSmsReminders:boolean = false
  private isSendEmailReminders:boolean = false
  private readonly updateUserAccount!: (userBody: UserUpdateBody) => Promise<any>

  private async mounted () {
    if (this.isAuthenticated) {
      await this.fetchUserAppointments()
    }
  }

  private get appointmentDisplayData () {
    return {
      serviceForAppointment: this.currentService?.externalServiceName,
      locationName: this.currentOffice?.officeName || '',
      locationAddress: this.currentOffice?.civicAddress || '',
      phoneNumber: this.currentOffice?.telephone,
      locationCoordinates: {
        lat: this.currentOffice?.latitude || 0,
        lng: this.currentOffice?.longitude || 0
      }
    }
  }

  private get appointmentDateTime () {
    const date = this.dateTimeFormatted(this.currentAppointmentSlot?.startTime, 'MMM dd, yyyy')
    const start = this.dateTimeFormatted(this.currentAppointmentSlot?.startTime, 'hh:mmaaaa')
    const end = this.dateTimeFormatted(this.currentAppointmentSlot?.endTime, 'hh:mmaaaa')
    return `${date} ${start} - ${end}`
  }

  private get submitBtnText () {
    return (this.$store.state.isAppointmentEditMode) ? 'Update Appointment' : 'Confirm Appointment'
  }

  private get staticMapData () {
    return {
      officeNumber: this.currentOffice?.officeNumber ? this.currentOffice?.officeNumber.toString() + '.png' : '999.png',
      civicAddress: this.currentOffice?.civicAddress || '',
      latitude: this.currentOffice?.latitude || 0,
      longitude: this.currentOffice?.longitude || 0,
      externalMapLink: this.currentOffice?.externalMapLink || null
    }
  }

  dateTimeFormatted (date, formatStr) {
    if (!date) {
      return ''
    }
    return CommonUtils.getUTCToTimeZoneTime(date, this.currentOfficeTimezone, formatStr)
  }

  private async fetchUserAppointments () {
    this.myappointmentList = await this.getAppointmentList()
  }

  private async checkActiveDLKTService () {
    await this.fetchUserAppointments()
    this.myappointmentList.forEach(app => {
      if (app?.service?.isDlkt) {
        if (new Date(app?.startTime) >= new Date()) {
          this.anyActiveDLKT = true
          // TODO should there be a return/break here?
        } else {
          this.anyActiveDLKT = false
        }
      }
    })
  }

  private async confirmAppointment () {
    this.isLoading = true
    if (this.currentService.isDlkt && (!this.$store.state.isAppointmentEditMode)) {
      await this.checkActiveDLKTService()
    }
    // Save user profile if there is a change
    if (this.isSendSmsReminders || this.isSendEmailReminders) {
      let enableEmailReminder = this.currentUserProfile.sendEmailReminders
      let enableSmsReminder = this.currentUserProfile.sendSmsReminders
      if (this.isSendSmsReminders) {
        enableSmsReminder = true
      }
      if (this.isSendEmailReminders) {
        enableEmailReminder = true
      }
      const userUpdate: UserUpdateBody = {
        email: this.currentUserProfile.email,
        telephone: this.currentUserProfile.telephone,
        sendEmailReminders: enableEmailReminder,
        sendSmsReminders: enableSmsReminder
      }
      await this.updateUserAccount(userUpdate)
    }
    if (!this.anyActiveDLKT) {
      try {
        // Removed redundant "await"
        const resp = await this.createAppointment()
        if (resp.appointmentId) {
          const mySP = { step: 'Appointment Confirmed', loggedIn: this.isAuthenticated, apptID: resp.appointmentId, clientID: this.currentUserProfile?.userId, loc: this.currentOffice?.officeName, serv: this.currentService?.externalServiceName }
          this.callSnowplow(mySP)
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
    } else {
      // Removed redundant "await" on next line
      this.deleteDraftAppointment()
      this.isLoading = false
      this.dialogPopup.showDialog = true
      this.dialogPopup.isSuccess = false
      this.dialogPopup.title = 'Failed!'
      this.dialogPopup.subTitle = 'You already have one appointment scheduled for Knowledge Test, to reschedule please visit My Appointments. This booking cannot be completed..'
    }
  }

  private callsp () {
    (window as any).snowplow('trackPageView')
  }

  private clickOk () {
    this.dialogPopup.showDialog = false
    if (this.dialogPopup.isSuccess) {
      this.clearSelectedValues()
      this.$router.push('/booked-appointments')
      this.callsp()
    }
  }

  private goToTime () {
    this.dialogPopup.showDialog = false
    this.stepBack()
  }

  private goToMyAppointments () {
    this.dialogPopup.showDialog = false
    this.$router.push('/booked-appointments')
    this.callsp()
  }

  /* private getMapUrl (location) {
    return GeocoderService.generateStaticMapURL(location, { height: 200, width: 1200, scale: 2 })
  } */

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
.sms-info {
  font-style: italic;
  font-size: small;
  text-align: left;
  margin-left: 10%;
}
</style>
