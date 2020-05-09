<template>
  <v-card-text>
    <v-row justify="center">
      <v-col
        cols="12"
        md="6"
      >
        <v-date-picker
          v-model="selectedDate"
          show-current
          light
          :allowed-dates="getAllowedDates"
          :events="availableDates"
          event-color="green lighten-1"
          color="success"
          header-color="primary"
          full-width
          @click:date="dateClicked"
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
          <div class="mt-6">
            <strong>Available Time Slots</strong>
          </div>
          <v-row>
            <v-col
              cols="6"
              v-for="(timeslot, index) in selectedDateTimeSlots"
              :key="index"
            >
              <v-btn
                large
                outlined
                block
                @click="selectTimeSlot(timeslot)"
                color="primary">
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
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapMutations, mapState } from 'vuex'
import { AppointmentSlot } from '@/models/appointment'
import CommonUtils from '@/utils/common-util'
import { Office } from '@/models/office'
import { OfficeModule } from '@/store/modules'
import StepperMixin from '@/mixins/StepperMixin.vue'

@Component({
  computed: {
    ...mapState('office', [
      'availableAppointmentSlots',
      'currentAppointmentSlot',
      'currentOffice',
      'currentOfficeTimezone'
    ])
  },
  methods: {
    ...mapMutations('office', [
      'setCurrentAppointmentSlot'
    ]),
    ...mapActions('office', [
      'getAvailableAppointmentSlots'
    ])
  }
})
export default class DateSelection extends Mixins(StepperMixin) {
  private readonly availableAppointmentSlots!: any
  private readonly currentOffice!: Office
  private readonly currentAppointmentSlot!: AppointmentSlot
  private readonly currentOfficeTimezone!: string
  private readonly getAvailableAppointmentSlots!: (officeId: number) => Promise<any>
  private readonly setCurrentAppointmentSlot!: (slot: AppointmentSlot) => void
  // TODO: take timezone from office data from state
  private selectedDate = CommonUtils.getTzFormattedDate(new Date(), this.currentOfficeTimezone)
  private selectedDateTimeSlots = []
  private availableDates = []

  private get selectedDateFormatted () {
    return CommonUtils.getTzFormattedDate(this.selectedDate, this.currentOfficeTimezone, 'MMM dd, yyyy')
  }

  private get selectedTimeSlot () {
    return (this.currentAppointmentSlot?.start_time && this.currentAppointmentSlot?.end_time)
      ? `${CommonUtils.getTzFormattedDate(this.currentAppointmentSlot?.start_time, this.currentOfficeTimezone, 'hh:mm aaa')} -
        ${CommonUtils.getTzFormattedDate(this.currentAppointmentSlot?.end_time, this.currentOfficeTimezone, 'hh:mm aaa')}`
      : ''
  }

  private async mounted () {
    if (this.isOnCurrentStep) {
      if (this.currentOffice?.office_id) {
        const availableAppoinments = await this.getAvailableAppointmentSlots(this.currentOffice.office_id)
        Object.keys(availableAppoinments).forEach(date => {
          if (availableAppoinments[date]?.length) {
            this.availableDates.push(CommonUtils.getTzFormattedDate(new Date(date), this.currentOfficeTimezone))
          }
        })
      }
      this.selectedDate = CommonUtils.getTzFormattedDate(this.currentAppointmentSlot?.start_time, this.currentOfficeTimezone)
      this.dateClicked()
    }
  }

  private getAllowedDates (val) {
    return this.availableDates.find(date => date === val)
  }

  private dateClicked () {
    this.selectedDateTimeSlots = []
    const slots = this.availableAppointmentSlots[CommonUtils.getTzFormattedDate(this.selectedDate, this.currentOfficeTimezone, 'MM/dd/yyyy')]
    slots?.forEach(slot => {
      this.selectedDateTimeSlots.push({
        ...slot,
        startTimeStr: CommonUtils.get12HTimeString(slot.start_time),
        endTimeStr: CommonUtils.get12HTimeString(slot.end_time)
      })
    })
  }

  selectTimeSlot (slot) {
    // Note - For cross browser, we must use specific date string format below
    // Chrome/FF pass with "2020-05-08 09:00" but Safari fails.
    // Safari needs format from spec, "2020-05-08T09:00"
    const selectedSlot: AppointmentSlot = {
      start_time: CommonUtils.getTzDate(new Date(`${this.selectedDate}T${slot.start_time}`), this.currentOfficeTimezone).toISOString(),
      end_time: CommonUtils.getTzDate(new Date(`${this.selectedDate}T${slot.end_time}`), this.currentOfficeTimezone).toISOString()
    }
    this.setCurrentAppointmentSlot(selectedSlot)
    this.stepNext()
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
