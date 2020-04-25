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
            v-model="selecedDate"
            show-current
            light
            color="success"
            header-color="primary"
            full-width
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
          <div class="mt-6">
            <strong>Available Time Slots</strong>
          </div>
          <v-row>
            <v-col
              cols="6"
              v-for="timeslot in timeSlots"
              :key="timeslot.id"
            >
              <v-btn
                large
                outlined
                block
                color="primary">
                {{`${timeslot.startTime} - ${timeslot.endTime}`}}
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { format } from 'date-fns'

@Component
export default class DateSelection extends Vue {
  private selecedDate = new Date().toISOString().substr(0, 10)
  private timeSlots = [
    {
      id: 1,
      startTime: '9:30am',
      endTime: '9:45am'
    },
    {
      id: 2,
      startTime: '9:45am',
      endTime: '10:00am'
    },
    {
      id: 3,
      startTime: '10:00am',
      endTime: '10:15am'
    },
    {
      id: 4,
      startTime: '10:15am',
      endTime: '10:30am'
    }
  ];

  private get selectedDateFormatted () {
    return format(new Date(this.selecedDate), 'MMM dd, yyyy')
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
