<template>
  <b-modal
    v-model="modal"
    hide-header
    size="md"
    modal-class="q-modal"
    body-class="q-modal"
    no-close-on-backdrop
    no-close-on-esc
    @shown="show"
  >
    <template slot="modal-footer">
      <div class="d-flex flex-row-reverse">
        <b-button
          v-if="
            this.recurring_input_state === 'notes' ||
            this.single_input_state === 'notes'
          "
          variant="primary"
          class="ml-2"
          size="md"
          @click="deleteApptWarning"
        >
          Submit</b-button
        >
        <b-button
          v-else-if="this.stat_submit"
          variant="primary"
          class="ml-2"
          size="md"
          @click="statSubmit"
        >
          Submit</b-button
        >
        <b-button v-else class="ml-2" size="md" disabled> Submit </b-button>
        <b-button
          v-if="this.recurring_input_state === 'event_information'"
          variant="primary"
          class="w-100 ml-2"
          size="md"
          v-b-toggle.recurring-dates-collapse
          @click="generateRule"
        >
          Next
        </b-button>
        <b-button
          v-else-if="(this.single_input_state === 'event_information') && (this.show_next)"
          variant="primary"
          class="w-100 ml-2"
          size="md"
          @click="nextSingleNotes"
        >
          Next
        </b-button>
        <b-button
          v-else-if="(this.recurring_input_state === 'audit_information') && (this.show_next)"
          variant="primary"
          class="w-100 ml-2"
          size="md"
          @click="nextRecurringNotes"
        >
          Next
        </b-button>
        <b-button
          v-else-if="
            (this.single_input_state === 'notes' ||
            this.recurring_input_state === 'notes')  && (this.show_next)
          "
          disabled
          class="w-100 ml-2"
          size="md"
        >
          Next
        </b-button>
        <b-button
          v-else-if="(this.show_stat_next)"
          variant="primary"
          class="w-100 ml-2"
          size="md"
          @click="nextStat"
        >
          Next
        </b-button>
        <b-button @click="cancel" size="md"> Cancel </b-button>
      </div>
    </template>
    <span style="font-size: 1.75rem">Schedule Appointment Blackout</span><br />
    <b-form>
      <b-collapse id="collapse-event-selection">
        <b-card>
          <b-form-row class="mb-2">
            <label for="event-selection">Step 1: Select Event Type</label>
          </b-form-row>
          <b-form-row>
            <b-col class="w-50 mb-1">
              <b-button
                variant="primary"
                class="w-100 mb-1"
                v-b-toggle.collapse-single-event
                @click="setRecurring"
                size="lg"
                id="create-single-blackout"
              >
                Create Single Blackout
              </b-button>
            </b-col>
            <b-col v-if="is_recurring_enabled" class="w-50">
              <b-button
                variant="primary"
                class="w-100 mb-1"
                v-b-toggle.collapse-recurring-events
                @click="setSingle"
                size="lg"
                id="create-recurring-blackout"
              >
                Create Recurring Blackout
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col v-if="is_Support" class="w-50">
              <b-button
                variant="primary"
                class="w-100 mb-1"
                size="lg"
                v-b-toggle.collapse-recurring-stat
                @click="setSTAT"
                id="create-stat"
              >
                Create STAT
              </b-button>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-single-event">
        <v-card class="mt-2 mb-2">
          <v-container>
          <b-form-row style="justify-content: center">
            <h4>Single Event</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label stlye="font-weight: bold;">Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label for="user-name">User Name</label><br />
              <b-form-input id="user-name" v-model="this.user_name" disabled />
            </b-col>
            <b-col cols="6">
              <label for="contact-info">Contact Information (optional)</label>
              <b-form-input id="contact-info" v-model="this.user_contact_info" />
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label for="blackout-date">Blackout Date:</label>
                <font-awesome-icon
                  v-if="this.blackout_date !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <DatePicker
                  id="blackout-date"
                  v-model="blackout_date"
                  id="appointment_blackout_date"
                  type="date"
                  lang="en"
                  class="w-100"
                  @change="checkSingleInput"
                  @input="checkSingleInput"
                  @clear="checkSingleInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label for="appointment_blackout_start_time" >Blackout Start Time:</label>
                <font-awesome-icon
                  v-if="this.start_time !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <vue-timepicker
                    v-model="start_time"
                    id="appointment_blackout_start_time"
                    class="w-100"
                    icon="clock"
                    editable
                    format="hh:mm A"
                    locale="en-US"
                    @change="checkSingleInput"
                    @input="checkSingleInput"
                    @clear="checkSingleInput"
                    manual-input>
                </vue-timepicker>
                <br/>
                <span class="danger" v-if="start_time_msg">{{start_time_msg}}</span>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label for="appointment_blackout_end_time">Blackout End Time:</label>
                <font-awesome-icon
                  v-if="this.end_time !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                  <vue-timepicker
                      v-model="end_time"
                      id="appointment_blackout_end_time"
                      class="w-100"
                      icon="clock"
                      editable
                      format="hh:mm A"
                      locale="en-US"
                      @change="checkSingleInput"
                      @input="checkSingleInput"
                      @clear="checkSingleInput"
                      manual-input>
                  </vue-timepicker>
                <br/>
                <span class="danger" v-if="end_time_msg">{{end_time_msg}}</span>
              </b-form-group>
            </b-col>
          </b-form-row>
          </v-container>
        </v-card>
      </b-collapse>
      <b-collapse id="collapse-recurring-events">
        <b-card class="mt-2">
          <b-form-row style="justify-content: center">
            <h4>Recurring Event</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label for="recurring-event-info" style="font-weight: bold">Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label for="user-name-recurring" >User Name:</label><br />
              <b-form-input id="user-name-recurring" v-model="this.user_name" disabled />
            </b-col>
            <b-col cols="6">
              <label for="contact-info-recurring" >Contact Information (optional):</label>
              <b-form-input id="contact-info-recurring" v-model="this.user_contact_info" />
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label for="recurring_blackout_start_time">Blackout Start Time:</label>
                <font-awesome-icon
                  v-if="this.recurring_start_time !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                  <vue-timepicker
                      v-model="recurring_start_time"
                      id="recurring_blackout_start_time"
                      class="w-100"
                      icon="clock"
                      editable
                      format="hh:mm A"
                      locale="en-US"
                      @change="checkRecurringInput"
                      @input="checkRecurringInput"
                      @clear="checkRecurringInput"
                      manual-input>
                  </vue-timepicker>
                  <br/>
                  <span class="danger" v-if="reccuring_start_time_msg">{{reccuring_start_time_msg}}</span>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label for="recurring_blackout_end_time">Blackout End Time:</label>
                <font-awesome-icon
                  v-if="this.recurring_end_time !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                  <vue-timepicker
                      v-model="recurring_end_time"
                      id="recurring_blackout_end_time"
                      class="w-100"
                      icon="clock"
                      editable
                      format="hh:mm A"
                      locale="en-US"
                      @change="checkRecurringInput"
                      @input="checkRecurringInput"
                      @clear="checkRecurringInput"
                      >
                  </vue-timepicker>
                  <br/>
                  <span class="danger" v-if="reccuring_end_time_msg">{{reccuring_end_time_msg}}</span>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label for="recurring_start_date">Blackout Start Date:</label>
                <font-awesome-icon
                  v-if="this.recurring_start_date !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <DatePicker
                  id="recurring_start_date"
                  class="w-100"
                  lang="en"
                  v-model="recurring_start_date"
                  placeholder="Select Start Date"
                  @change="checkRecurringInput"
                  @input="checkRecurringInput"
                  @clear="checkRecurringInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label for="recurring_end_date">Blackout End Date:</label>
                <font-awesome-icon
                  v-if="this.recurring_end_date !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <DatePicker
                  id="recurring_end_date"
                  class="w-100"
                  lang="en"
                  v-model="recurring_end_date"
                  placeholder="Select End Date"
                  @change="checkRecurringInput"
                  @input="checkRecurringInput"
                  @clear="checkRecurringInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-form-group class="mt-0 ml-1">
              <fieldset>
              <legend>Frequency:</legend>
              <font-awesome-icon
                v-if="this.selected_frequency.length === 1"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <font-awesome-icon
                v-if="this.selected_frequency.length > 1"
                icon="exclamation-triangle"
                style="font-size: 1rem; color: #ffc32b"
              />
              <b-form-checkbox-group
                id="frequency-checkboxes"
                v-model="selected_frequency"
                @input="checkRecurringInput"
              >
                <b-form-checkbox :value="weekly">Weekly</b-form-checkbox>
                <b-form-checkbox :value="daily">Daily</b-form-checkbox>
              </b-form-checkbox-group>
              </fieldset>
            </b-form-group>
          </b-form-row>
          <b-form-group>
            <fieldset>
            <legend>Select Weekdays:</legend>
            <font-awesome-icon
              v-if="this.selected_weekdays.length >= 1"
              icon="check"
              style="font-size: 1rem; color: green"
            />
            <b-form-checkbox-group
              id="weekday-checkboxes"
              v-model="selected_weekdays"
              @input="checkRecurringInput"
            >
              <b-form-checkbox :value="monday">Mon.</b-form-checkbox>
              <b-form-checkbox :value="tuesday">Tues.</b-form-checkbox>
              <b-form-checkbox :value="wednesday">Wed.</b-form-checkbox>
              <b-form-checkbox :value="thursday">Thurs.</b-form-checkbox>
              <b-form-checkbox :value="friday">Fri.</b-form-checkbox>
            </b-form-checkbox-group>
            </fieldset>
          </b-form-group>
          <b-form-group>
            <b-form-row>
              <label for="occurrences-input" style="font-weight: bold" class="mt-0"
                >Number of Occurences(optional):
              </label>
              <span v-if="this.selected_count !== ''"
                >&nbsp; Limited to {{ this.selected_count }} occurences.</span
              >
              <font-awesome-icon
                v-if="this.selected_count !== ''"
                icon="check"
                style="font-size: 1rem; color: green"
                class="ml-1"
              />
            </b-form-row>
            <b-form-row>
              <b-col cols="6">
                <b-form-input
                  id="occurrences-input"
                  type="number"
                  class="mb-1 w-100"
                  v-model="selected_count"
                />
              </b-col>
            </b-form-row>
          </b-form-group>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-recurring-stat">
        <v-card class="mt-2">
          <v-container>
          <b-form-row style="justify-content: center">
            <h4>Recurring STAT</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <h5 style="font-weight: bold">Step 2: STAT Information</h5>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label for="stat_user_name">User Name:</label><br />
              <b-form-input id="stat_user_name" v-model="this.stat_user_name" disabled />
            </b-col>
            <b-col cols="6">
              <label for="user_contact_info" >Contact Information (optional):</label>
              <b-form-input id="user_contact_info" v-model="this.user_contact_info" />
            </b-col>
          </b-form-row>
          <b-form-row>
              <b-form-group label="STAT Date/s">
                <div
                  v-for="(input, index) in stat_dates"
                  :key="`stat_dates-${index}`"
                >
                <b-form-row>
                  <b-col cols="6">
                    <DatePicker
                        v-model="input.value"
                        id="appointment_stat_date"
                        type="date"
                        lang="en"
                        class="w-100"
                        :inline="true"
                        @change="checkStatInput"
                        @input="checkStatInput"
                        @clear="checkStatInput"
                      >
                      </DatePicker>
                  </b-col>
                  <b-col cols="6">
                    <b-form-input maxlength="255" v-model="input.note" placeholder="Note"/>
                  </b-col>
                </b-form-row>
                <b-form-row>
                  <b-col cols="1">
                    <font-awesome-icon
                      v-if="input.value"
                      icon="check"
                      style="font-size: 1rem; color: green"
                    />
                  </b-col>
                  <b-col cols="1">
                    <!--   Remove Icon-->
                    <b-button
                    variant="outline-danger"
                    pill
                    size="sm"
                    v-show="stat_dates.length > 1"
                    @click="removeField(index, stat_dates)"
                    >
                      <font-awesome-icon
                          icon="eraser"
                          style="font-size: 1rem; color: red"
                        />
                    </b-button>
                  </b-col>
                  <b-col cols="1">
                    <!--   Add Icon-->
                    <b-button
                    variant="outline-primary"
                    pill
                    size="sm"
                    v-show="(stat_dates.length === (index+1))"
                     @click="addField(input, stat_dates)"
                    >
                      <font-awesome-icon
                          icon="plus"
                          style="font-size: 1rem; color: blue"
                        />
                    </b-button>
                  </b-col>
                </b-form-row>
                <b-form-row v-if="(show_stat_next) && ((stat_dates.length === (index+1)))">
                  <!-- only add to current office -->
                  <b-col>
                    <b-form-checkbox-group
                        v-model="only_this_office"
                        @input="checkRecurringInput"
                      >
                        <b-form-checkbox :value="true">Only this Office</b-form-checkbox>
                    </b-form-checkbox-group>
                  </b-col>
                  <b-col>
                    <b-form-checkbox-group
                      v-if="only_this_office.length"
                        v-model="only_appointments"
                        @input="checkRecurringInput"
                      >
                        <b-form-checkbox :value="true">Only appointment</b-form-checkbox>
                    </b-form-checkbox-group>
                  </b-col>
                </b-form-row>
              </div>
              </b-form-group>
          </b-form-row>
          </v-container>
        </v-card>
      </b-collapse>
      <b-collapse id="date-limit">
        <b-card class="mb-2">
          <b-card-body>
            <b-form-row class="mb-2">
              <p stlye="font-weight: bold;" class="text-danger"
              >Cannot blackout more that 1 year at Once.
              </p
              >
            </b-form-row>
          </b-card-body>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-information-audit">
        <b-card class="mb-2">
          <b-form-group>
            <b-form-row style="justify-content: center">
              <h4 v-if="!is_stat">Recurring Event</h4>
              <h4 v-else>Recurring STAT</h4>
            </b-form-row>
            <b-form-row class="mb-2">
              <p stlye="font-weight: bold;"
                v-if="!is_stat">Step 2 (continued): Confirm Recurring Event Dates</p
              >
              <p stlye="font-weight: bold;"
                v-else>Step 2 (continued): Confirm Recurring STAT Dates</p
              >
            </b-form-row>
            <b-form-row>
              <b-col cols="12">
                <b-button
                  variant="primary"
                  class="w-100 mb-2"
                  v-b-toggle.recurring-rule-collapse
                >
                  <span v-if="!is_stat">View Recurring Event Info</span>
                  <span v-else>View Recurring Event Info</span>
                </b-button>
              </b-col>
            </b-form-row>
            <b-form-row class="mb-0">
              <b-collapse
                id="recurring-rule-collapse"
                class="mb-2 ml-2"
                visible
              >
               <span v-if="!is_stat">{{ this.rrule_text }}</span>
               <span v-else>All selected dates for all office</span>
              </b-collapse>
            </b-form-row>
            <b-form-row>
              <b-col cols="12">
                <b-button
                  variant="primary"
                  class="w-100 mb-2"
                  v-b-toggle.recurring-dates-collapse
                >
                  View Recurring Dates ({{ this.rrule_array.length }})
                </b-button>
              </b-col>
            </b-form-row>
            <b-form-row>
              <b-collapse id="recurring-dates-collapse" class="mb-2">
                <div style="height: 75px; overflow-y: scroll; margin: 0px" v-if="!is_stat">
                  <ul
                    class="list-group"
                    v-for="date in this.rrule_array"
                    style="justify-content: center"
                    :key="date.start"
                  >
                    <li class="list-group-item">
                      <strong>Event:</strong> {{ formatStartDate(date.start) }} until
                    </li>
                  </ul>
                </div><div style="height: 75px; overflow-y: scroll; margin: 0px" v-else>
                  <ul
                    class="list-group"
                    v-for="(value, index) in this.rrule_array"
                    style="justify-content: center"
                    :key="index"
                  >
                    <li class="list-group-item">
                      <strong>STAT:</strong> {{ formatDate(value.value) }} whole Day for all office.
                    </li>
                  </ul>
                </div>
              </b-collapse>
            </b-form-row>
          </b-form-group>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-blackout-notes">
        <v-card class="mt=2">
          <v-container>
          <b-form-row style="justify-content: center">
            <h4 v-if="this.single_input_boolean">Single Event</h4>
            <h4 v-if="this.recurring_input_boolean">Recurring Event</h4>
          </b-form-row>
          <b-form-row>
            <p
              v-if="this.recurring_input_boolean"
              stlye="font-weight: bold;"
            >
              Step 3 (optional): Event Notes. <br />
            </p>
            <p v-if="this.single_input_boolean" stlye="font-weight: bold;">
              Step 2 (optional): Event Notes. <br />
            </p>
            <font-awesome-icon
              v-if="this.notes !== ''"
              icon="check"
              style="font-size: 1rem; color: green"
            />
          </b-form-row>
          <b-form-row>
            <b-textarea
              v-model="notes"
              id="single_appointment_blackout_notes"
              placeholder="Enter notes about blackout period"
              rows="3"
              maxlength="255"
              max-rows="6"
              size="md"
            >
            </b-textarea>
          </b-form-row>
          </v-container>
        </v-card>
      </b-collapse>
    </b-form>
    <v-dialog
      v-model="confirmDialog"
      max-width="400"
    >
      <v-card>
        <v-card-title class="headline">
         Warning
        </v-card-title>
        <v-card-text>
          {{ this.warning_text }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red darken-1"
            text
            @click="confirmBlackout(false)"
          >
            No
          </v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="confirmBlackout(true)"
          >
            Yes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </b-modal>
</template>

<script lang="ts">
/* eslint-disable */
import { Component, Vue } from 'vue-property-decorator'
import { Action, State, namespace } from 'vuex-class'
import { apiProgressBus, APIProgressBusEvents } from '../../../events/progressBus'
import { showFlagBus, ShowFlagBusEvents } from '../../../events/showFlagBus'
import DatePicker from 'vue2-datepicker'
import VueTimepicker from 'vue2-timepicker'
import { RRule } from 'rrule'
import moment from 'moment'
import 'vue2-datepicker/index.css'
import 'vue2-timepicker/dist/VueTimepicker.css'

const appointmentsModule = namespace('appointmentsModule')

@Component({
  components: {
    DatePicker,
    VueTimepicker
  }
})

export default class AppointmentBlackoutModal extends Vue {
  
  @State('roomResources') private roomResources!: any
  @appointmentsModule.State('showAppointmentBlackoutModal') private showAppointmentBlackoutModal!: any
  @appointmentsModule.State('appointments') private myappointments!: any

  @appointmentsModule.Getter('is_recurring_enabled') private is_recurring_enabled!: any;
  @appointmentsModule.Getter('is_Support') private is_Support!: any;

  @appointmentsModule.Action('getAppointments') public getAppointments: any
  @appointmentsModule.Action('postAppointment') public postAppointment: any
  @appointmentsModule.Action('createAxioObject') public createAxioObject: any
  @appointmentsModule.Action('callBulkAxios') public callBulkAxios: any
  @appointmentsModule.Action('createStatAxioObject') public createStatAxioObject: any

  @appointmentsModule.Mutation('toggleAppointmentBlackoutModal') public toggleAppointmentBlackoutModal: any
  @appointmentsModule.Mutation('setApiTotalCount') public setApiTotalCount: any

  @Action('postBookingStat') public postBookingStat: any
  @Action('getOffices') public getOffices: any
  @Action('getBookings') public getBookings: any
  @Action('getOfficeRooms') public getOfficeRooms: any

  public blackout_date: any = null
  public start_time: any = null
  public end_time: any = null
  public notes: any = ''
  public user_name: any = ''
  public stat_user_name: any = ''
  public user_contact_info: any = ''
  public selected_frequency: any = []
  public selected_weekdays: any = []
  public selected_count: any = ''
  public recurring_start_time: any = null
  public recurring_end_time: any = null
  public recurring_start_date: any = null
  public recurring_end_date: any = null
  public recurring_array: any = ''
  public yearly: any = RRule.YEARLY
  public monthly: any = RRule.MONTHLY
  public weekly: any = RRule.WEEKLY
  public daily: any = RRule.DAILY
  public monday: any = RRule.MO
  public tuesday: any = RRule.TU
  public wednesday: any = RRule.WE
  public thursday: any = RRule.TH
  public friday: any = RRule.FR
  public single_blackout_boolean: any = true
  public recurring_blackout_boolean: any = true
  public rrule_array: any = []
  public filtered_appt: any = []
  public filtered_appt_start: any = []
  public filtered_appt_end: any = []
  public rrule_text: any = ''
  public recurring_input_boolean: any = false
  public single_input_boolean: any = false
  public next_boolean: any = false
  public single_input_state: any = ''
  public recurring_input_state: any = ''
  public warning_text: any = ''
  private confirmDialog: boolean = false
  public appt_overlap: any = 0
  public api_count: any = 0
  public show_next: boolean = true
  public stat_dates: any = [{note:""}]
  public show_stat_next: boolean = false
  public is_stat: boolean = false
  public stat_submit: boolean = false
  public only_this_office: any = []
  public only_appointments: any = []
  public reccuring_start_time_msg: any =''
  public reccuring_end_time_msg: any =''
  public start_time_msg: any =''
  public end_time_msg: any =''
  

  get modal () {
    return this.showAppointmentBlackoutModal
  }

  set modal (e) {
    this.toggleAppointmentBlackoutModal(e)
  }

  hideCollapse (div_id) {
    const elementDivId = document.getElementById(div_id)
    if (elementDivId) {
      if (elementDivId.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', div_id)
      }
    }
  }
  showCollapse (div_id) {
    const elementDivId = document.getElementById(div_id)
    if (elementDivId) {
      if (elementDivId.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse',
          div_id)
      }
    }
  }
   addField(value, fieldType) {
      fieldType.push({ value: "" });
    }
    
    removeField(index, fieldType) {
      fieldType.splice(index, 1);
    }
  show () {
    this.showCollapse('collapse-event-selection')
    this.hideCollapse('collapse-single-event')
    this.hideCollapse('collapse-information-audit')
    this.hideCollapse('collapse-blackout-notes')
    this.hideCollapse('date-limit')
    // clear single event information
    this.start_time = null
    this.end_time = null
    this.blackout_date = null

    // clear recurring event information
    this.recurring_start_date = null
    this.recurring_end_date = null
    this.recurring_start_time = null
    this.recurring_end_time = null
    this.selected_frequency = []
    this.selected_weekdays = []
    this.selected_count = ''
    this.notes = ''
  }

  cancel () {
    this.recurring_blackout_boolean = true
    this.single_blackout_boolean = true
    this.single_input_boolean = false
    this.recurring_input_boolean = false
    this.rrule_text = ''
    this.rrule_array = []
    this.stat_dates = [{note:""}]
    this.toggleAppointmentBlackoutModal(false)
    this.show_stat_next = false
    this.is_stat = false
    this.stat_submit = false
  }

  private async confirmBlackout (isAgree: boolean) {
    if (isAgree) {
      this.submit()
    } else {
      this.rrule_text = ''
      this.rrule_array = []
      this.recurring_input_state = ''
      this.single_input_boolean = ''
    }
    this.confirmDialog = false
    this.toggleAppointmentBlackoutModal(false);
  }

  private async countApptWarning (e) {
    this.filtered_appt = this.myappointments.filter(appt => appt.blackout_flag === 'N' && (!appt.stat_flag) &&
                                                    moment(appt.start_time).format('YYYY-MM-DD HH:mm:ssZ') >= e.start_time &&
                                                    moment(appt.end_time).format('YYYY-MM-DD HH:mm:ssZ') <= e.end_time)
    
    this.filtered_appt_start = this.myappointments.filter(appt => appt.blackout_flag === 'N' && (!appt.stat_flag) &&
                                                          moment(appt.start_time).format('YYYY-MM-DD HH:mm:ssZ') < e.start_time &&
                                                          moment(appt.end_time).format('YYYY-MM-DD HH:mm:ssZ') > e.start_time)
    
    this.filtered_appt_end = this.myappointments.filter(appt => appt.blackout_flag === 'N' && (!appt.stat_flag) &&
                                                        moment(appt.start_time).format('YYYY-MM-DD HH:mm:ssZ') < e.end_time &&
                                                        moment(appt.end_time).format('YYYY-MM-DD HH:mm:ssZ') > e.end_time)
    this.appt_overlap = this.appt_overlap + this.filtered_appt.length + this.filtered_appt_start.length + this.filtered_appt_end.length
  }

  deleteApptWarning () {
    // INC0056259 - Popup Warning message before committing Blackouts
    this.appt_overlap = 0
    const start_time = (this.start_time && this.start_time.hh) ? this.convertTimePickerValue(this.start_time) : this.start_time
    const end_time = (this.end_time && this.end_time.hh) ? this.convertTimePickerValue(this.end_time) : this.end_time

    const date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
    const start = moment(start_time).clone().format('HH:mm:ss')
    const start_date = moment(date + ' ' + start).format('YYYY-MM-DD HH:mm:ssZ')
    const end = moment(end_time).clone().format('HH:mm:ss')
    const end_date = moment(date + ' ' + end).format('YYYY-MM-DD HH:mm:ssZ')
    const uuidv4 = require('uuid').v4
    const recurring_uuid = uuidv4()
    if (this.rrule_array.length > 0) {
      this.rrule_array.forEach(item => {
        const e: any = {
          start_time: item.start,
          end_time: item.end,
          citizen_name: this.user_name,
          contact_information: this.user_contact_info,
          blackout_flag: 'Y',
          recurring_uuid: recurring_uuid
        }
        if (this.notes) {
          e.comments = this.notes
        }
        this.countApptWarning(e)
      })
    } else if (this.rrule_array.length === 0) {
      const e: any = {
        start_time: start_date,
        end_time: end_date,
        citizen_name: this.user_name,
        contact_information: this.user_contact_info,
        blackout_flag: 'Y'
      }
      if (this.notes) {
        e.comments = this.notes
      }
      this.countApptWarning(e)
    }
    if (this.appt_overlap > 0) {
      this.warning_text = "There is " + this.appt_overlap + " appointment(s) which is overlapping with this Blackout. Are you sure you want to create the Blackout?"
      this.confirmDialog=true;
    } else {
      this.submit()
    }
  }
  private delay(ms: number) {
      return new Promise(resolve => setTimeout(resolve, ms));
  }

  async bulkApiCall(axiosArray, flag=false) {
    const res = await this.callBulkAxios({'axiosArray': axiosArray, 'flag': flag})
    if (res) {
      apiProgressBus.$emit(APIProgressBusEvents.APIProgressEvent, axiosArray.length)
      await this.delay(3000)
      showFlagBus.$emit(ShowFlagBusEvents.ShowFlagEvent, false)
      this.getAppointments()
      this.getBookings()
      this.setApiTotalCount(0)
    } else {
      apiProgressBus.$emit(APIProgressBusEvents.APIProgressEvent, axiosArray.length)
      await this.delay(50000)
    }
  }

  async submit () {
    const start_time = (this.start_time && this.start_time.hh) ? this.convertTimePickerValue(this.start_time) : this.start_time
    const end_time = (this.end_time && this.end_time.hh) ? this.convertTimePickerValue(this.end_time) : this.end_time
    this.setApiTotalCount(0)
    this.setApiTotalCount(this.rrule_array.length)
    showFlagBus.$emit(ShowFlagBusEvents.ShowFlagEvent, true)
    // this is the number of api in a group- for bulk api call
    const limit = 50
    const date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
    const start = moment(start_time).clone().format('HH:mm:ss')
    const end = moment(end_time).clone().format('HH:mm:ss')
    const start_date = moment.tz(date + ' ' + start, this.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
    const end_date = moment.tz(date + ' ' + end, this.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
    const uuidv4 = require('uuid').v4
    const recurring_uuid = uuidv4()
    let axiosArray: any = []
    let rrule_ind = 0
    if (this.rrule_array.length > 0) {
       this.rrule_array.forEach(item => {
        rrule_ind += 1
        const startDateR = moment(item.start).clone().format('YYYY-MM-DD')
        const startTimeR = moment(item.start).clone().format('HH:mm:ss')
        const endDateR = moment(item.end).clone().format('YYYY-MM-DD')
        const endTimeR = moment(item.end).clone().format('HH:mm:ss')
        const e: any = {
          start_time: moment.tz(startDateR + ' ' + startTimeR, this.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
          end_time: moment.tz(endDateR + ' ' + endTimeR, this.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
          citizen_name: this.user_name,
          contact_information: this.user_contact_info,
          blackout_flag: 'Y',
          recurring_uuid: recurring_uuid
        }
        if (this.notes) {
          e.comments = this.notes
        }
        axiosArray.push(this.createAxioObject(e))
        if ((axiosArray.length == limit)) {
            this.bulkApiCall(axiosArray)
            axiosArray = []
        } else if (rrule_ind == this.rrule_array.length) {
          this.bulkApiCall(axiosArray, true)
          axiosArray = [] 
        }        
      })
    } else if (this.rrule_array.length === 0) {
      const e: any = {
        start_time: start_date,
        end_time: end_date,
        citizen_name: this.user_name,
        contact_information: this.user_contact_info,
        blackout_flag: 'Y'
      }
      if (this.notes) {
        e.comments = this.notes
      }
      this.postAppointment(e)
      apiProgressBus.$emit(APIProgressBusEvents.APIProgressEvent, this.rrule_array.length)
      this.getAppointments()
      await this.delay(3000)
      showFlagBus.$emit(ShowFlagBusEvents.ShowFlagEvent, false)
    }

    this.recurring_blackout_boolean = true
    this.single_blackout_boolean = true
    this.getAppointments()
    this.toggleAppointmentBlackoutModal(false)
    this.rrule_text = ''
    this.rrule_array = []
    this.recurring_input_state = ''
    this.single_input_boolean = ''
  }

  formatStartDate (date) {
    return moment(date).format('YYYY-MM-DD HH:mm')
  }

  formatEndDate (date) {
    return moment(date).format('HH:mm')
  }
  formatDate (value) {
    return moment(value).format('DD MMM, YYYY')
  }

  generateRule () {
    let validate_flag = false
    const recurring_start_time = (this.recurring_start_time && this.recurring_start_time.hh) ? this.convertTimePickerValue(this.recurring_start_time) : this.recurring_start_time
    const recurring_end_time = (this.recurring_end_time && this.recurring_end_time.hh) ? this.convertTimePickerValue(this.recurring_end_time) : this.recurring_end_time

    if (recurring_start_time) {
      if ((new Date(recurring_start_time).getHours() <= 8) || (new Date(recurring_start_time).getHours() >= 17)){
        if ((new Date(recurring_start_time).getHours() === 8)) {
          if ((new Date(recurring_start_time).getMinutes() < 30)) {
              this.reccuring_start_time_msg = "Time not allowed"
              this.recurring_start_time = null
              validate_flag = true
          } else {
            this.reccuring_start_time_msg = ''
          }
        } else if (new Date(recurring_start_time).getHours() === 17) {
          if ((new Date(recurring_start_time).getMinutes() > 0)) {
              this.reccuring_start_time_msg = "Time not allowed"
              this.recurring_start_time = null
              validate_flag = true
          } else {
            this.reccuring_start_time_msg = ''
          }
        } else {
          this.reccuring_start_time_msg = "Time not allowed"
          this.recurring_start_time = null
          validate_flag = true
        }
      }
    }
    if (recurring_end_time) {
      if ((new Date(recurring_end_time).getHours() <= 8) || (new Date(recurring_end_time).getHours() >= 17)){
        if ((new Date(recurring_end_time).getHours() === 8)) {
          if ((new Date(recurring_end_time).getMinutes() < 30)) {
              this.reccuring_end_time_msg = "Time not allowed"
              this.recurring_end_time = null
              validate_flag = true
          } else {
            this.reccuring_end_time_msg = ''
          }
        } else if (new Date(recurring_end_time).getHours() === 17) {
          if ((new Date(recurring_end_time).getMinutes() > 0)) {
              this.reccuring_end_time_msg = "Time not allowed"
              this.recurring_end_time = null
              validate_flag = true
          } else {
            this.reccuring_end_time_msg = ''
          }
        } else {
          this.reccuring_end_time_msg = "Time not allowed"
          this.recurring_end_time = null
          validate_flag = true
        }
      }
    }
    if (validate_flag) {
      this.recurring_input_state = ''
      return false
    }
    this.hideCollapse('collapse-event-selection')
    this.hideCollapse('collapse-recurring-events')

    this.recurring_blackout_boolean = true
    this.single_blackout_boolean = true
    this.next_boolean = false
    //365 DAYS VALIDATION
    const a = moment(this.recurring_start_date)
    const b = moment(this.recurring_end_date)
    const diffDays = b.diff(a, 'days')
    if (diffDays > 365) {
      this.recurring_start_date = null
      this.recurring_end_date = null
      this.showCollapse('date-limit')
      this.show_next = false
      return false
    }
    const start_year = parseInt(moment(this.recurring_start_date).utc().clone().format('YYYY'))
    const start_month = parseInt(moment(this.recurring_start_date).utc().clone().format('MM'))
    const start_day = parseInt(moment(this.recurring_start_date).utc().clone().format('DD'))
    const start_hour = parseInt(moment(recurring_start_time).utc().clone().format('HH'))
    const local_start_hour = parseInt(moment(recurring_start_time).clone().format('HH'))
    const start_minute = parseInt(moment(recurring_start_time).utc().clone().format('mm'))
    const end_year = parseInt(moment(this.recurring_end_date).utc().clone().format('YYYY'))
    const end_month = parseInt(moment(this.recurring_end_date).utc().clone().format('MM'))
    const end_day = parseInt(moment(this.recurring_end_date).utc().clone().format('DD'))
    const end_hour = parseInt(moment(recurring_end_time).utc().clone().format('HH'))
    const end_minute = parseInt(moment(recurring_end_time).utc().clone().format('mm'))
    const duration = moment.duration(moment(recurring_end_time).diff(moment(recurring_start_time)))
    const duration_minutes = duration.asMinutes()
    let input_frequency: any = null
    let end_adj_day: any = null
    const local_dates_array: any = []

    switch (this.selected_frequency[0]) {
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
      // INC0048019 - fix UTC error by creating new end day and if end_hour is 4pm PACIFIC (16:00) or later then add 1 day to end of series   ozamani 12/17/2020
      if (start_hour > 15 && end_hour < 8) {
        end_adj_day = end_day + 1
      } else {
        end_adj_day = end_day
      }
      const date_start = new Date(Date.UTC(start_year, start_month - 1, start_day, start_hour, start_minute))
      const until = new Date(Date.UTC(end_year, end_month - 1, end_adj_day, end_hour, end_minute))

      const rule = new RRule({
        freq: input_frequency,
        count: this.selected_count,
        byweekday: this.selected_weekdays,
        dtstart: date_start,
        until: until,
        tzid: Intl.DateTimeFormat().resolvedOptions().timeZone
      })
      const array = rule.all()
      this.rrule_text = rule.toText()
      array.forEach(date => {
         // INC0048019 - fix UTC error by creating new date field and if local time is 4pm PACIFIC (16:00) or later then add 1 day to series   ozamani 12/17/2020
        const adj_date = moment(date)
         if (local_start_hour >= 16 && start_hour == 0) {
          adj_date.add(1, 'day')
        }
        const formatted_start_date = moment(adj_date).clone().set({ hour: local_start_hour }).format('YYYY-MM-DD HH:mm:ssZ')
        const formatted_end_date = moment(adj_date).clone().set({ hour: local_start_hour }).add(duration_minutes, 'minutes').format('YYYY-MM-DD HH:mm:ssZ')
        local_dates_array.push({ start: formatted_start_date, end: formatted_end_date })
      })
    }
    this.rrule_array = local_dates_array
    this.selected_count = ''
    this.selected_weekdays = []
    this.selected_frequency = []
    this.recurring_start_date = ''
    this.recurring_start_time = null
    this.recurring_end_date = ''
    this.recurring_end_time = null
    this.recurring_input_boolean = true
    this.recurring_input_state = 'audit_information'
    this.hideCollapse('collapse-blackout-notes')
    this.hideCollapse('date-limit')
    this.showCollapse('collapse-information-audit')
  }

  setSingle () {
    this.single_blackout_boolean = !this.single_blackout_boolean
    this.single_input_boolean = false
    this.recurring_input_boolean = false
    this.blackout_date = null
    this.start_time = null
    this.end_time = null
    this.recurring_input_state = ''
    this.single_input_state = ''
    
    this.stat_dates = [{note:""}]
    this.stat_submit = false
    this.show_stat_next = false
    this.show_next = true

    this.hideCollapse('collapse-single-event')
    this.hideCollapse('collapse-recurring-stat')
  }

  setRecurring () {
    this.recurring_blackout_boolean = !this.recurring_blackout_boolean
    this.single_input_boolean = false
    this.recurring_input_boolean = false
    this.selected_count = ''
    this.selected_weekdays = []
    this.selected_frequency = []
    this.recurring_start_date = null
    this.recurring_start_time = null
    this.recurring_end_date = null
    this.recurring_end_time = null
    this.recurring_input_state = ''
    this.single_input_state = ''

    this.stat_dates = [{note:""}]
    this.stat_submit = false
    this.show_stat_next = false
    this.show_next = true

    this.hideCollapse('collapse-recurring-events')
    this.hideCollapse('collapse-recurring-stat')
  }

  setSTAT () {
    this.recurring_blackout_boolean = !this.recurring_blackout_boolean
    this.single_input_boolean = false
    this.recurring_input_boolean = false
    this.selected_count = ''
    this.selected_weekdays = []
    this.selected_frequency = []
    this.recurring_start_date = null
    this.recurring_start_time = null
    this.recurring_end_date = null
    this.recurring_end_time = null
    this.recurring_input_state = ''
    this.single_input_state = ''

    this.single_blackout_boolean = !this.single_blackout_boolean
    this.single_input_boolean = false
    this.recurring_input_boolean = false
    this.blackout_date = null
    this.start_time = null
    this.end_time = null
    this.recurring_input_state = ''
    this.single_input_state = ''
    this.show_next = true

    this.hideCollapse('collapse-single-event')
    this.hideCollapse('collapse-recurring-events')
  }

  checkRecurringInput () {
    this.reccuring_start_time_msg = ''
    this.reccuring_end_time_msg = ''

    if (this.selected_frequency.length > 0 &&
      this.recurring_start_date !== null && this.recurring_start_time !== null && this.recurring_end_date !== null &&
      this.recurring_end_time !== null) {
      this.recurring_input_boolean = true
      this.next_boolean = true
      this.recurring_input_state = 'event_information'
    } else {
      this.recurring_input_boolean = false
    }
    if (this.only_this_office.length === 0){
      this. only_appointments = []
    }
  }

  checkSingleInput () {
    if (this.blackout_date !== '' && this.start_time !== '' && this.end_time) {
      if (this.blackout_date && this.start_time && this.end_time) {
         this.single_input_boolean = true
          this.single_input_state = 'event_information'
      } else {
        this.single_input_boolean = false
        this.single_input_state = ''
      }
     
    } else {
      this.single_input_boolean = false
      this.single_input_state = ''
    }
  }
  checkStatInput () {
    if (this.stat_dates[0].value) {
        this.show_stat_next = true
    } else {
        this.show_stat_next = false
    }
  }

  nextSingleNotes () {
    const start_time = (this.start_time && this.start_time.hh) ? this.convertTimePickerValue(this.start_time) : this.start_time
    const end_time = (this.end_time && this.end_time.hh) ? this.convertTimePickerValue(this.end_time) : this.end_time

    this.start_time_msg = ''
    this.end_time_msg = ''
    let validate_flag = false
    if (start_time) {
      if ((new Date(start_time).getHours() <= 8) || (new Date(start_time).getHours() >= 17)){
        if ((new Date(start_time).getHours() === 8)) {
          if ((new Date(start_time).getMinutes() < 30)) {
              this.start_time_msg = "Time not allowed"
              this.start_time = null
              validate_flag = true
          } else {
            this.start_time_msg = ''
          }
        } else if (new Date(start_time).getHours() === 17) {
          if ((new Date(start_time).getMinutes() > 0)) {
              this.start_time = "Time not allowed"
              this.start_time = null
              validate_flag = true
          } else {
            this.start_time_msg = ''
          }
        } else {
          this.start_time_msg = "Time not allowed"
          this.start_time = null
          validate_flag = true
        }
      }
    }
    if (end_time) {
      if ((new Date(end_time).getHours() <= 8) || (new Date(end_time).getHours() >= 17)){
        if ((new Date(end_time).getHours() === 8)) {
          if ((new Date(end_time).getMinutes() < 30)) {
              this.end_time_msg = "Time not allowed"
              this.end_time = null
              validate_flag = true
          } else {
            this.end_time_msg = ''
          }
        } else if (new Date(end_time).getHours() === 17) {
          if ((new Date(end_time).getMinutes() > 0)) {
              this.end_time_msg = "Time not allowed"
              this.end_time = null
              validate_flag = true
          } else {
            this.end_time_msg = ''
          }
        } else {
          this.end_time_msg = "Time not allowed"
          this.end_time = null
          validate_flag = true
        }
      }
    }
    if (validate_flag) {
      this.single_input_state = ''
      return false
    }

    this.hideCollapse('collapse-event-selection')
    this.hideCollapse('collapse-single-event')
    this.showCollapse('collapse-blackout-notes')
    this.hideCollapse('date-limit')
    this.single_input_state = 'notes'
  }

  nextRecurringNotes () {
    this.hideCollapse('collapse-information-audit')
    this.showCollapse('collapse-blackout-notes')
    this.hideCollapse('date-limit')
    this.recurring_input_boolean = true
    this.recurring_input_state = 'notes'
  }

  nextStat () {
    this.hideCollapse('collapse-event-selection')
    this.hideCollapse('collapse-information-audit')
    this.hideCollapse('collapse-blackout-notes')
    this.hideCollapse('date-limit')
    this.hideCollapse('collapse-recurring-stat')
    this.rrule_array = []
    this.stat_dates.forEach(item => {
      if (item.value) { 
        this.rrule_array.push(item)
      }
    })
    this.is_stat = true
    this.showCollapse('collapse-information-audit')
    this.show_stat_next = false
    this.stat_submit = true
  }

  async created () {
    this.user_name = 'BLACKOUT PERIOD'
    this.stat_user_name = 'STAT PERIOD'
    this.user_contact_info = this.$store.state.user.username
  }

  mounted () {
    this.user_name = 'BLACKOUT PERIOD'
    this.stat_user_name = 'STAT PERIOD'
  }

  convertTimePickerValue(model:any){
    const currentDate = new Date()
    const fullformat = moment(model.hh + ':' + model.mm + ' ' + model.A ,'hh:mm A').format('HH:mm:ss')
    const day = currentDate.getDate().toString().length === 1 ? '0' + currentDate.getDate().toString() : currentDate.getDate().toString()
    const month = currentDate.getMonth().toString().length === 1 ? '0' + (currentDate.getMonth() + 1).toString() : (currentDate.getMonth() + 1).toString()
    const year = currentDate.getFullYear()
    return new Date(year + '-' + month + '-' + day + ' ' + fullformat)
  }

  async statSubmit () {
    this.setApiTotalCount(0)
    this.setApiTotalCount(this.rrule_array.length)
    showFlagBus.$emit(ShowFlagBusEvents.ShowFlagEvent, true)
    const uuidv4 = require('uuid').v4
    const recurring_uuid = uuidv4()
    let axiosArray: any = []
    let rrule_ind = 0
    const all_offices = await this.getOffices('force')
    const stat_user_name = this.stat_user_name
    const user_contact_info = this.user_contact_info
    const createStatAxioObject = this.createStatAxioObject
    const rrule_array = this.rrule_array
    const bulkApiCall = this.bulkApiCall
    const getOfficeRooms =  this.getOfficeRooms
    this.rrule_array = this.stat_dates
    const self = this
    if (this.rrule_array.length > 0) {
      const limit = 10
      this.rrule_array.forEach(async function (item) { 
        if (item.value) {
          rrule_ind += 1
          const date = moment(item.value).clone().format('YYYY-MM-DD')
          const start = moment(item.value).clone().format('HH:mm:ss')
          const end =  moment(item.value).add(59, 'minutes').add(23, 'hours').add(59, 'seconds').clone().format('HH:mm:ss')
          //only for this off and appointments or both           
          if (self.only_this_office.length == 1){
            if (self.only_this_office[0]){
              //for this office -appointment
              const e: any = {
                  start_time: moment.tz(date+' '+start, self.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
                  end_time: moment.tz(date+' '+end, self.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
                  citizen_name: stat_user_name+'_'+self.$store.state.user.office.office_name,
                  contact_information: user_contact_info,
                  stat_flag: true,
                  office_id: self.$store.state.user.office.office_id,
                  recurring_uuid: recurring_uuid,
                  comments : item.note
                }
                await axiosArray.push(await createStatAxioObject(e))

              // stat for rooms
              if (self.only_appointments.length === 0) {
                const office_room = await getOfficeRooms({'office_id': self.$store.state.user.office.office_id})
                await office_room.forEach(function (room) {
                  const blackout_booking: any = {}
                  // Removed duplicated code in the following "if" stmt. Dec23/21
                  if (room.id != '_offsite') {
                    blackout_booking.room_id = room.id
                  }
                  blackout_booking.start_time = moment.tz(date+' '+start, self.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
                  blackout_booking.end_time = moment.tz(date+' '+end, self.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
                  blackout_booking.booking_name = stat_user_name+'_'+self.$store.state.user.office.office_name
                  blackout_booking.booking_contact_information = user_contact_info
                  blackout_booking.stat_flag = true
                  blackout_booking.blackout_notes = item.note
                  blackout_booking.office_id = self.$store.state.user.office.office_id
                  blackout_booking.recurring_uuid = recurring_uuid
                  blackout_booking.for_stat = true
                  axiosArray.push(self.postBookingStat(blackout_booking))
                })
              }
            }
          } 
          else if (self.only_this_office.length == 0) {
              // stat for appointments
              await all_offices.forEach(async function(office) {
                  const e: any = {
                      start_time: moment.tz(date+' '+start, office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
                      end_time: moment.tz(date+' '+end, office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
                      citizen_name: stat_user_name+'_'+office.office_name,
                      contact_information: user_contact_info,
                      stat_flag: true,
                      office_id: office.office_id,
                      recurring_uuid: recurring_uuid,
                      comments : item.note
                    }
                    await axiosArray.push(await createStatAxioObject(e))

                  // stat for rooms
                  const office_room = await getOfficeRooms({'office_id': office.office_id})
                  await office_room.forEach(function (room) {
                    const blackout_booking: any = {}
                    if (room.id != '_offsite') {
                      blackout_booking.room_id = room.id
                    }
                    blackout_booking.start_time = moment.tz(date+' '+start, office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
                    blackout_booking.end_time = moment.tz(date+' '+end, office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
                    blackout_booking.booking_name = stat_user_name+'_'+office.office_name
                    blackout_booking.booking_contact_information = user_contact_info
                    blackout_booking.stat_flag = true
                    blackout_booking.blackout_notes = item.note
                    blackout_booking.office_id = office.office_id
                    blackout_booking.recurring_uuid = recurring_uuid
                    blackout_booking.for_stat = true
                    axiosArray.push(self.postBookingStat(blackout_booking))
                  })
                })
            }
            //bulk call
            if ((axiosArray.length == limit)) {
                bulkApiCall(axiosArray)
                axiosArray = []
            } else if (rrule_ind == rrule_array.length) {
              bulkApiCall(axiosArray, true)
              axiosArray = []
            } 

        }
      })

  }
  this.recurring_blackout_boolean = true
  this.single_blackout_boolean = true
  this.getAppointments()
  this.toggleAppointmentBlackoutModal(false)
  this.rrule_text = ''
  this.rrule_array = []
  this.recurring_input_state = ''
  this.single_input_boolean = ''

  this.hideCollapse('collapse-event-selection')
  this.hideCollapse('collapse-information-audit')
  this.hideCollapse('collapse-blackout-notes')
  this.hideCollapse('date-limit')
  this.hideCollapse('collapse-recurring-stat')
  this.is_stat = false
  this.hideCollapse('collapse-information-audit')
  this.show_stat_next = false
  this.stat_submit = false
  
  this.stat_dates = [{note:""}]
  this.show_next = true
  this.only_this_office = []
  this.only_appointments = []


}
}
</script>

<style scoped>
.list-group {
  max-height: 75px;
  min-height: 50px;
  overflow-y: scroll;
}
#appointment_stat_date > input.mx-input { 
  height: 38px !important;
}
.danger {
  color: red !important;
}
</style>