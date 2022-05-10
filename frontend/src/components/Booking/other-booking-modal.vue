<template>
  <b-modal
    v-model="modalVisible"
    modal-class="q-modal"
    body-class="q-modal"
    :no-close-on-backdrop="true"
    lazy
    @show="show"
    hide-header
    size="md"
  >
    <template slot="modal-footer">
      <div class="d-flex flex-row-reverse">
        <b-button
          v-if="
            (this.recurring_form_state === 'audit' && !this.submitting_flag) ||
            this.single_input_boolean
          "
          variant="primary"
          class="ml-2"
          size="md"
          id="final-submit"
          @click="postEvent"
        >
          Submit
        </b-button>
        <b-button
          v-else-if="
            this.recurring_form_state === 'audit' && this.submitting_flag
          "
          variant="primary"
          disabled
          class="ml-2"
          id="submitting-phase"
          size="md"
        >
          Submitting
        </b-button>
        <b-button v-else disabled class="ml-2" id="disabled-submit" size="md">
          Submit
        </b-button>
        <b-button
          v-if="this.recurring_form_state === 'rule_generated'"
          variant="primary"
          class="ml-2"
          size="md"
          id="recurring-generate-next"
          @click="generateRule"
        >
          Next
        </b-button>
        <b-button
          v-else-if="this.recurring_form_state === 'audit'"
          disabled
          class="ml-2"
          size="md"
        >
          Next
        </b-button>
        <b-button
          v-else-if="this.recurring_form_state === ''"
          disabled
          class="ml-2"
          size="md"
        >
          Next
        </b-button>
        <b-button class="ml-2" @click="cancel"> Cancel </b-button>
      </div>
    </template>
    <div v-if="showModal" style="margin: 10px">
      <div
        v-if="minimized || !confirm"
        style="display: flex; justify-content: space-between"
      >
        <div><h5>Non-Exam Event Booking</h5></div>
        <div>
          <button class="btn btn-link" @click="minimized = !minimized">
            {{ minimized ? 'Maximize' : 'Minimize' }}
          </button>
        </div>
      </div>
      <b-collapse id="collapse-other-booking-event-selection" visible>
        <b-card>
          <b-form-row class="mb-2">
            <label>Step 1: Select Event Type</label>
          </b-form-row>
          <b-form-row>
            <b-col class="w-50">
              <b-button
                variant="primary"
                class="w-100 mb-2"
                v-b-toggle.collapse-single-event
                @click="setRecurring"
              >
                Create Single Event
              </b-button>
            </b-col>
            <b-col v-if="is_recurring_enabled" class="w-50">
              <b-button
                variant="primary"
                class="w-100 mb-2"
                v-b-toggle.collapse-recurring-event
                @click="setSingle"
              >
                Create Recurring Event
              </b-button>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-single-event">
        <b-card class="mt-2">
          <b-form-row style="justify-content: center" class="mb-1">
            <h4>Single Event</h4>
          </b-form-row>
          <b-form-row>
            <label style="font-weight: bold">Step 2: Event Information</label>
          </b-form-row>
          <div class="mb-1" style="font-size: 1rem">
            {{ startTime.format('ddd MMMM Do, YYYY') }}
          </div>
          <template v-if="!minimized">
            <b-form autocomplete="off">
              <b-form-group>
                <label
                  >Scheduling Party<span style="color: red">{{
                    message
                  }}</span></label
                >
                <font-awesome-icon
                  v-if="this.title !== ''"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <b-input
                  :state="state"
                  type="text"
                  v-model="title"
                  @change="checkSingleInput"
                  @input="checkSingleInput"
                />
              </b-form-group>
              <b-form-group>
                <label>Contact Information(Email or Phone Number)</label>
                <font-awesome-icon
                  v-if="this.contact_information !== ''"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <b-input
                  :state="state"
                  type="text"
                  v-model="contact_information"
                  @change="checkSingleInput"
                  @input="checkSingleInput"
                />
              </b-form-group>
              <b-form-row>
                <b-col cols="5">
                  <b-form-group>
                    <label>Collect Fees</label>
                    <font-awesome-icon
                      v-if="this.fees !== ''"
                      icon="check"
                      style="font-size: 1rem; color: green"
                    />
                    <b-select
                      v-model="fees"
                      :options="feesOptions"
                      @input="checkSingleInput"
                      @change="checkSingleInput"
                    />
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
                    <label>Start Time</label><br />
                    <b-input
                      type="text"
                      readonly
                      :value="startTime.format('hh:mm a')"
                    />
                  </b-form-group>
                </b-col>
                <b-col>
                  <b-form-group>
                    <label>End Time</label><br />
                    <b-input
                      type="text"
                      readonly
                      :value="endTime.format('hh:mm a')"
                    />
                  </b-form-group>
                </b-col>
                <b-col cols="5">
                  <b-form-group>
                    <label>Duration</label><br />
                    <b-button-group>
                      <b-button @click="decrementDuration">
                        <font-awesome-icon
                          icon="minus"
                          class="m-0 p-0"
                          style="font-size: 0.8rem; color: white"
                        />
                      </b-button>
                      <b-input
                        :value="displayDuration"
                        readonly
                        style="border-radius: 0px"
                        class="w-100"
                      />
                      <b-button @click="incrementDuration">
                        <font-awesome-icon
                          icon="plus"
                          class="m-0 p-0"
                          style="font-size: 0.8rem; color: white"
                        />
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
          <b-form-row style="justify-content: center">
            <h4>Recurring event</h4>
          </b-form-row>
          <b-form-row style="font-weight: bold">
            <label>Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-1">
            <b-col cols="6">
              <label>Scheduling Party</label>
              <font-awesome-icon
                v-if="this.recurring_title !== ''"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <b-input
                type="text"
                v-model="recurring_title"
                @input="checkRecurringInput"
                @change="checkRecurringInput"
              >
              </b-input>
            </b-col>
            <b-col cols="6">
              <label>Contact Information</label>
              <font-awesome-icon
                v-if="this.recurring_contact_information !== ''"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <b-input
                type="text"
                v-model="recurring_contact_information"
                @input="checkRecurringInput"
                @change="checkRecurringInput"
              >
              </b-input>
            </b-col>
          </b-form-row>
          <b-form-row class="mb-1">
            <b-col cols="6">
              <label>Collect Fees</label>
              <font-awesome-icon
                v-if="this.recurring_fees !== ''"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <b-select
                v-model="recurring_fees"
                :options="feesOptions"
                @input="checkRecurringInput"
                @change="checkRecurringInput"
              />
            </b-col>
            <b-col cols="6">
              <label>Room</label>
              <b-input readonly :value="resource.title" />
            </b-col>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>Booking Start Time</label>
              <font-awesome-icon
                v-if="
                  this.other_recurring_start_time !== null ||
                  this.other_recurring_display_time !== null
                "
                icon="check"
                style="font-size: 1rem; color: green"
              />
                <vue-timepicker
                  v-model="other_recurring_start_time"
                  id="other-recurring-start-time"
                  class="w-100"
                  icon="clock"
                  editable
                  format="hh:mm A"
                  locale="en-US"
                  placeholder="Select Start Time"
                  @input="checkRecurringInput"
                  @change="checkRecurringInput"
                  @clear="checkRecurringInput"
                  manual-input>
              </vue-timepicker>
                <br/>
                <span class="danger" v-if="start_time_msg">{{start_time_msg}}</span>
            </b-col>
            <b-col cols="6">
              <label>Booking End Time</label>
              <font-awesome-icon
                v-if="this.other_recurring_end_time !== null"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <vue-timepicker
                v-model="other_recurring_end_time"
                id="other-recurring-end-time"
                :value="other_recurring_end_time"
                class="w-100"
                icon="clock"
                editable
                format="hh:mm A"
                locale="en-US"
                placeholder="Select End Time"
                @input="checkRecurringInput"
                @change="checkRecurringInput"
                @clear="checkRecurringInput"
                manual-input>
              </vue-timepicker>
              <br/>
              <span class="danger" v-if="end_time_msg">{{end_time_msg}}</span>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <label>Booking Start Date</label>
              <font-awesome-icon
                v-if="
                  this.other_recurring_start_date !== null ||
                  this.other_recurring_display_date !== null
                "
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <DatePicker
                v-model="other_recurring_start_date"
                id="other_blackout_start_date"
                type="date"
                lang="en"
                class="w-100"
                placeholder="Select Date"
                @input="checkRecurringInput"
                @change="checkRecurringInput"
                @clear="checkRecurringInput"
              >
              </DatePicker>
            </b-col>
            <b-col cols="6">
              <label>Booking End Date</label>
              <font-awesome-icon
                v-if="this.other_recurring_end_date !== null"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <DatePicker
                v-model="other_recurring_end_date"
                id="other_blackout_end_date"
                type="date"
                lang="en"
                class="w-100"
                @input="checkRecurringInput"
                @change="checkRecurringInput"
                @clear="checkRecurringInput"
              >
              </DatePicker>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-form-group class="mt-2 ml-1">
              <label>Frequency</label>
              <font-awesome-icon
                v-if="this.other_selected_frequency.length === 1"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <font-awesome-icon
                v-if="this.other_selected_frequency.length > 1"
                icon="exclamation-triangle"
                style="font-size: 1rem; color: #ffc32b"
              />
              <label v-if="this.other_selected_frequency.length > 1"
                >Select one frequency</label
              >
              <b-form-checkbox-group
                id="other-frequency-checkboxes"
                v-model="other_selected_frequency"
                @input="checkRecurringInput"
              >
                <b-form-checkbox :value="weekly">Weekly</b-form-checkbox>
                <b-form-checkbox :value="daily">Daily</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>
          </b-form-row>
          <b-form-row>
            <b-form-group class="ml-1">
              <label>Select Weekdays</label>
              <font-awesome-icon
                v-if="this.other_selected_weekdays.length >= 1"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <b-form-checkbox-group
                id="weekday-checkboxes"
                v-model="other_selected_weekdays"
                @input="checkRecurringInput"
              >
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
            <span v-if="this.other_selected_count !== ''"
              >&nbsp; Limited to
              {{ this.other_selected_count }} occurences.</span
            >
            <font-awesome-icon
              v-if="this.other_selected_count !== ''"
              icon="check"
              style="font-size: 1rem; color: green"
              class="ml-1"
            />
          </b-form-row>
          <b-form-row>
            <b-form-input
              type="number"
              class="mb-1 w-25"
              v-model="other_selected_count"
            >
            </b-form-input>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-other-event-audit">
        <b-card v-if="this.other_rrule_text !== ''" class="mb-2">
          <b-form-row style="justify-content: center">
            <h4>Recurring Event</h4>
          </b-form-row>
          <b-form-row>
            <label style="font-weight: bold"
              >Step 2 (continued): Confirm Recurring Event Information</label
            >
          </b-form-row>
          <b-form-row>
            <b-col cols="12">
              <b-button
                variant="primary"
                class="w-100 mb-2"
                v-b-toggle.other-recurring-rule-collapse
              >
                View Recurring Event Info
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row class="mb-0">
            <b-collapse
              id="other-recurring-rule-collapse"
              class="mb-2 ml-2"
              visible
            >
              {{ this.other_rrule_text }}
            </b-collapse>
          </b-form-row>
          <b-form-row>
            <b-col cols="12">
              <b-button
                variant="primary"
                class="w-100 mb-2"
                v-b-toggle.other-recurring-dates-collapse
              >
                View Recurring Dates ({{ this.other_rrule_array.length }})
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-collapse id="other-recurring-dates-collapse">
              <div style="height: 75px; overflow-y: scroll; margin: 0px">
                <ul
                  class="list-group mb-0"
                  v-for="date in this.other_rrule_array"
                  :key="date.start"
                >
                  <li class="list-group-item">
                    <strong>Event:</strong> {{ formatStartDate(date.start) }} until
                    {{ formatEndDate(date.end) }}
                  </li>
                </ul>
              </div>
            </b-collapse>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="date-limit">
        <b-card class="mb-2">
          <b-card-body>
            <b-form-row class="mb-2">
              <label stlye="font-weight: bold;" class="danger"
              >Cannot blackout more that 1 year at Once.
              </label
              >
            </b-form-row>
          </b-card-body>
        </b-card>
      </b-collapse>
    </div>
  </b-modal>
