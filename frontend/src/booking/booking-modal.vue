<template>
  <b-modal v-model="modalVisible"
           modal-class="q-modal"
           body-class="q-modal"
           :no-close-on-backdrop="true"
           hide-ok
           lazy
           @cancel="cancel"
           @ok="postEvent"
           hide-header
           size="md">
    <div v-if="showModal">
      <b-container style="font-size:1.1rem; border:1px solid lightgrey; border-radius: 10px">
        <b-row>
          <b-col><b>Booking Details</b></b-col>
        </b-row>
        <b-row no-gutters>
          <b-col cols="4">Date: </b-col><b-col> {{ date.start.local().format('ddd, MMM Do, YYYY')}}</b-col>
        </b-row>
        <b-row no-gutters>
          <b-col cols="4">Room: </b-col><b-col> {{ date.resource.title }}</b-col>
        </b-row>
        <b-row no-gutters>
          <b-col cols="4">Start: </b-col><b-col> {{ date.start.local().format('h:mm a') }}</b-col>
        </b-row>
        <b-row no-gutters>
          <b-col cols="4">End: </b-col><b-col> {{ endTime.local().format('h:mm a') }}</b-col>
        </b-row>
      </b-container>
      <b-container class="p-3" style="font-size: .9rem;">
        <b-row no-gutters>
          <b-col cols="4" >Exam: </b-col><b-col> {{ exam.exam_name }}</b-col>
        </b-row>
        <b-row no-gutters>
          <b-col cols="4">Event ID: </b-col><b-col> {{ exam.event_id }}</b-col>
        </b-row>
        <b-row no-gutters>
          <b-col cols="4">Type: </b-col><b-col> {{ exam.exam_type.exam_type_name }}</b-col>
        </b-row>
        <b-row no-gutters>
          <b-col cols="4">Format: </b-col><b-col> {{ exam.exam_method }}</b-col>
        </b-row>
        <b-row no-gutters>
          <b-col cols="4">Duration: </b-col><b-col> {{ exam.exam_type.number_of_hours+' hrs' }}</b-col>
        </b-row>
      </b-container>
    </div>
  </b-modal>
</template>

<script>
  import { mapState, mapMutations, mapActions } from 'vuex'
  import moment from 'moment'

  export default {
    name: "BookingModal",
    computed: {
      ...mapState({
        exam: state => state.selectedExam,
        date: state => state.clickedDate,
        showModal: state => state.showBookingModal,
      }),
      modalVisible: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleBookingModal(e)
        }
      },
      endTime() {
        if (this.date && this.exam) {
          let l = parseInt(this.exam.exam_type.number_of_hours)
          return new moment(this.date.start).add(l, 'hours')
        }
      },
    },
    methods: {
      ...mapActions(['scheduleExam']),
      ...mapMutations(['toggleBookingModal', 'toggleScheduling', 'toggleCalendarControls', 'navigationVisible']),
      cancel() {
        this.toggleScheduling(true)
        this.toggleBookingModal(false)
      },
      postEvent(e) {
        e.preventDefault()
        let start = new moment(this.date.start).utc()
        let end = new moment(this.endTime).utc()
        let booking = {
          room_id: this.date.resource.id,
          start_time: start.format('DD-MMM-YYYY[T]HH:mm:ssZ'),
          end_time: end.format('DD-MMM-YYYY[T]HH:mm:ssZ'),
          fees: 'false',
          booking_name: this.exam.exam_name,
        }
        this.scheduleExam(booking)
      }
    }
  }
</script>