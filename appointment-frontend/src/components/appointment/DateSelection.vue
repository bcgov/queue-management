<template>
  <v-card>
    <v-card-title class="justify-center">
      <h3>Select a Date</h3>
    </v-card-title>
    <v-divider class="mx-4"></v-divider>
    <v-card-text>
      <p class="step-desc">What day would you like to have the appointment?</p>
      <v-row justify="center">
        <v-col
          cols="12"
          sm="6"
        >
          <v-date-picker
            v-model="selectedDate"
            show-current
            light
            color="success"
            header-color="primary"
            full-width
            @click:date="dateClicked"
          ></v-date-picker>
        </v-col>
        <v-col
          cols="12"
          sm="6"
          class="text-center"
        >
          <div>
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
  </v-card>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { mapMutations, mapState } from 'vuex'
import { AppointmentSlot } from '@/models/appointment'
import CommonUtils from '@/utils/common-util'
import { OfficeModule } from '@/store/modules'
import StepperMixin from '@/mixins/StepperMixin.vue'
import { format } from 'date-fns'
import { utcToZonedTime } from 'date-fns-tz'

@Component({
  computed: {
    ...mapState('office', [
      'availableAppointmentSlots'
    ])
  },
  methods: {
    ...mapMutations('office', [
      'setCurrentAppointmentSlot'
    ])
  }
})
export default class DateSelection extends Mixins(StepperMixin) {
  private readonly availableAppointmentSlots!: any
  private readonly setCurrentAppointmentSlot!: (slot: AppointmentSlot) => void
  private selectedDate = format(utcToZonedTime(new Date(), 'America/Vancouver'), 'yyyy-MM-dd')
  private selectedDateTimeSlots = []

  private get selectedDateFormatted () {
    return format(utcToZonedTime(this.selectedDate, 'America/Vancouver'), 'MMM dd, yyyy')
  }

  private dateClicked () {
    this.selectedDateTimeSlots = []
    const slots = this.availableAppointmentSlots[format(utcToZonedTime(this.selectedDate, 'America/Vancouver'), 'MM/dd/yyyy')]
    slots?.forEach(slot => {
      this.selectedDateTimeSlots.push({
        ...slot,
        startTimeStr: CommonUtils.get12HTimeString(slot.start_time),
        endTimeStr: CommonUtils.get12HTimeString(slot.end_time)
      })
    })
  }

  selectTimeSlot (slot) {
    const selectedSlot: AppointmentSlot = {
      start_time: new Date(`${this.selectedDate} ${slot.start_time}`).toISOString(),
      end_time: new Date(`${this.selectedDate} ${slot.end_time}`).toISOString()
    }
    this.setCurrentAppointmentSlot(selectedSlot)
    this.stepNext()
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