</template>

<script lang="ts">
/* eslint-disable */
import { Action, Getter, Mutation, State, namespace } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'

import DatePicker from 'vue2-datepicker'
import VueTimepicker from 'vue2-timepicker'
import { RRule } from 'rrule'

import moment from 'moment'

import { apiProgressBus, APIProgressBusEvents } from '../../events/progressBus'
import { showBookingFlagBus, ShowBookingFlagBusEvents } from '../../events/showBookingFlagBus'
import 'vue2-datepicker/index.css'
import 'vue2-timepicker/dist/VueTimepicker.css'


const appointmentsModule = namespace('appointmentsModule')

@Component({
  components: {
    DatePicker,
    VueTimepicker
  }
})
export default class OtherBookingModal extends Vue {
  @Prop({ default: '' })
  private editSelection!: any

  @Prop({ default: '' })
  private getEvent!: any

  @State('selectedExam') private exam!: any
  @State('clickedDate') private event!: any
  @State('showOtherBookingModal') private showModal!: any
  @State('selectionIndicator') private selectionIndicator!: any

  @Getter('is_recurring_enabled') private is_recurring_enabled!: any;

  @Action('postBooking') public postBooking: any
  @Action('finishBooking') public finishBooking: any
  @Action('getBookings') public getBookings: any

