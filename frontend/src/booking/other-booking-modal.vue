<template>
  <b-modal v-model="modalVisible"
           modal-class="q-modal"
           body-class="q-modal"
           :no-close-on-backdrop="true"
           lazy
           @show="show"
           @hidden="hide"
           @cancel="cancel"
           @ok="postEvent"
           hide-header
           size="md">
    <div v-if="showModal">
      <b-form>
        <b-form-group>
          <label>Event Title<span style="color: red">{{ message }}</span></label><br>
          <b-input :state="state" type="text" v-model="title" />
        </b-form-group>
        <b-row>
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
        </b-row>
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
          <b-col cols="4">
            <b-form-group>
              <label>Start Time</label><br>
              <b-input type="text"
                       readonly
                       :value="startTime.format('hh:mm a')" />
            </b-form-group>
          </b-col>
          <b-col cols="4">
            <b-form-group>
              <label>End Time</label><br>
              <b-input type="text"
                       readonly
                       :value="endTime.format('hh:mm a')" />
            </b-form-group>
          </b-col>
          <b-col cols="4">
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
                         style="border-radius: 0px" />
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
    data() {
      return {
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
        'toggleSchedulingIndicator',
        'toggleSchedulingOther',
        'navigationVisible',
        'toggleCalendarControls',
      ]),
      cancel() {
        this.toggleSchedulingOther(true)
        this.toggleSchedulingIndicator(true)
        this.toggleOtherBookingModal(false)
        this.$root.$emit('unselect')
        this.message = ''
      },
      show() {
        this.toggleSchedulingIndicator(false)
        this.message = ''
        this.added = 0
        this.title = ''
        this.state = null
      },
      incrementDuration() {
        this.added -= .5
      },
      decrementDuration() {
        this.added += .5
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
          }
          this.postBooking(booking).then( () => {
            this.finishBooking()
            this.$root.$emit('options', {name: 'selectable', value: false})
          })
        } else {
          this.message = ' (Required)'
          this.state = 'invalid'
        }
      }
    }
  }
</script>