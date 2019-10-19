<template>
  <b-modal v-model="modalVisible"
           modal-class="q-modal"
           body-class="q-modal"
           :no-close-on-backdrop="true"
           lazy
           @show="show"
           hide-header
           size="md">
    <template slot="modal-footer">
      <div class="d-flex flex-row-reverse">
        <b-button v-if="this.recurring_form_state === 'audit' && !this.submitting_flag || this.single_input_boolean"
                  variant="primary"
                  class="ml-2"
                  size="md"
                  id="final-submit"
                  @click="postEvent">
          Submit
        </b-button>
        <b-button v-else-if="this.recurring_form_state === 'audit' && this.submitting_flag"
                  variant="primary"
                  disabled
                  class="ml-2"
                  id="submitting-phase"
                  size="md">
          Submitting
        </b-button>
        <b-button v-else
                  disabled
                  class="ml-2"
                  id="disabled-submit"
                  size="md">
          Submit
        </b-button>
        <b-button v-if="this.recurring_form_state === 'rule_generated'"
                  variant="primary"
                  class="ml-2"
                  size="md"
                  id="recurring-generate-next"
                  @click="generateRule">
          Next
        </b-button>
        <b-button v-else-if="this.recurring_form_state === 'audit'"
                  disabled
                  class="ml-2"
                  size="md">
          Next
        </b-button>
        <b-button v-else-if="this.recurring_form_state === ''"
                  disabled
                  class="ml-2"
                  size="md">
          Next
        </b-button>
        <b-button class="ml-2"
                  @click="cancel">
          Cancel
        </b-button>
      </div>
    </template>
    <div v-if="showModal" style="margin: 10px">
      <div v-if="minimized || !confirm" style="display: flex; justify-content: space-between">
        <div><h5>Non-Exam Event Booking</h5></div>
        <div><button class="btn btn-link"
                  @click="minimized = !minimized">{{ minimized ? "Maximize" : "Minimize" }}</button></div>
      </div>
      <b-collapse id="collapse-other-booking-event-selection"
                  visible>
        <b-card>
          <b-form-row class="mb-2">
            <label>Step 1: Select Event Type</label>
          </b-form-row>
          <b-form-row>
            <b-col class="w-50">
              <b-button variant="primary"
                        class="w-100 mb-2"
                        v-b-toggle.collapse-single-event
                        @click="setRecurring">
                Create Single Event
              </b-button>
            </b-col>
            <b-col v-if="is_recurring_enabled"
                   class="w-50">
              <b-button variant="primary"
                        class="w-100 mb-2"
                        v-b-toggle.collapse-recurring-event
                        @click="setSingle">
                Create Recurring Event
              </b-button>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-single-event">
        <b-card class="mt-2">
          <b-form-row style="justify-content: center;"
                      class="mb-1">
            <h4>Single Event</h4>
          </b-form-row>
          <b-form-row>
            <label style="font-weight: bold;">Step 2: Event Information</label>
          </b-form-row>
          <div class="mb-1"
               style="font-size:1rem;">
            {{ startTime.format('ddd MMMM Do, YYYY') }}
          </div>
          <template v-if="!minimized">
            <b-form autocomplete="off">
              <b-form-group>
                <label>Scheduling Party<span style="color: red">{{ message }}</span></label>
                <font-awesome-icon v-if="this.title !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <b-input :state="state"
                         type="text"
                         v-model="title"
                         @change="checkSingleInput"
                         @input="checkSingleInput"/>
              </b-form-group>
              <b-form-group>
                <label>Contact Information(Email or Phone Number)</label>
                <font-awesome-icon v-if="this.contact_information !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <b-input :state="state"
                         type="text"
                         v-model="contact_information"
                         @change="checkSingleInput"
                         @input="checkSingleInput"/>
              </b-form-group>
              <b-form-row>
                <b-col cols="5">
                  <b-form-group>
                    <label>Collect Fees</label>
                    <font-awesome-icon v-if="this.fees !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                    <b-select v-model="fees"
                              :options="feesOptions"
                              @input="checkSingleInput"
                              @change="checkSingleInput"/>
                  </b-form-group>
                </b-col>
                <b-col cols="7">
                  <b-form-group>
                    <label>Room</label>
                    <b-input readonly
                             :value="resource.title" />
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
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-recurring-event">
        <b-card class="mt-2 mb-2">
          <b-form-row style="justify-content: center;">
            <h4>Recurring Event</h4>
          </b-form-row>
          <b-form-row style="font-weight: bold;">
            <label>Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-1">
            <b-col cols="6">
              <label>Scheduling Party</label>
              <font-awesome-icon v-if="this.recurring_title !== ''"
                                 icon="check"
                                 style="fontSize: 1rem; color: green;"/>
              <b-input type="text"
                       v-model="recurring_title"
                       @input="checkRecurringInput"
                       @change="checkRecurringInput">
              </b-input>
            </b-col>
            <b-col cols="6">
              <label>Contact Information</label>
              <font-awesome-icon v-if="this.recurring_contact_information !== ''"
                                 icon="check"
                                 style="fontSize: 1rem; color: green;"/>
              <b-input type="text"
                       v-model="recurring_contact_information"
                       @input="checkRecurringInput"
                       @change="checkRecurringInput">
              </b-input>
            </b-col>
          </b-form-row>
          <b-form-row class="mb-1">
            <b-col cols="6">
              <label>Collect Fees</label>
              <font-awesome-icon v-if="this.recurring_fees !== ''"
                                 icon="check"
                                 style="fontSize: 1rem; color: green;"/>
              <b-select v-model="recurring_fees"
                        :options="feesOptions"
                        @input="checkRecurringInput"
                        @change="checkRecurringInput"/>
            </b-col>
            <b-col cols="6">
              <label>Room</label>
              <b-input readonly :value="resource.title" />
            </b-col>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>Booking Start Time</label>
              <font-awesome-icon v-if="this.other_recurring_start_time !== null || this.other_recurring_display_time !== null"
                                 icon="check"
                                 style="fontSize: 1rem; color: green;"/>
              <DatePicker v-model="other_recurring_start_time"
                          id="other-recurring-start-time"
                          :time-picker-options="{ start: '8:00', step: '00:30', end: '17:30' }"
                          lang="en"
                          format="h:mm a"
                          autocomplete="off"
                          placeholder="Select Start Time"
                          class="w-100"
                          type="time"
                          @input="checkRecurringInput"
                          @change="checkRecurringInput"
                          @clear="checkRecurringInput">
              </DatePicker>
            </b-col>
            <b-col cols="6">
              <label>Booking End Time</label>
              <font-awesome-icon v-if="this.other_recurring_end_time !== null"
                                 icon="check"
                                 style="fontSize: 1rem; color:green;"/>
              <DatePicker v-model="other_recurring_end_time"
                          id="other-recurring-end-time"
                          :time-picker-options="{ start: '8:30', step: '00:30', end: '18:00' }"
                          lang="en"
                          format="h:mm a"
                          autocomplete="off"
                          placeholder="Select End Time"
                          class="w-100"
                          type="time"
                          @input="checkRecurringInput"
                          @change="checkRecurringInput"
                          @clear="checkRecurringInput">
              </DatePicker>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <label>Booking Start Date</label>
              <font-awesome-icon v-if="this.other_recurring_start_date !== null || this.other_recurring_display_date !== null"
                                 icon='check'
                                 style="fontSize: 1rem; color: green;"/>
              <DatePicker v-model="other_recurring_start_date"
                          id="other_blackout_start_date"
                          type="date"
                          lang="en"
                          class="w-100"
                          placeholder="Select Date"
                          @input="checkRecurringInput"
                          @change="checkRecurringInput"
                          @clear="checkRecurringInput">
              </DatePicker>
            </b-col>
            <b-col cols="6">
              <label>Booking End Date</label>
              <font-awesome-icon v-if="this.other_recurring_end_date !== null"
                                 icon='check'
                                 style="fontSize: 1rem; color: green;"/>
              <DatePicker v-model="other_recurring_end_date"
                          id="other_blackout_end_date"
                          type="date"
                          lang="en"
                          class="w-100"
                          @input="checkRecurringInput"
                          @change="checkRecurringInput"
                          @clear="checkRecurringInput">
              </DatePicker>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-form-group class="mt-2 ml-1">
              <label>Frequency</label>
              <font-awesome-icon v-if="this.other_selected_frequency.length === 1"
                                 icon="check"
                                 style="fontSize: 1rem; color: green;"/>
              <font-awesome-icon v-if="this.other_selected_frequency.length > 1"
                                 icon="exclamation-triangle"
                                 style="fontSize: 1rem; color: #FFC32B;"/>
              <label v-if="this.other_selected_frequency.length > 1">Select one frequency</label>
              <b-form-checkbox-group id="other-frequency-checkboxes"
                                     v-model="other_selected_frequency"
                                     @input="checkRecurringInput">
                <b-form-checkbox :value="yearly">Yearly</b-form-checkbox>
                <b-form-checkbox :value="monthly">Monthly</b-form-checkbox>
                <b-form-checkbox :value="weekly">Weekly</b-form-checkbox>
                <b-form-checkbox :value="daily">Daily</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>
          </b-form-row>
          <b-form-row>
            <b-form-group class="ml-1">
              <label>Select Weekdays</label>
              <font-awesome-icon v-if="this.other_selected_weekdays.length >= 1"
                                 icon="check"
                                 style="fontSize: 1rem; color: green;"/>
              <b-form-checkbox-group id="weekday-checkboxes"
                                     v-model="other_selected_weekdays"
                                     @input="checkRecurringInput">
                <b-form-checkbox :value="monday">Mon.</b-form-checkbox>
                <b-form-checkbox :value="tuesday">Tues.</b-form-checkbox>
                <b-form-checkbox :value="wednesday">Wed.</b-form-checkbox>
                <b-form-checkbox :value="thursday">Thur.</b-form-checkbox>
                <b-form-checkbox :value="friday">Fri.</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>
          </b-form-row>
          <b-form-row>
            <label>Number of Occurences (optional)</label>
            <span v-if="this.other_selected_count !== ''">&nbsp; Limited to {{ this.other_selected_count }} occurences.</span>
            <font-awesome-icon v-if="this.other_selected_count !== ''"
                               icon="check"
                               style="fontSize: 1rem; color: green;"
                               class="ml-1"/>
          </b-form-row>
          <b-form-row>
            <b-form-input type="number"
                          class="mb-1 w-25"
                          v-model="other_selected_count">
            </b-form-input>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-other-event-audit">
        <b-card v-if="this.other_rrule_text !== ''"
                class="mb-2">
          <b-form-row style="justify-content: center;">
            <h4>Recurring Event</h4>
          </b-form-row>
          <b-form-row>
            <label style="font-weight: bold;">Step 2 (continued): Confirm Recurring Event Information</label>
          </b-form-row>
          <b-form-row>
            <b-col cols="12">
              <b-button variant="primary"
                        class="w-100 mb-2"
                        v-b-toggle.other-recurring-rule-collapse>
                View Recurring Event Info
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row class="mb-0">
            <b-collapse id="other-recurring-rule-collapse"
                        class="mb-2 ml-2"
                        visible>
              {{ this.other_rrule_text }}
            </b-collapse>
          </b-form-row>
          <b-form-row>
            <b-col cols="12">
              <b-button variant="primary"
                        class="w-100 mb-2"
                        v-b-toggle.other-recurring-dates-collapse>
                View Recurring Dates ({{ this.other_rrule_array.length }})
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-collapse id="other-recurring-dates-collapse">
              <div style="height: 75px; overflow-y: scroll; margin: 0px;">
                <ul class="list-group mb-0"
                    v-for="date in this.other_rrule_array">
                  <li class="list-group-item">
                    <b>Event:</b> {{ formatStartDate(date.start) }} until {{ formatEndDate(date.end) }}
                  </li>
                </ul>
              </div>
            </b-collapse>
          </b-form-row>
        </b-card>
      </b-collapse>
    </div>
  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState, mapGetters } from 'vuex'
  import moment from 'moment'
  import { FullCalendar } from 'vue-full-calendar'
  import 'fullcalendar/dist/fullcalendar.css'
  import 'fullcalendar-scheduler'
  import { RRule } from 'rrule'
  import DatePicker from 'vue2-datepicker'

  export default {
    name: "OtherBookingModal",
    components: { FullCalendar, DatePicker },
    props: ['editSelection', 'getEvent'],
    data() {
      return {
        confirm: false,
        contact_information: '',
        minimized: false,
        title: '',
        state: null,
        message: '',
        fees: '',
        feesOptions: [
          {text: 'No', value: "false"},
          {text: 'Yes', value: "true"},
          {text: 'HQ to Invoice', value: "HQFin"}
        ],
        added: 0,
        invoice: null,
        rate: null,
        start:'',
        end:'',
        other_recurring_start_time: null,
        other_recurring_end_time: null,
        other_recurring_start_date: null,
        other_recurring_end_date: null,
        other_recurring_display_time: null,
        other_recurring_display_date: null,
        other_selected_frequency: [],
        other_selected_weekdays: [],
        other_selected_count: '',
        yearly: RRule.YEARLY,
        monthly: RRule.MONTHLY,
        weekly: RRule.WEEKLY,
        daily: RRule.DAILY,
        monday: RRule.MO,
        tuesday: RRule.TU,
        wednesday: RRule.WE,
        thursday: RRule.TH,
        friday: RRule.FR,
        other_single_event: true,
        other_recurring_event: true,
        other_rrule_text: '',
        other_rrule_array: [],
        recurring_title: '',
        recurring_contact_information: '',
        recurring_fees: '',
        single_input_boolean: false,
        recurring_input_boolean: false,
        recurring_form_state: '',
        submitting_flag: false,
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
      ...mapGetters([
        'is_recurring_enabled',
      ]),
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
      ...mapActions([
        'postBooking',
        'finishBooking',
        'getBookings',
      ]),
      ...mapMutations([
        'toggleOtherBookingModal',
        'toggleScheduling',
      ]),
      hideCollapse(div_id){
        if(document.getElementById(div_id)){
          if(document.getElementById(div_id).classList.contains('show')){
            this.$root.$emit('bv::toggle::collapse', div_id)
          }
        }
      },
      showCollapse(div_id){
        if(document.getElementById(div_id)){
          if(document.getElementById(div_id).style.display === 'none'){
            this.$root.$emit('bv::toggle::collapse', div_id)
          }
        }
      },
      cancel() {
        this.$root.$emit('removeSavedSelection')
        this.message = ''
        this.recurring_input_boolean = false
        this.single_input_boolean = false
        this.recurring_form_state = ''
        this.toggleOtherBookingModal(false)
      },
      show() {
        this.showCollapse('collapse-other-booking-event-selection')
        this.hideCollapse('collapse-single-event')
        /* TODO Start setting start time/date on modal load here
        let start = new moment(this.startTime)
        this.other_recurring_display_date = moment(start).clone().format('YYYY-MM-DD')
        this.other_recurring_display_time = moment(start).clone().format('HH:mm a')
        this.other_recurring_start_time = new moment(this.startTime).clone()
        this.other_recurring_start_date = new moment(this.startTime).clone()
        console.log('show time', this.other_recurring_start_time)
        console.log('show date', this.other_recurring_start_date)
        */

        // clear single event fields
        this.title = ''
        this.fees = ''
        this.contact_information = ''

        // clear recurring event fields
        this.other_recurring_end_date = null
        this.other_recurring_end_time = null
        this.recurring_title = ''
        this.recurring_fees = ''
        this.recurring_contact_information = ''
        this.other_selected_frequency = []
        this.other_selected_weekdays = []
        this.other_selected_count = ''
        this.other_rrule_array = []
        this.other_rrule_text = ''

        this.message = ''
        this.added = 0
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
        this.submitting_flag = true
        let self = this
        if(this.other_rrule_array.length > 0){
          this.other_rrule_array.forEach(date => {
            let booking = {
              room_id: self.resource.id,
              start_time: date.start,
              end_time: date.end,
              fees: self.recurring_fees,
              booking_name: self.recurring_title,
              booking_contact_information: self.recurring_contact_information,
            }
            self.postBooking(booking).then( () => {
              self.getBookings()
            })
          })
          this.recurring_contact_information = ''
        }

        if (this.title.length > 0) {
          this.message = ''
          this.state = null
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
        } else {
          this.message = ' (Required)'
          this.state = 'invalid'
        }
        this.other_single_event = true
        this.other_recurring_event = true
        this.recurring_input_boolean = false
        setTimeout(function() {
          self.toggleOtherBookingModal(false)
          self.toggleScheduling(false)
          self.getBookings()
          self.submitting_flag = false
        }, 2000)
      },
      setSingle(){
        this.hideCollapse('collapse-single-event')
        this.other_single_event = !this.other_single_event
        this.title = ''
        this.contact_information = ''
        this.fees = ''
        this.recurring_form_state = ''
      },
      setRecurring(){
        this.hideCollapse('collapse-recurring-event')
        this.other_recurring_event = !this.other_recurring_event
        this.recurring_title = ''
        this.recurring_contact_information = ''
        this.recurring_fees = ''
        this.other_recurring_end_time = null
        this.other_recurring_end_date = null
        this.other_selected_frequency = []
        this.other_selected_weekdays = []
        this.other_selected_count = ''
        this.recurring_form_state = ''
      },
      formatStartDate(date){
        let formatted_start_date = moment(date).format('YYYY-MM-DD HH:mm')
        return formatted_start_date
      },
      formatEndDate(date){
        let formatted_end_date = moment(date).clone().format('HH:mm')
        return formatted_end_date
      },
      generateRule(){
        this.other_single_event = true
        this.other_recurring_event = true
        // Commented out start/end variables are for testing 5pm pst -> utc conversion bug
        // Removed these variables from the date_start and until variable declarations
        let start_year = parseInt(moment(this.other_recurring_start_date).utc().clone().format('YYYY'))
        let start_month = parseInt(moment(this.other_recurring_start_date).utc().clone().format('MM'))
        let start_day = parseInt(moment(this.other_recurring_start_date).utc().clone().format('DD'))
        //let start_hour = parseInt(moment(this.other_recurring_start_time).utc().clone().format('HH'))
        let local_start_hour = parseInt(moment(this.other_recurring_start_time).clone().format('HH'))
        //let start_minute = parseInt(moment(this.other_recurring_start_time).utc().clone().format('mm'))
        let end_year = parseInt(moment(this.other_recurring_end_date).utc().clone().format('YYYY'))
        let end_month = parseInt(moment(this.other_recurring_end_date).utc().clone().format('MM'))
        let end_day = parseInt(moment(this.other_recurring_end_date).utc().clone().format('DD'))
        //let end_hour = parseInt(moment(this.other_recurring_end_time).utc().clone().format('HH'))
        //let end_minute = parseInt(moment(this.other_recurring_end_time).utc().clone().format('mm'))
        let duration = moment.duration(moment(this.other_recurring_end_time).diff(moment(this.other_recurring_start_time)))
        let duration_minutes = duration.asMinutes()
        let input_frequency = null
        let local_other_dates_array = []

        switch(this.other_selected_frequency[0]){
          case 0:
            input_frequency = RRule.YEARLY;
            break;
          case 1:
            input_frequency = RRule.MONTHLY;
            break;
          case 2:
            input_frequency = RRule.WEEKLY;
            break;
          case 3:
            input_frequency = RRule.DAILY;
            break;
        }

        if(isNaN(start_year) == false || isNaN(end_year) == false){
          // TODO Might be Deprecated -- IF RRule Breaks, this is where it will happen
          // TODO remove tzid from rule object
          let date_start = new Date(Date.UTC(start_year, start_month-1, start_day))
          let until = new Date(Date.UTC(end_year, end_month-1, end_day))

          const rule = new RRule({
            freq: input_frequency,
            count: this.other_selected_count,
            byweekday: this.other_selected_weekdays,
            dtstart: date_start,
            until: until,
            tzid: Intl.DateTimeFormat().resolvedOptions().timeZone,
          })

          let array = rule.all()
          this.other_rrule_text = rule.toText()

          array.forEach(date => {
            let date_with_offset = moment(date).clone().set({hour: local_start_hour}).add(new Date().getTimezoneOffset(), 'minutes')
            let formatted_start_date = moment(date_with_offset).clone().set({hour: local_start_hour}).format('YYYY-MM-DD HH:mm:ssZ')
            let formatted_end_date = moment(date_with_offset).clone().set({hour: local_start_hour}).add(duration_minutes, 'minutes').format('YYYY-MM-DD HH:mm:ssZ')
            local_other_dates_array.push({start: formatted_start_date, end: formatted_end_date})
          })
        }
        this.other_rrule_array = local_other_dates_array
        this.other_selected_count = ''
        this.other_selected_weekdays = []
        this.other_selected_frequency = []
        this.other_recurring_start_date = ''
        this.other_recurring_start_time = ''
        this.other_recurring_end_date = ''
        this.other_recurring_end_time = ''
        this.showCollapse('collapse-other-event-audit')
        this.hideCollapse('collapse-other-booking-event-selection')
        this.hideCollapse('collapse-recurring-event')
        this.recurring_form_state = 'audit'
      },
      checkRecurringInput(){
        if(this.other_selected_frequency.length > 0 && this.other_recurring_end_date !== null
          && this.other_recurring_end_time !== null && this.recurring_title !== '' && this.recurring_fees !== ''){
          this.recurring_input_boolean = true
          this.recurring_form_state = 'rule_generated'
        } else {
          this.recurring_input_boolean = false
        }
      },
      checkSingleInput(){
        if(this.contact_information !== '' && this.title !== '' && this.fees !== ''){
          this.single_input_boolean = true
        }else {
          this.single_input_boolean = false
        }
      }
    }
  }
</script>