  @Mutation('toggleOtherBookingModal') public toggleOtherBookingModal: any
  @Mutation('toggleScheduling') public toggleScheduling: any
  
  @appointmentsModule.Mutation('setApiTotalCount') public setApiTotalCount: any

  public confirm: boolean = false
  public contact_information: any = ''
  public minimized: boolean = false
  public title: any = ''
  public state: any = null
  public message: any = ''
  public fees: any = ''
  public feesOptions: any = [
    { text: 'No', value: 'false' },
    { text: 'Yes', value: 'true' },
    { text: 'HQ to Invoice', value: 'HQFin' }
  ]

  public added: any = 0
  public invoice: any = null
  public rate: any = null
  public start: any = ''
  public end: any = ''
  public other_recurring_start_time: any = null
  public other_recurring_end_time: any = null
  public other_recurring_start_date: any = null
  public other_recurring_end_date: any = null
  public other_recurring_display_time: any = null
  public other_recurring_display_date: any = null
  public other_selected_frequency: any = []
  public other_selected_weekdays: any = []
  public other_selected_count: any = ''
  public yearly: any = RRule.YEARLY
  public monthly: any = RRule.MONTHLY
  public weekly: any = RRule.WEEKLY
  public daily: any = RRule.DAILY
  public monday: any = RRule.MO
  public tuesday: any = RRule.TU
  public wednesday: any = RRule.WE
  public thursday: any = RRule.TH
  public friday: any = RRule.FR
  public other_single_event: any = true
  public other_recurring_event: any = true
  public other_rrule_text: any = ''
  public other_rrule_array: any = []
  public recurring_title: any = ''
  public recurring_contact_information: any = ''
  public recurring_fees: any = ''
  public single_input_boolean: any = false
  public recurring_input_boolean: any = false
  public recurring_form_state: any = ''
  public submitting_flag: any = false
  public start_time_msg: any = ''
  public end_time_msg: any = ''

