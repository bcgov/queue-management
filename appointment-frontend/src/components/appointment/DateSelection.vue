<template>
  <v-card-text>
    <v-row justify="center">
      <v-col
        cols="12"
        md="6"
      >
        <v-date-picker
          id="appointment-datepicker"
          v-model="selectedDate"
          show-current
          light
          :allowed-dates="getAllowedDates"
          :events="availableDates"
          event-color="green lighten-1"
          color="success"
          header-color="primary"
          full-width
          @click:date="goto('available');dateClicked('true')"
          data-cy="step-3-date-picker"
        ></v-date-picker>
      </v-col>
      <v-col
        cols="12"
        md="6"
        class="text-center"
      >
        <div v-if="selectedTimeSlot">
          <strong class="mr-1">Appointment Date: </strong>
          <br class='d-sm-none' />
          {{selectedDateFormatted}}, {{selectedTimeSlot}}
        </div>
        <div v-else>
          <strong class="mr-1">Date Selected: </strong> {{selectedDateFormatted}}
        </div>
        <template v-if="selectedDateTimeSlots.length">
          <div ref="available" class="mt-6">
            <strong>Available Time Slots</strong>
          </div>
          <v-row>
            <v-col
              cols="12"
              sm="6"
              v-for="(timeslot, index) in selectedDateTimeSlots"
              :key="index"
            >
              <v-btn
                large
                outlined
                block
                @click="selectTimeSlot(timeslot)"
                color="primary"
                data-cy="step-3-button-timeslot"
              >
                {{`${timeslot.startTimeStr} - ${timeslot.endTimeStr}`}}
              </v-btn>
            </v-col>
          </v-row>
        </template>
        <template v-else>
          <div class="mt-6 error-text">
            <strong>No time slots available on the selected date</strong>
          </div>
        </template>
      </v-col>
    </v-row>
  </v-card-text>
</template>

<script lang="ts">
/* eslint-disable sort-imports */
import { Appointment, AppointmentSlot } from '@/models/appointment'
import CommonUtils from '@/utils/common-util'
import { Component, Mixins } from 'vue-property-decorator'
import { mapActions, mapMutations, mapState } from 'vuex'
import { Office } from '@/models/office'
import { Service } from '../../models/service'
import StepperMixin from '@/mixins/StepperMixin.vue'

@Component({
  computed: {
    ...mapState('office', [
      'availableAppointmentSlots',
      'currentAppointmentSlot',
      'currentOffice',
      'currentOfficeTimezone',
      'currentService'
    ])
  },
  methods: {
    ...mapMutations('office', [
      'setCurrentAppointmentSlot',
      'setCurrentDraftAppointment'
    ]),
    ...mapActions('office', [
      'getAvailableAppointmentSlots',
      'createDraftAppointment'
    ])
  }
})
export default class DateSelection extends Mixins(StepperMixin) {
  private readonly availableAppointmentSlots!: any
  private readonly currentOffice!: Office
  private readonly currentAppointmentSlot!: AppointmentSlot
  private readonly currentOfficeTimezone!: string
  private readonly getAvailableAppointmentSlots!: (input: {officeId: number, serviceId: number}) => Promise<any>
  private readonly createDraftAppointment!: () => Promise<any>
  private readonly setCurrentAppointmentSlot!: (slot: AppointmentSlot) => void
  private readonly setCurrentDraftAppointment!: (appointment: Appointment) => void
  private readonly currentService!: Service
  private selectedDate = ''
  private selectedDateObj = ''
  private selectedDateTimeSlots = []
  private availableDates = []
  private isUserClicked = 'false'

   private isLoading: boolean = false

   private get selectedDateFormatted () {
     if (this.isUserClicked === 'true') {
       return CommonUtils.getTzFormattedDate(new Date(CommonUtils.changeDateFormat(this.selectedDate)), Intl.DateTimeFormat().resolvedOptions().timeZone, 'MMM dd, yyyy')
     } else if (this.selectedDateObj) {
       return CommonUtils.getTzFormattedDate(new Date(this.selectedDateObj), Intl.DateTimeFormat().resolvedOptions().timeZone, 'MMM dd, yyyy')
     }
     return CommonUtils.getTzFormattedDate(new Date(), Intl.DateTimeFormat().resolvedOptions().timeZone, 'MMM dd, yyyy')
   }

   private get selectedTimeSlot () {
     return (this.currentAppointmentSlot?.startTime && this.currentAppointmentSlot?.endTime)
       ? `${CommonUtils.getFormattedDate(this.currentAppointmentSlot?.startTime, 'hh:mm aaa')} -
        ${CommonUtils.getFormattedDate(this.currentAppointmentSlot?.endTime, 'hh:mm aaa')}`
       : ''
   }

   private async mounted () {
     if (this.isOnCurrentStep) {
       if (this.currentOffice?.officeId) {
         this.getAvailableService()
       }
       this.dateClicked()
     }
   }

   private async getAvailableService () {
     const availableAppoinments = await this.getAvailableAppointmentSlots({
       officeId: this.currentOffice.officeId,
       serviceId: this.currentService.serviceId
     })
     Object.keys(availableAppoinments).forEach(date => {
       if (availableAppoinments[date]?.length) {
         this.availableDates.push(CommonUtils.getTzFormattedDate(new Date(date), this.currentOfficeTimezone))
         if (!this.selectedDate) {
           this.selectedDate = CommonUtils.getTzFormattedDate(new Date(date), this.currentOfficeTimezone)
           this.selectedDateObj = date
           this.dateClicked()
         }
       }
     })
   }

   private getAllowedDates (val) {
     return this.availableDates.find(date => date === val)
   }

   goto (refName) {
     let element = this.$refs[refName] as HTMLDivElement
     let top = element.offsetTop
     window.scrollTo(0, top)
   }

   private dateClicked (userClicked = 'false') {
     this.selectedDateTimeSlots = []
     let slots: AppointmentSlot[] = []
     if (this.selectedDate) {
       if (userClicked === 'true') {
         this.isUserClicked = 'true'
         slots = this.availableAppointmentSlots[CommonUtils.getTzFormattedDate(new Date(CommonUtils.changeDateFormat(this.selectedDate)), this.currentOfficeTimezone, 'MM/dd/yyyy')]
       } else {
         slots = this.availableAppointmentSlots[CommonUtils.getTzFormattedDate(new Date(this.selectedDateObj), this.currentOfficeTimezone, 'MM/dd/yyyy')]
       }
     }
     slots?.forEach(slot => {
       this.selectedDateTimeSlots.push({
         ...slot,
         startTimeStr: CommonUtils.get12HTimeString(slot.startTime),
         endTimeStr: CommonUtils.get12HTimeString(slot.endTime)
       })
     })
   }

   async selectTimeSlot (slot: AppointmentSlot) {
     const selectedSlot: AppointmentSlot = {
       startTime: `${this.selectedDate}T${slot.startTime}:00`,
       endTime: `${this.selectedDate}T${slot.endTime}:00`
     }
     this.setCurrentAppointmentSlot(selectedSlot)
     try {
       const resp = await this.createDraftAppointment()
       if (resp) {
         this.setCurrentDraftAppointment(resp)
         this.setCurrentAppointmentSlot({
           startTime: resp.localStartTime,
           endTime: resp.localEndTime
         })
         window.scrollTo(0, 0)
         this.stepNext()
       }
     } catch (error) {
       this.isLoading = false

       this.getAvailableService()
       this.dateClicked()
     }
   }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
@import "@/assets/scss/overrides.scss";
</style>
