<template>
  <b-modal v-model="modalVisible"
           modal-class="q-modal"
           body-class="q-modal"
           :no-close-on-backdrop="true"
           lazy
           @show="show"
           @cancel="cancel"
           @ok="postEvent"
           hide-header
           size="md">
    <div v-if="showModal" style="margin: 10px">
      <div v-if="minimized || !confirm" style="display: flex; justify-content: space-between">
        <div><h5>Other Booking</h5></div>
        <div><button class="btn btn-link"
                  @click="minimized = !minimized">{{ minimized ? "Maximize" : "Minimize" }}</button></div>
      </div>
      <div class="mb-1" style="font-size:1rem;">{{ startTime.format('ddd MMMM Do, YYYY') }}</div>
        <template v-if="!minimized">
          <b-form autocomplete="off">
            <b-form-group>
              <label>Scheduling Party<span style="color: red">{{ messageSP }}</span></label><br>
              <b-input :state="stateSP" type="text" v-model="title" />
            </b-form-group>
            <b-form-group>
              <label>Contact Information(Email or Phone Number)<span style="color: red">{{ messageCI }}</span></label><br>
              <b-input :state="stateCI" type="text" v-model="contact_information"/>
            </b-form-group>
            <b-form-row>
              <b-col cols="5">
                <b-form-group>
                  <label>Collect Fees<span style="color: red">{{ messageCF }}</span></label><br>
                  <b-select v-model="fees"
                            :state="stateCF"
                            :options="feesOptions" />
                </b-form-group>
              </b-col>
              <b-col cols="7">
                <b-form-group>
                  <label>Room</label>
                  <b-input readonly :value="resource.title" />
                </b-form-group>
              </b-col>
            </b-form-row>
            <b-form-row>
              <b-col>
                <b-form-group>
                  <label>Start Time</label><br>
                  <b-input type="text"
                           readonly
                           :value="startTime.format('hh:mm a')" />
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group>
                  <label>End Time</label><br>
                  <b-input type="text"
                           readonly
                           :value="endTime.format('hh:mm a')" />
                </b-form-group>
              </b-col>
              <b-col cols="5">
                <b-form-group>
                  <label>Duration</label><br>
                  <b-button-group>
                    <b-button @click="decrementDuration" >
                      <font-awesome-icon icon="minus"
                                         class="m-0 p-0"
                                         style="font-size: .8rem; color: white"/>
                    </b-button>
                    <b-input :value="displayDuration"
                             readonly
                             style="border-radius: 0px"
                             class="w-100"/>
                    <b-button @click="incrementDuration" >
                      <font-awesome-icon icon="plus"
                                         class="m-0 p-0"
                                         style="font-size: .8rem; color: white"/>
                    </b-button>
                  </b-button-group>
                </b-form-group>
              </b-col>
            </b-form-row>
          </b-form>
        </template>
    </div>
  </b-modal>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import moment from 'moment'
  import { FullCalendar } from 'vue-full-calendar'
  import 'fullcalendar/dist/fullcalendar.css'
  import 'fullcalendar-scheduler'

  export default {
    name: "OtherBookingModal",
    components: { FullCalendar },
    props: ['editSelection', 'getEvent'],
    data() {
      return {
        confirm: false,
        contact_information: '',
        minimized: false,
        title: '',
        stateSP: null,
        stateCI: null,
        stateCF: null,
        messageSP: '',
        messageCI: '',
        messageCF: '',
        fees: '',
        feesOptions: [
          {text: 'No', value: "false"},
          {text: 'Yes', value: "true"}
        ],
        added: 0,
        invoice: null,
        rate: null,
        start:'',
        end:'',
      }
    },
    computed: {
      ...mapState(
        {
          exam: state => state.selectedExam,
          event: state => state.clickedDate,
          showModal: state => state.showOtherBookingModal,
          selectionIndicator: state => state.selectionIndicator,
        }
      ),
      modalVisible: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleOtherBookingModal(e)
        }
      },
      startTime() {
        if (this.event && this.event.start) {
          return moment(this.event.start)
        }
        return ''
      },
      okDisabled() {
        if (this.title.length > 0 && this.contact_information.length > 0 && this.fees.length > 0) {
          return false
        }
        return true
      },
      endTime() {
        if (this.event && this.event.end) {
          let output = new moment(this.event.end)
          output.add(this.added, 'hours')
          return output
        }
        return ''
      },
      resource() {
        if (this.event && this.event.resource) {
          return this.event.resource
        }
        return ''
      },
      duration() {
        return this.endTime.diff(this.startTime, 'hours', true)
      },
      displayDuration() {
        let output = this.duration.toFixed(1)
        return `${output} hrs`
      },
    },
    methods: {
      ...mapActions(['postBooking', 'finishBooking']),
      ...mapMutations([
        'toggleOtherBookingModal',
      ]),
      cancel() {
        this.$root.$emit('removeSavedSelection')
        this.messageSP = ''
        this.messageCI = ''
        this.messageCF = ''
      },
      show() {
        this.messageSP = ''
        this.messageCI = ''
        this.messageCF = ''
        this.added = 0
        this.title = ''
        this.stateSP = null
        this.stateCI = null
        this.stateCF = null
      },
      incrementDuration() {
        if (this.endTime.format('H') == 18) {
          return
        }
        this.added += .5
        if (this.selectionIndicator) {
          let event = this.getEvent()
          this.editSelection(event, 0.5)
        }
      },
      decrementDuration() {
        if (this.duration == .5) {
          return
        }
        this.added -= .5
        if (this.selectionIndicator) {
          let event = this.getEvent()
          this.editSelection(event, -0.5)
        }
      },
      postEvent(e) {
        e.preventDefault()

        if (this.title.length === 0 ) {
          this.messageSP = ' (Required)'
          this.stateSP = 'invalid'

        } else {
           this.messageSP = ''
           this.stateSP = null
        }
         if (this.contact_information.length === 0 ) {

          this.messageCI = ' (Required)'
          this.stateCI = 'invalid'

        } else {
           this.messageCI = ''
           this.stateCI = null
        }
         if (this.fees.length === 0 ) {

          this.messageCF = ' (Required)'
          this.stateCF = 'invalid'

        } else {
           this.messageCF = ''
           this.stateCF = null
        }

        if (this.title.length > 0 && this.contact_information.length > 0 && this.fees.length > 0)  {
          let start = new moment(this.startTime).utc()
          let end = new moment(this.endTime).utc()
          let booking = {
            room_id: this.resource.id,
            start_time: start.format('DD-MMM-YYYY[T]HH:mm:ssZ'),
            end_time: end.format('DD-MMM-YYYY[T]HH:mm:ssZ'),
            fees: this.fees,
            booking_name: this.title,
            booking_contact_information: this.contact_information,
          }
          this.postBooking(booking).then( () => {
            this.finishBooking()
            this.contact_information = ''
          })
        }
      }






    }
  }
</script>]

event = {
title: 'a title',
end: moment('2019-01-21T19:54:33.03-08:00').format('YYY-MM').utc()
start: moment('2019-01-20T19:54:33.03-08:00').format('YYY-MM').utc()
id: '24324'
resource: 'the conservatory'
weapon: 'with the candlestick'
person: 'Mrs. White'
}

delete event.end