  get modalVisible () {
    return this.showModal
  }

  set modalVisible (e) {
    this.toggleOtherBookingModal(e)
  }

  get startTime () {
    if (this.event && this.event.start) {
      return moment(this.event.start)
    }
    return ''
  }

  get endTime () {
    if (this.event && this.event.end) {
      // JSTOTS TOCHECK removed new from moment. no need to use new with moment
      const output = moment(this.event.end)
      output.add(this.added, 'hours')
      return output
    }
    return ''
  }

  get resource () {
    if (this.event && this.event.resource) {
      return this.event.resource
    }
    return ''
  }

  get duration () {
    return (this.endTime as any).diff(this.startTime, 'hours', true)
  }

  get displayDuration () {
    const output = this.duration.toFixed(1)
    return `${output} hrs`
  }

  hideCollapse (div_id) {
    const selectDivId = document.getElementById(div_id)

    if (selectDivId) {
      if (selectDivId.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', div_id)
      }
    }
  }

  showCollapse (div_id) {
    const selectDivId = document.getElementById(div_id)
    if (selectDivId) {
      if (selectDivId.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse', div_id)
      }
    }
  }

  cancel () {
    this.$root.$emit('removeSavedSelection')
    this.message = ''
    this.recurring_input_boolean = false
    this.single_input_boolean = false
    this.recurring_form_state = ''
    this.toggleOtherBookingModal(false)
  }

