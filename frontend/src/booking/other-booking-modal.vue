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
              <label>Scheduling Party<span style="color: red">{{ message }}</span></label><br>
              <b-input :state="state" type="text" v-model="title" />
            </b-form-group>
            <b-form-group>
              <label>Contact Information(Email or Phone Number)</label><br>
              <b-input :state="state" type="text" v-model="contact_information"/>
            </b-form-group>
            <b-form-row>
              <b-col cols="5">
                <b-form-group>
                  <label>Collect Fees</label><br>
                  <b-select v-model="fees" :options="feesOptions" />
                </b-form-group>
              </b-col>
              <b-col cols="7">
                <b-form-group>
                  <label>Room</label>
                  <b-input readonly :value="resource.title" />
                </b-form-group>
              </b-col>
            </b-form-row>
            <b-form-row v-if="fees">
              <b-col cols="4">
                <b-form-group>
                  <label>Fee Option</label>
                  <b-select :options="roomRates" v-model="rate" />
                </b-form-group>
              </b-col>
              <b-col cols="8">
                <b-form-group>
                  <label>Invoice To</label>
                  <b-select :options="invoiceOptions" v-model="invoice"/>
                </b-form-group>
              </b-col>
            </b-form-row>
            <b-form-row v-if="invoice==='custom'">
              <b-col cols="12">
                <b-form-group>
                  <label>Enter Name of Entity to Invoice</label><br>
                  <b-input />
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
        state: null,
        message: '',
        fees: false,
        feesOptions: [
          {text: 'No', value: false},
        ],
        added: 0,
        roomRates: [
          {value: 125, text: '$125 for 1/2 Day'},
          {value: 250, text: '$250 for Whole Day'}
        ],
        invoiceOptions: [
          {text: 'Custom', value: 'custom'}
        ],
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
      ...mapGetters(['room_resources']),
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
        if (this.title.length > 0) {
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
        this.message = ''
      },
      show() {
        this.message = ''
        this.added = 0
        this.title = ''
        this.state = null
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
        if (this.title.length > 0) {
          this.message = ''
          this.state = null
          let start = new moment(this.startTime).utc()
          let end = new moment(this.endTime).utc()
          let booking = {
            room_id: this.resource.id,
            start_time: start.format('DD-MMM-YYYY[T]HH:mm:ssZ'),
            end_time: end.format('DD-MMM-YYYY[T]HH:mm:ssZ'),
            fees: 'false',
            booking_name: this.title,
            booking_contact_information: this.contact_information,
          }
          this.postBooking(booking).then( () => {
            this.finishBooking()
          })
        } else {
          this.message = ' (Required)'
          this.state = 'invalid'
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
