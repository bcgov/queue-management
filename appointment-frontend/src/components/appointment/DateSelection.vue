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
import { Component, Prop, Vue } from 'vue-property-decorator'
import CommonUtils from '@/utils/common-util'
import { OfficeModule } from '@/store/modules'
import { format } from 'date-fns'
import { mapState } from 'vuex'

@Component({
  computed: {
    ...mapState('office', [
      'availableAppointmentSlots'
    ])
  }
})
export default class DateSelection extends Vue {
  private readonly availableAppointmentSlots!: any
  private selectedDate = new Date().toISOString().substr(0, 10)
  private selectedDateTimeSlots = []

  private get selectedDateFormatted () {
    return format(new Date(this.selectedDate), 'MMM dd, yyyy')
  }

  private dateClicked () {
    this.selectedDateTimeSlots = []
    const slots = this.availableAppointmentSlots[format(new Date(this.selectedDate), 'MM/dd/yyyy')]
    slots?.forEach(slot => {
      this.selectedDateTimeSlots.push({
        ...slot,
        startTimeStr: CommonUtils.get12HTimeString(slot.start_time),
        endTimeStr: CommonUtils.get12HTimeString(slot.end_time)
      })
    })
  }

  selectTimeSlot (slot) {
    // eslint-disable-next-line no-console
    console.log(slot)
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