  show () {
    this.showCollapse('collapse-other-booking-event-selection')
    this.hideCollapse('collapse-single-event')
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    if (moment.isMoment(this.startTime)) {
      this.other_recurring_start_time = new Date(this.startTime.format())
    } else {
      this.other_recurring_start_time = new Date(this.startTime)
    }
    
    // JSTOTS TOCHECK removed new from moment. no need to use new with moment
    this.other_recurring_start_date = moment(this.startTime).clone()

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
  }

  incrementDuration () {
    if ((this.endTime as any).format('H') == 18) {
      return
    }
    this.added += 0.5
    if (this.selectionIndicator) {
      const event = this.getEvent()
      this.editSelection(event, 0.5)
    }
  }

  decrementDuration () {
    if (this.duration == 0.5) {
      return
    }
    this.added -= 0.5
    if (this.selectionIndicator) {
      const event = this.getEvent()
      this.editSelection(event, -0.5)
    }
  }

  postEvent (e) {
    e.preventDefault()
    this.setApiTotalCount(0)
    this.setApiTotalCount(this.other_rrule_array.length)
    this.submitting_flag = true
    const uuidv4 = require('uuid').v4
    const recurring_uuid = uuidv4()
    const self = this
    let sent_flag: number = 0
    if (this.other_rrule_array.length > 0) {
      showBookingFlagBus.$emit(ShowBookingFlagBusEvents.ShowBookingFlagEvent, true)
      this.other_rrule_array.forEach(date => {
        let st = moment(date.start).clone()
        let ed = moment(date.end).clone()
        const startOffice = moment.tz(st.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
        const endOffice = moment.tz(ed.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
        const booking = {
          room_id: self.resource.id,
          start_time:startOffice,
          end_time: endOffice,
          fees: self.recurring_fees,
          booking_name: self.recurring_title,
          booking_contact_information: self.recurring_contact_information,
          recurring_uuid: recurring_uuid
        }
        self.postBooking(booking).then(() => {
          sent_flag = sent_flag + 1
          apiProgressBus.$emit(APIProgressBusEvents.APIProgressEvent, sent_flag)
          if (sent_flag === this.other_rrule_array.length) {
              self.finishBooking()
              self.getBookings()
              showBookingFlagBus.$emit(ShowBookingFlagBusEvents.ShowBookingFlagEvent, false)
              this.setApiTotalCount(0) 
              setTimeout(function () {
                // I assume this is intentionally empty.
              }, 2000)
          }
        })
      })
      this.recurring_contact_information = ''
    }

    if (this.title.length > 0) {
      this.message = ''
      this.state = null
      // JSTOTS TOCHECK removed new from moment. no need to use new with moment
      let start = moment(this.startTime).utc()
     if (this.startTime) {
       start = moment.tz(this.startTime.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).utc()
     }

      // JSTOTS TOCHECK removed new from moment. no need to use new with moment
      let end = moment(this.endTime).utc()
      if (this.endTime) {
        end = moment.tz(this.endTime.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).utc()
      }

      const booking = {
        room_id: this.resource.id,
        start_time: start.format('YYYY-MM-DD[T]HH:mm:ssZ'),
        end_time: end.format('YYYY-MM-DD[T]HH:mm:ssZ'),
        fees: this.fees,
        booking_name: this.title,
        booking_contact_information: this.contact_information
      }
      this.postBooking(booking).then(() => {
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
    setTimeout(function () {
      self.toggleOtherBookingModal(false)
      self.toggleScheduling(false)
      self.getBookings()
      self.submitting_flag = false
    }, 2000)
  }

  setSingle () {
    this.hideCollapse('collapse-single-event')
    this.other_single_event = !this.other_single_event
    this.title = ''
    this.contact_information = ''
    this.fees = ''
    this.recurring_form_state = ''
  }

  setRecurring () {
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
  }

  formatStartDate (date) {
    return moment(date).format('YYYY-MM-DD HH:mm')
  }

  formatEndDate (date) {
    return moment(date).clone().format('HH:mm')
  }

  generateRule () {
    let validate_flag =false
    this.start_time_msg = ''
    this.end_time_msg = ''
    const recurring_start_time_obj = this.convertTimePickerValue(this.other_recurring_start_time)
    const recurring_end_time_obj = this.convertTimePickerValue(this.other_recurring_end_time)

    if (recurring_start_time_obj) {
      if ((new Date(recurring_start_time_obj).getHours() <= 8) || (new Date(recurring_start_time_obj).getHours() >= 17)){
        if ((new Date(recurring_start_time_obj).getHours() === 8)) {
          if ((new Date(recurring_start_time_obj).getMinutes() < 30)) {
              this.start_time_msg = "Time not allowed"
              this.other_recurring_start_time = null
              validate_flag = true
          } else {
            this.start_time_msg = ''
          }
        } else if (new Date(recurring_start_time_obj).getHours() === 17) {
          if ((new Date(recurring_start_time_obj).getMinutes() > 0)) {
              this.other_recurring_start_time = null
              this.start_time_msg = "Time not allowed"
              validate_flag = true
          } else {
            this.start_time_msg = ''
          }
        } else {
          this.start_time_msg = "Time not allowed"
          this.other_recurring_start_time = null
          validate_flag = true
        }
      }
    }
    if (recurring_end_time_obj) {
      if ((new Date(recurring_end_time_obj).getHours() <= 8) || (new Date(recurring_end_time_obj).getHours() >= 17)){
        if ((new Date(recurring_end_time_obj).getHours() === 8)) {
          if ((new Date(recurring_end_time_obj).getMinutes() < 30)) {
              this.end_time_msg = "Time not allowed"
              this.other_recurring_end_time = null
              validate_flag = true
          } else {
            this.end_time_msg = ''
            validate_flag = false
          }
        } else if (new Date(recurring_end_time_obj).getHours() === 17) {
          if ((new Date(recurring_end_time_obj).getMinutes() > 0)) {
              this.end_time_msg = "Time not allowed"
              this.other_recurring_end_time = null
              validate_flag = true
          } else {
            this.end_time_msg = ''
            validate_flag = false
          }
        } else {
          this.end_time_msg = "Time not allowed"
          this.other_recurring_end_time = null
          validate_flag = true
        }
      }
    }
    if (validate_flag) {
      this.recurring_form_state = ''
      return false
    }
    this.other_single_event = true
    this.other_recurring_event = true
    //365 DAYS VALIDATION
    const a = moment(this.other_recurring_start_date)
    const b = moment(this.other_recurring_end_date)
    const diffDays = b.diff(a, 'days')
   
    if (diffDays > 364) {
      this.other_recurring_start_date = null
      this.other_recurring_end_date = null
      this.hideCollapse('collapse-recurring-event')
      this.hideCollapse('collapse-other-booking-event-selection')
      this.showCollapse('date-limit')
      this.recurring_form_state = ''
      return false
    }
    // Commented out start/end variables are for testing 5pm pst -> utc conversion bug
    // Removed these variables from the date_start and until variable declarations
    const other_recurring_start_date = moment.tz(moment(this.other_recurring_start_date).format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
    const start_year = parseInt(moment(other_recurring_start_date).utc().clone().format('YYYY'))
    const start_month = parseInt(moment(other_recurring_start_date).utc().clone().format('MM'))
    const start_day = parseInt(moment(other_recurring_start_date).utc().clone().subtract(4, 'hours').format('DD'))
    const other_recurring_start_time = moment.tz(moment(recurring_start_time_obj).format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
    const local_start_hour = parseInt(moment(other_recurring_start_time).clone().format('HH'))
    const local_start_minute = parseInt(moment(other_recurring_start_time).clone().format('mm'))
    const other_recurring_end_date_obj = moment(this.other_recurring_end_date).clone()
    const other_recurring_end_date = moment.tz(other_recurring_end_date_obj.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
    const end_year = parseInt(moment(other_recurring_end_date).utc().clone().format('YYYY'))
    const end_month = parseInt(moment(other_recurring_end_date).utc().clone().format('MM'))
    const end_day = parseInt(moment(other_recurring_end_date).utc().clone().format('DD'))
    const other_recurring_end_time_obj = moment(recurring_end_time_obj).clone()
    const other_recurring_end_time = moment.tz(other_recurring_end_time_obj.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
    const local_end_hour = parseInt(moment(other_recurring_end_time).clone().format('HH'))
    const local_end_minute = parseInt(moment(other_recurring_end_time).clone().format('mm'))
    let input_frequency: any = null
    const local_other_dates_array: any = []

    switch (this.other_selected_frequency[0]) {
      case 0:
        input_frequency = RRule.YEARLY
        break
      case 1:
        input_frequency = RRule.MONTHLY
        break
      case 2:
        input_frequency = RRule.WEEKLY
        break
      case 3:
        input_frequency = RRule.DAILY
        break
    }

    if (!isNaN(start_year) || !isNaN(end_year)) {
      // IF RRule Breaks, this is where it will happen
      const date_start = new Date(start_year+'/'+start_month+'/'+start_day)
      let until = new Date(end_year+'/'+end_month+'/'+end_day)
      const rule = new RRule({
        freq: input_frequency,
        count: this.other_selected_count,
        byweekday: this.other_selected_weekdays,
        dtstart: date_start,
        until: until
      })

      const array = rule.all()
      this.other_rrule_text = rule.toText()
      // JSTOTS added typr for this.startTime
      const first_event_start_day: any = moment(this.startTime).clone().set({ hour: local_start_hour, minute: local_start_minute }).add(new Date((this.startTime as any)).getTimezoneOffset(), 'minutes')
      let num_days = Math.floor(moment.duration(first_event_start_day.diff(moment(new Date()))).asDays())
      array.forEach(date => {
          const date_with_offset = moment(date).clone().set({ hour: local_start_hour, minute: local_start_minute }).add(new Date(date).getTimezoneOffset(), 'minutes')
          if (local_start_hour >= 8 && local_start_hour < 16) {
            date_with_offset.add(1, 'd')
          }
          const formatted_start_date = moment(date).clone().set({ hour: local_start_hour, minute: local_start_minute }).format('YYYY-MM-DD HH:mm:ssZ')
          if (num_days < 0) {
            num_days = 0
          }
          const formatted_end_date = moment(date).clone().set({ hour: local_end_hour, minute: local_end_minute }).format('YYYY-MM-DD HH:mm:ssZ')
          local_other_dates_array.push({ start: formatted_start_date, end: formatted_end_date })
      })

    }
    this.other_rrule_array = local_other_dates_array
    this.other_selected_count = ''
    this.other_selected_weekdays = []
    this.other_selected_frequency = []
    this.other_recurring_start_date = ''
    this.other_recurring_start_time = null
    this.other_recurring_end_date = ''
    this.other_recurring_end_time = null
    this.showCollapse('collapse-other-event-audit')
    this.hideCollapse('collapse-other-booking-event-selection')
    this.hideCollapse('collapse-recurring-event')
    this.recurring_form_state = 'audit'
  }

  checkRecurringInput () {
    if (this.other_selected_frequency.length > 0 && this.other_recurring_end_date !== null &&
      this.other_recurring_end_time !== null && this.recurring_title !== '' && this.recurring_fees !== '') {
      this.recurring_input_boolean = true
      this.recurring_form_state = 'rule_generated'
    } else {
      this.recurring_input_boolean = false
    }
  }

  checkSingleInput () {
    if (this.contact_information !== '' && this.title !== '' && this.fees !== '') {
      this.single_input_boolean = true
    } else {
      this.single_input_boolean = false
    }
  }

  convertTimePickerValue(model:any){
    const currentDate = new Date()
    const fullformat = moment(model.hh + ':' + model.mm + ' ' + model.A ,'hh:mm A').format('HH:mm:ss')
    const day = currentDate.getDate().toString().length === 1 ? '0' + currentDate.getDate().toString() : currentDate.getDate().toString()
    const month = currentDate.getMonth().toString().length === 1 ? '0' + (currentDate.getMonth() + 1).toString() : (currentDate.getMonth() + 1).toString()
    const year = currentDate.getFullYear()
    return new Date(year + '-' + month + '-' + day + ' ' + fullformat)
  }
}
</script>
<style scoped>
.danger {
  color: red !important;
}
</style>

