<template>
  <b-modal
    v-model="modal"
    hide-header
    size="md"
    modal-class="q-modal"
    body-class="q-modal"
    no-close-on-backdrop
    @shown="show"
  >
    <template slot="modal-footer">
      <div class="d-flex flex-row-reverse">
        <b-button
          v-if="
            this.recurring_form_state === 'notes' ||
            this.single_form_state === 'notes'
          "
          variant="primary"
          class="ml-2"
          size="md"
          id="recurring-submit"
          @click="submit"
        >
          Submit
        </b-button>
        <b-button
          v-else-if="this.stat_submit"
          variant="primary"
          class="ml-2"
          size="md"
          @click="statSubmit"
        >
          Submit</b-button
        >
        <b-button v-else class="ml-2" size="md" id="disabled-submit" disabled>
          Submit
        </b-button>
        <b-button
          v-if="this.single_form_state === 'event_information'"
          variant="primary"
          class="ml-2"
          size="md"
          id="single-event-information-next"
          @click="nextRoomSingleSelection"
        >
          Next
        </b-button>
        <b-button
          v-if="
            this.single_form_state === 'room_selection' &&
            this.room_id_list.length > 0
          "
          variant="primary"
          class="ml-2"
          size="md"
          id="single-room-select-next"
          @click="nextSingleNotes"
        >
          Next
        </b-button>
        <b-button
          v-if="(this.recurring_form_state === 'rule_generated') && (this.show_next)"
          variant="primary"
          class="ml-2"
          size="md"
          id="generate-next"
          @click="generateRule"
        >
          Next
        </b-button>
        <b-button
          v-else-if="this.recurring_form_state === 'audit'"
          variant="primary"
          class="ml-2"
          size="md"
          id="audit-next"
          @click="nextRoomSelection"
        >
          Next
        </b-button>
        <b-button
          v-else-if="
            this.recurring_form_state === 'room_selection' &&
            this.room_id_list.length > 0
          "
          variant="primary"
          class="ml-2"
          size="md"
          id="room-select-enabled"
          @click="nextNotes"
        >
          Next
        </b-button>
        <b-button
          v-else-if="
            (this.recurring_form_state === 'room_selection' &&
              this.room_id_list.length === 0) ||
            (this.single_form_state === 'room_selection' &&
              this.room_id_list.length === 0) ||
            this.recurring_form_state === 'notes'
          "
          disabled
          class="ml-2"
          size="md"
          id="room-select-disabled"
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
        <b-button @click="cancel"> Cancel </b-button>
      </div>
    </template>
    <span style="font-size: 1.75rem">Schedule Booking Blackout</span><br />
    <b-form class="blackout_form">
      <b-collapse id="collapse-booking-event-selection">
        <b-card>
          <b-form-row class="mb-2">
            <label>Step 1: Select Event Type</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col class="w-50">
              <b-button
                variant="primary"
                class="w-100"
                v-b-toggle.collapse-single-booking
                @click="setRecurring"
                size="lg"
              >
                Create Single Blackout
              </b-button>
            </b-col>
            <b-col v-if="is_recurring_enabled" class="w-50">
              <b-button
                variant="primary"
                class="w-100"
                @click="setSingle"
                v-b-toggle.collapse-recurring-booking
                size="lg"
              >
                Create Recurring Blackout
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col v-if="is_Support" class="w-50">
              <b-button
                variant="primary"
                class="w-100"
                @click="setSTAT"
                v-b-toggle.collapse-recurring-stat
                size="lg"
              >
                Create STAT
              </b-button>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-single-booking" class="mt-2 mb-2">
        <v-card>
          <v-container>
          <b-form-row style="justify-content: center">
            <h4>Single Event</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label style="font-weight: bold">Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>Booking Name</label><br />
              <b-form-input v-model="this.blackout_name" disabled />
            </b-col>
            <b-col cols="6">
              <label>Contact Information (optional)</label>
              <b-form-input v-model="this.user_contact_info" />
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Date</label>
                <font-awesome-icon
                  v-if="this.blackout_date !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <DatePicker
                  v-model="blackout_date"
                  id="appointment_blackout_date"
                  type="date"
                  lang="en"
                  class="w-100"
                  clearable
                  @input="checkSingleInput"
                  @change="checkSingleInput"
                  @clear="checkSingleInput"
                >
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Start Time</label>
                <font-awesome-icon
                  v-if="this.start_time !== null"
                  v-model="this.start_time"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <vue-timepicker
                      v-model="start_time"
                      id="appointment_blackout_start_time"
                      icon="clock"
                      editable
                      format="hh:mm A"
                      locale="en-US"
                      placeholder="Select Start Time"
                      @input="checkSingleInput"
                      @clear="checkSingleInput"
                      @change="checkSingleInput"
                      manual-input>
                  </vue-timepicker>
                  <br/>
                  <span class="danger" v-if="start_time_msg">{{start_time_msg}}</span>

              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout End Time</label>
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
                      placeholder="Select End Time"
                      @input="checkSingleInput"
                      @clear="checkSingleInput"
                      @change="checkSingleInput"
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
      <b-collapse id="collapse-recurring-stat">
        <v-card class="mt-2">
          <v-container>
          <b-form-row style="justify-content: center">
            <h4>Recurring STAT</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label style="font-weight: bold">Step 2: STAT Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>Booking Name</label><br />
              <b-form-input v-model="this.stat_user_name" disabled />
            </b-col>
            <b-col cols="6">
              <label>Contact Information (optional)</label>
              <b-form-input v-model="this.user_contact_info" />
            </b-col>
          </b-form-row>
          <b-form-row>
              <b-form-group>
                <label>STAT Date/s:</label>
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
                        v-model="only_bookings"
                        @input="checkRecurringInput"
                      >
                        <b-form-checkbox :value="true">Only bookings</b-form-checkbox>
                    </b-form-checkbox-group>
                  </b-col>
                </b-form-row>
              </div>
              </b-form-group>
          </b-form-row>
          </v-container>
        </v-card>
      </b-collapse>
      <b-collapse id="collapse-recurring-booking" class="mt-2">
        <b-card class="mb-2">
          <b-form-group>
            <b-form-row style="justify-content: center">
              <h4>Recurring Event</h4>
            </b-form-row>
            <b-form-row class="mb-2">
              <label>Step 2: Event Information</label>
            </b-form-row>
            <b-form-row class="mb-2">
              <b-col cols="6">
                <label>Booking Name</label><br />
                <b-form-input v-model="this.blackout_name" disabled />
              </b-col>
              <b-col cols="6">
                <label>Contact Information (optional)</label>
                <b-form-input v-model="this.user_contact_info" />
              </b-col>
            </b-form-row>
            <b-form-row class="mb-2">
              <b-col cols="6">
                <label>Blackout Start Time</label>
                <font-awesome-icon
                  v-if="this.recurring_booking_start_time !== null"
                  v-model="this.recurring_booking_start_time"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <vue-timepicker
                      v-model="recurring_booking_start_time"
                      id="recurring_blackout_start_time"
                      class="w-100"
                      icon="clock"
                      editable
                      format="hh:mm A"
                      locale="en-US"
                      placeholder="Select Start Time"
                      @input="checkRecurringInput"
                      @clear="checkRecurringInput"
                      @change="checkRecurringInput"
                      manual-input>
                  </vue-timepicker>
                  <br/>
                  <span class="danger" v-if="reccuring_start_time_msg">{{reccuring_start_time_msg}}</span>
              </b-col>
              <b-col cols="6">
                <label>Blackout End Time</label>
                <font-awesome-icon
                  v-if="this.recurring_booking_end_time !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <vue-timepicker
                      v-model="recurring_booking_end_time"
                      id="recurring_blackout_end_time"
                      class="w-100"
                      icon="clock"
                      editable
                      format="hh:mm A"
                      locale="en-US"
                      placeholder="Select End Time"
                      @input="checkRecurringInput"
                      @clear="checkRecurringInput"
                      @change="checkRecurringInput"
                      manual-input>
                  </vue-timepicker>
                  <br/>
                  <span class="danger" v-if="reccuring_end_time_msg">{{reccuring_end_time_msg}}</span>
              </b-col>
            </b-form-row>
            <b-form-row class="mb-2">
              <b-col cols="6">
                <label>Blackout Start Date</label>
                <font-awesome-icon
                  v-if="this.recurring_booking_start_date !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <DatePicker
                  id="recurring_booking_start_date"
                  class="w-100"
                  lang="en"
                  v-model="recurring_booking_start_date"
                  placeholder="Select Start Date"
                  clearable
                  @input="checkRecurringInput"
                  @clear="checkRecurringInput"
                >
                </DatePicker>
              </b-col>
              <b-col cols="6">
                <label>Blackout End Date</label>
                <font-awesome-icon
                  v-if="this.recurring_booking_end_date !== null"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <DatePicker
                  v-model="recurring_booking_end_date"
                  id="recurring_booking_end_date"
                  class="w-100"
                  lang="en"
                  clearable
                  @input="checkRecurringInput"
                  @clear="checkRecurringInput"
                >
                </DatePicker>
              </b-col>
            </b-form-row>
            <b-form-row>
              <b-form-group class="mt-0 mb-0">
                <label>Frequency</label>
                <font-awesome-icon
                  v-if="this.selected_booking_frequency.length === 1"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <font-awesome-icon
                  v-if="this.selected_booking_frequency.length > 1"
                  icon="exclamation-triangle"
                  style="font-size: 1rem; color: #ffc32b"
                />
                <label v-if="this.selected_booking_frequency.length > 1"
                  >Select one frequency</label
                >
                <b-form-checkbox-group
                  id="frequency-checkboxes"
                  v-model="selected_booking_frequency"
                  @input="checkRecurringInput"
                >
                  <b-form-checkbox :value="weekly">Weekly</b-form-checkbox>
                  <b-form-checkbox :value="daily">Daily</b-form-checkbox>
                </b-form-checkbox-group>
              </b-form-group>
            </b-form-row>
            <b-form-row>
              <b-form-group class="mt-2">
                <label>Select Weekdays</label>
                <font-awesome-icon
                  v-if="this.selected_booking_weekdays.length >= 1"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <b-form-checkbox-group
                  id="weekday-checkboxes"
                  v-model="selected_booking_weekdays"
                  @input="checkRecurringInput"
                >
                  <b-form-checkbox :value="monday">Mon.</b-form-checkbox>
                  <b-form-checkbox :value="tuesday">Tues.</b-form-checkbox>
                  <b-form-checkbox :value="wednesday">Wed.</b-form-checkbox>
                  <b-form-checkbox :value="thursday">Thurs.</b-form-checkbox>
                  <b-form-checkbox :value="friday">Fri.</b-form-checkbox>
                </b-form-checkbox-group>
              </b-form-group>
            </b-form-row>
            <b-form-row>
              <label stlye="font-weight: bold" class="mt-0"
                >Number of Occurences (optional):</label
              >
              <span v-if="this.selected_booking_count !== ''"
                >&nbsp; Limited to
                {{ this.selected_booking_count }} occurences.</span
              >
              <font-awesome-icon
                v-if="this.selected_booking_count !== ''"
                icon="check"
                style="font-size: 1rem; color: green"
                class="ml-1"
              />
            </b-form-row>
            <b-form-row>
              <b-form-input
                type="number"
                class="mb-1 w-25"
                v-model="selected_booking_count"
              >
              </b-form-input>
            </b-form-row>
          </b-form-group>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-information-audit">
        <b-card class="mb-2">
          <b-form-row style="justify-content: center">
            <h4 v-if="!is_stat">Recurring Event</h4>
            <h4 v-else>Recurring STAT</h4>
          </b-form-row>
          <b-form-row class="mb-2">
              <label stlye="font-weight: bold;"
                v-if="!is_stat">Step 2 (continued): Confirm Recurring Event Information</label
              >
              <label stlye="font-weight: bold;"
                v-else>Step 2 (continued): Confirm Recurring STAT Dates</label
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
            <b-collapse id="recurring-rule-collapse" class="mb-2 ml-2" visible>
              <span v-if="!is_stat">{{ this.booking_rrule_text }}</span>
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
                View Recurring Dates ({{ this.booking_rrule_array.length }})
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-collapse id="recurring-dates-collapse" class="mb-2">
              <div style="height: 75px; overflow-y: scroll; margin: 0px" v-if="!is_stat">
                <ul
                  class="list-group mb-0"
                  v-for="date in this.booking_rrule_array"
                  style="justify-content: center"
                  :key="date.start"
                >
                  <li class="list-group-item">
                    <strong>Event:</strong> {{ formatStartDate(date.start) }} until
                    {{ formatEndDate(date.end) }}
                  </li>
                </ul>
              </div>
              <div style="height: 75px; overflow-y: scroll; margin: 0px" v-else>
                  <ul
                    class="list-group mb-0"
                    v-for="(value, index) in this.booking_rrule_array"
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
      <b-collapse id="collapse-room-selection">
        <b-card>
          <b-form-row style="justify-content: center">
            <h4 v-if="this.recurring_form_state === 'room_selection'">
              Recurring Event
            </h4>
            <h4 v-if="this.single_form_state === 'room_selection'">
              Single Event
            </h4>
          </b-form-row>
          <b-form-row>
            <label
              v-if="this.recurring_form_state === 'room_selection'"
              style="font-weight: bold"
            >
              Step 3: Room Selection
            </label>
            <label
              v-if="this.single_form_state === 'room_selection'"
              style="font-weight: bold"
            >
              Step 2: Room Selection
            </label>
          </b-form-row>
          <b-form-row class="mb-1">
            <b-col class="mr-2">
              <label>Select Room(s)</label>
              <b-table
                selectable
                select-mode="multi"
                selected-variant="success"
                responsive
                :fields="room_fields"
                :items="this.roomResources"
                style="height: 100px"
                bordered
                striped
                @row-selected="onRowSelected"
              >
                <template #cell(selected)="{ rowSelected }">
                  <template v-if="rowSelected">
                    <span aria-hidden="true">&check;</span>
                    <span class="sr-only" Selected></span>
                  </template>
                  <template v-else>
                    <span aria-hidden="true">&nbsp;</span>
                    <span class="sr-only">Not selected</span>
                  </template>
                </template>
              </b-table>
            </b-col>
            <b-col>
              <b-row>
                <label>Selected Room(s)</label>
              </b-row>
              <b-row
                v-for="room in selected"
                style="justify-content: center"
                :key="room.name"
              >
                {{ room.name }}
              </b-row>
              <b-row
                v-if="this.room_id_list.length === 0"
                style="justify-content: center"
              >
                <font-awesome-icon
                  icon="exclamation-triangle"
                  style="font-size: 3rem; color: #ffc32b"
                  class="p-1"
                />
              </b-row>
              <b-row
                v-if="this.room_id_list.length > 0"
                style="justify-content: center"
              >
                <font-awesome-icon
                  icon="check"
                  style="font-size: 3rem; color: green"
                  class="p-1"
                />
              </b-row>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-booking-notes">
        <b-card>
          <b-form-row style="justify-content: center">
            <h4 v-if="this.recurring_form_state === 'notes'">
              Recurring Event
            </h4>
            <h4 v-if="this.single_form_state === 'notes'">Single Event</h4>
          </b-form-row>
          <b-form-row>
            <b-form-group class="ml-1" style="width: 465px">
              <label v-if="this.single_form_state === 'notes'"
                >Step 3: Blackout Notes (optional)</label
              >
              <label v-if="this.recurring_form_state === 'notes'"
                >Step 4: Blackout Notes (optional)</label
              >
              <font-awesome-icon
                v-if="this.notes !== ''"
                icon="check"
                style="font-size: 1rem; color: green"
              />
              <b-textarea
                v-model="notes"
                id="appointment_blackout_notes"
                placeholder="Enter notes about blackout period"
                rows="3"
                maxlength="255"
                max-rows="6"
                size="md"
              >
              </b-textarea>
            </b-form-group>
          </b-form-row>
        </b-card>
      </b-collapse>
    </b-form>
  </b-modal>
</template>

<script lang="ts">
/* eslint-disable */
import { Action, Getter, Mutation, State, namespace } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

import { apiProgressBus, APIProgressBusEvents } from '../../events/progressBus'
import { showBookingFlagBus, ShowBookingFlagBusEvents } from '../../events/showBookingFlagBus'

import DatePicker from 'vue2-datepicker'
import VueTimepicker from 'vue2-timepicker'
import 'vue2-datepicker/index.css'
import 'vue2-timepicker/dist/VueTimepicker.css'
import moment from 'moment'
import { RRule } from 'rrule'


const appointmentsModule = namespace('appointmentsModule')

@Component({
  components: {
    DatePicker,
    VueTimepicker
  }
})
export default class BookingBlackoutModal extends Vue {
  @State('showBookingBlackoutModal') private showBookingBlackoutModal!: any
  @State('rooms') private rooms!: any
  @State('roomResources') private roomResources!: any

  @Getter('is_recurring_enabled') private is_recurring_enabled!: any;
  @appointmentsModule.Getter('is_Support') private is_Support!: any;
  

  @Action('getBookings') public getBookings: any
  @Action('postBooking') public postBooking: any
  @Action('postBookingStat') public postBookingStat: any
  @Action('finishBooking') public finishBooking: any
  @Action('getOffices') public getOffices: any
  @Action('getOfficeRooms') public getOfficeRooms: any

  @Mutation('toggleBookingBlackoutModal') public toggleBookingBlackoutModal: any
  
  @appointmentsModule.Mutation('setApiTotalCount') public setApiTotalCount: any
  
  @appointmentsModule.Action('createStatAxioObject') public createStatAxioObject: any
  @appointmentsModule.Action('callBulkAxios') public callBulkAxios: any
  @appointmentsModule.Action('getAppointments') public getAppointments: any

  public blackout_date: any = null
  public start_time: any = null
  public end_time: any = null
  public notes: string = ''
  public blackout_name: string = ''
  public user_contact_info: string = ''
  public selected: any = []
  public selectedLength: any = 0
  public room_id_list: any = []
  public room_fields: any = ['selected', 'title']
  public single_booking_blackout_boolean: any = true
  public recurring_booking_blackout_boolean: any = true
  public selected_booking_frequency: any = []
  public selected_booking_weekdays: any = []
  public selected_booking_count: any = ''
  public recurring_booking_start_time: any = null
  public recurring_booking_end_time: any = null
  public recurring_booking_start_date: any = null
  public recurring_booking_end_date: any = null
  public yearly: any = RRule.YEARLY
  public monthly: any = RRule.MONTHLY
  public weekly: any = RRule.WEEKLY
  public daily: any = RRule.DAILY
  public monday: any = RRule.MO
  public tuesday: any = RRule.TU
  public wednesday: any = RRule.WE
  public thursday: any = RRule.TH
  public friday: any = RRule.FR
  public booking_rrule_array: any = []
  public booking_rrule_text: string = ''
  public single_input_boolean: any = false
  public recurring_input_boolean: any = false
  public recurring_form_state: string = ''
  public single_form_state: string = ''
  public stat_dates: any = [{note:""}]
  public stat_user_name: string = ''
  public stat_submit: boolean = false
  public show_stat_next: boolean = false
  public is_stat: boolean = false
  public show_next: boolean = true
  public only_this_office: any = []
  public only_bookings: any =[]
  public reccuring_start_time_msg: any = ''
  public reccuring_end_time_msg: any = ''
  public start_time_msg: any = ''
  public end_time_msg: any = ''

  get modal () {
    return this.showBookingBlackoutModal
  }

  set modal (e) {
    this.toggleBookingBlackoutModal(e)
  }

  hideCollapse (div_id) {
    const divSelection = document.getElementById(div_id)
    if (divSelection) {
      if (divSelection.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', div_id)
      }
    }
  }

  showCollapse (div_id) {
    const divSelection = document.getElementById(div_id)
    if (divSelection) {
      if (divSelection.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse', div_id)
      }
    }
  }
  show () {
    this.showCollapse('collapse-booking-event-selection')
    this.hideCollapse('collapse-single-booking')
    // clear single event information
    this.start_time = null
    this.end_time = null
    this.blackout_date = null
    this.notes = ''

    // clear recurring event information
    this.recurring_booking_start_date = null
    this.recurring_booking_start_time = null
    this.recurring_booking_end_date = null
    this.recurring_booking_end_time = null
    this.selected_booking_frequency = []
    this.selected_booking_weekdays = []
    this.selected_booking_count = ''

    // clear local states
    this.single_form_state = ''
    this.recurring_form_state = ''
  }

  cancel () {
    this.toggleBookingBlackoutModal(false)
    this.stat_dates = [{note:""}]
    this.show_stat_next = false
    this.is_stat = false
    this.stat_submit = false
  }

  onRowSelected (roomResources) {
    const roomResourceLength = roomResources.length
    let roomResourceIndex = roomResources.length - 1

    if (roomResourceIndex == -1) {
      roomResourceIndex = 0
    }

    if (this.selectedLength <= roomResourceLength) {
      if (roomResourceLength == 1) {
        this.selected.push({ id: roomResources[0].id, name: roomResources[0].title })
        this.selectedLength = this.selected.length
        this.room_id_list.push(roomResources[0].id)
      } else if (roomResourceLength > 1) {
        this.selected.push({ id: roomResources[roomResourceIndex].id, name: roomResources[roomResourceIndex].title })
        this.selectedLength = this.selected.length
        this.room_id_list.push(roomResources[roomResourceIndex].id)
      }
    } else if (this.selectedLength > roomResourceLength) {
      const remainingIDs: any = []
      roomResources.forEach(function (room) {
        remainingIDs.push(room.id)
      })
      const selectedIDs: any = []
      this.selected.forEach(function (room) {
        selectedIDs.push(room.id)
      })
      const difference = selectedIDs.filter(x => !remainingIDs.includes(x))
      const indexOfDifference = this.selected.findIndex(x => x.id == difference)
      if (indexOfDifference !== undefined) {
        this.selected.splice(indexOfDifference, 1)
      }
      const indexOfDifferenceRoomList = this.room_id_list.findIndex(x => x.id == difference)
      if (indexOfDifferenceRoomList !== undefined) {
        this.room_id_list.splice(indexOfDifferenceRoomList, 1)
      }
    }
  }

  formatStartDate (date) {
    return moment(date).format('YYYY-MM-DD HH:mm')
  }

  formatEndDate (date) {
    return moment(date).format('HH:mm')
  }

  submit (e) {
    e.preventDefault()
    this.setApiTotalCount(0)
    this.setApiTotalCount(this.booking_rrule_array.length)
    showBookingFlagBus.$emit(ShowBookingFlagBusEvents.ShowBookingFlagEvent, true)
    // this is the number of api in a group- for bulk api call
    const limit = 50
    let rrule_ind = 0
    const start_time = this.convertTimePickerValue(this.start_time)
    const end_time = this.convertTimePickerValue(this.end_time)
    const date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
    const start = moment(start_time).clone().format('HH:mm:ss')
    const start_date = moment(date + ' ' + start).format()
    const end = moment(end_time).clone().format('HH:mm:ss')
    const end_date = moment(date + ' ' + end).format()
    const start_date_office = moment.tz(date + ' ' + start, this.$store.state.user.office.timezone.timezone_name).format()
    const end_date_office = moment.tz(date + ' ' + end, this.$store.state.user.office.timezone.timezone_name).format()
    const uuidv4 = require('uuid').v4
    let axiosArray: any = []
    const recurring_uuid = uuidv4()
    if (this.booking_rrule_array.length === 0) {
      if (this.room_id_list.length === 1) {
        const blackout_booking: any = {}
        if (this.selected[0].id === '_offsite') {
          blackout_booking.start_time = start_date_office
          blackout_booking.end_time = end_date_office
          blackout_booking.booking_name = this.blackout_name
          blackout_booking.booking_contact_information = this.user_contact_info
          blackout_booking.blackout_flag = 'Y'
          blackout_booking.blackout_notes = this.notes
        } else {
          blackout_booking.start_time = start_date_office
          blackout_booking.end_time = end_date_office
          blackout_booking.booking_name = this.blackout_name
          blackout_booking.booking_contact_information = this.user_contact_info
          blackout_booking.room_id = this.selected[0].id
          blackout_booking.blackout_flag = 'Y'
          blackout_booking.blackout_notes = this.notes
        }
        this.postBooking(blackout_booking).then(() => {
          this.finishBooking()
          this.toggleBookingBlackoutModal(false)
          showBookingFlagBus.$emit(ShowBookingFlagBusEvents.ShowBookingFlagEvent, false)
        })
      } else if (this.room_id_list.length > 1) {
        const self = this
        this.room_id_list.forEach(function (room) {
          const blackout_booking: any = {}
          if (room == '_offsite') {
            blackout_booking.start_time = start_date_office
            blackout_booking.end_time = end_date_office
            blackout_booking.booking_name = self.blackout_name
            blackout_booking.booking_contact_information = self.user_contact_info
            blackout_booking.blackout_flag = 'Y'
            blackout_booking.blackout_notes = self.notes
          } else {
            blackout_booking.start_time = start_date_office
            blackout_booking.end_time = end_date_office
            blackout_booking.booking_name = self.blackout_name
            blackout_booking.booking_contact_information = self.user_contact_info
            blackout_booking.room_id = room
            blackout_booking.blackout_flag = 'Y'
            blackout_booking.blackout_notes = self.notes
          }
          self.postBooking(blackout_booking).then(() => {
            self.getBookings()
            showBookingFlagBus.$emit(ShowBookingFlagBusEvents.ShowBookingFlagEvent, false)
          })
        })
      }
    } else if (this.booking_rrule_array.length > 0) {
      const booking_array: any = []
      const self = this
      if (this.room_id_list.length === 1) {
        if (this.selected[0].id === '_offsite') {
          this.booking_rrule_array.forEach(date => {
            rrule_ind += 1
            let st = moment(date.start).clone()
            let ed = moment(date.end).clone()
            const startOffice = moment.tz(st.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
            const endOffice = moment.tz(ed.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
            const booking: any = {}
            booking.start_time = startOffice
            booking.end_time = endOffice
            booking.booking_name = self.blackout_name
            booking.booking_contact_information = self.user_contact_info
            booking.blackout_flag = 'Y'
            booking.blackout_notes = self.notes
            booking.recurring_uuid = recurring_uuid
            booking_array.push(booking)
            axiosArray.push(self.postBooking(booking))
          })
        } else {
          this.booking_rrule_array.forEach(date => {
            rrule_ind += 1
            const booking: any = {}
            let st = moment(date.start).clone()
            let ed = moment(date.end).clone()
            const startOffice = moment.tz(st.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
            const endOffice = moment.tz(ed.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
            booking.start_time = startOffice
            booking.end_time = endOffice
            booking.booking_name = self.blackout_name
            booking.booking_contact_information = self.user_contact_info
            booking.blackout_flag = 'Y'
            booking.blackout_notes = self.notes
            booking.room_id = self.selected[0].id
            booking.recurring_uuid = recurring_uuid
            booking_array.push(booking)
            axiosArray.push(self.postBooking(booking))
          })
        }
      } else if (this.room_id_list.length > 1) {
        this.room_id_list.forEach(room => {
          this.booking_rrule_array.forEach(date => {
            rrule_ind += 1
            const booking: any = {}
            let st = moment(date.start).clone()
            let ed = moment(date.end).clone()
            const startOffice = moment.tz(st.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
            const endOffice = moment.tz(ed.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name)
            booking.room_id = room
            booking.start_time = startOffice
            booking.end_time = endOffice
            booking.booking_name = self.blackout_name
            booking.booking_contact_information = self.user_contact_info
            booking.blackout_flag = 'Y'
            booking.blackout_notes = self.notes
            booking.recurring_uuid = recurring_uuid
            if (booking.room_id === '_offsite') {
              delete booking.room_id
            }
            booking_array.push(booking)
            axiosArray.push(self.postBooking(booking))
          })
        })
      }

      if ((axiosArray.length == limit)) {
              this.bulkApiCall(axiosArray)
              axiosArray = []
          } else if (rrule_ind ==  this.booking_rrule_array.length*this.room_id_list.length) {
            this.bulkApiCall(axiosArray, true)
            axiosArray = []
          } 

      this.toggleBookingBlackoutModal(false)
    }
    this.toggleBookingBlackoutModal(false)
  }

  generateRule () {
    let validate_flag =false
    this.reccuring_start_time_msg = ''
    this.reccuring_end_time_msg = ''
    let recurring_booking_start_time = this.convertTimePickerValue(this.recurring_booking_start_time)
    let recurring_booking_end_time = this.convertTimePickerValue(this.recurring_booking_end_time)

    if (recurring_booking_start_time) {
      if ((new Date(recurring_booking_start_time).getHours() <= 8) || (new Date(recurring_booking_start_time).getHours() >= 17)){
        if ((new Date(recurring_booking_start_time).getHours() === 8)) {
          if ((new Date(recurring_booking_start_time).getMinutes() < 30)) {
              this.reccuring_start_time_msg = "Time not allowed"
              this.recurring_booking_start_time = null
              validate_flag = true
          } else {
            this.reccuring_start_time_msg = ''
            validate_flag = false
          }
        } else if (new Date(recurring_booking_start_time).getHours() === 17) {
          if ((new Date(recurring_booking_start_time).getMinutes() > 0)) {
              this.recurring_booking_start_time = null
              this.reccuring_start_time_msg = "Time not allowed"
              validate_flag = true
          } else {
            this.reccuring_start_time_msg = ''
            validate_flag = false
          }
        } else {
          this.reccuring_start_time_msg = "Time not allowed"
          this.recurring_booking_start_time = null
          validate_flag = true
        }
      }
    }
    if (recurring_booking_end_time) {
      if ((new Date(recurring_booking_end_time).getHours() <= 8) || (new Date(recurring_booking_end_time).getHours() >= 17)){
        if ((new Date(recurring_booking_end_time).getHours() === 8)) {
          if ((new Date(recurring_booking_end_time).getMinutes() < 30)) {
              this.reccuring_end_time_msg = "Time not allowed"
              this.recurring_booking_end_time = null
              validate_flag = true
          } else {
            this.reccuring_end_time_msg = ''
            validate_flag = false
          }
        } else if (new Date(recurring_booking_end_time).getHours() === 17) {
          if ((new Date(recurring_booking_end_time).getMinutes() > 0)) {
              this.reccuring_end_time_msg = "Time not allowed"
              this.recurring_booking_end_time = null
              validate_flag = true
          } else {
            this.reccuring_end_time_msg = ''
            validate_flag = false
          }
        } else {
          this.reccuring_end_time_msg = "Time not allowed"
          this.recurring_booking_end_time = null
          validate_flag = true
        }
      }
    }
    if (validate_flag) {
      this.recurring_form_state = ''
      return false
    }
    this.hideCollapse('collapse-booking-event-selection')
    this.hideCollapse('collapse-recurring-booking')
    this.single_booking_blackout_boolean = true
    this.recurring_booking_blackout_boolean = true
    //365 DAYS VALIDATION
    const a = moment(this.recurring_booking_start_date)
    const b = moment(this.recurring_booking_end_date)
    const diffDays = b.diff(a, 'days')
    if (diffDays > 365) {
      this.recurring_booking_start_date = null
      this.recurring_booking_end_date = null
      this.showCollapse('date-limit')
      this.show_next = false
      return false
    }
    // Commented out start/end variables are for testing 5pm pst -> utc conversion bug
    // Removed these variables from the date_start and until variable declarations
    const start_year = parseInt(moment(this.recurring_booking_start_date).clone().format('YYYY'))
    const start_month = parseInt(moment(this.recurring_booking_start_date).clone().format('MM'))
    const start_day = parseInt(moment(this.recurring_booking_start_date).clone().format('DD'))
    const local_start_hour = parseInt(moment(recurring_booking_start_time).clone().format('HH'))
    const start_minute = parseInt(moment(recurring_booking_start_time).utc().clone().format('mm'))
    const end_year = parseInt(moment(this.recurring_booking_end_date).clone().format('YYYY'))
    const end_month = parseInt(moment(this.recurring_booking_end_date).clone().format('MM'))
    const end_day = parseInt(moment(this.recurring_booking_end_date).clone().format('DD'))
    const duration = moment.duration(moment(recurring_booking_end_time).diff(moment(recurring_booking_start_time)))
    const duration_minutes = duration.asMinutes()
    let booking_input_frequency: any = null
    const local_booking_dates_array: any = []

    switch (this.selected_booking_frequency[0]) {
    case 0:
      booking_input_frequency = RRule.YEARLY
      break
    case 1:
      booking_input_frequency = RRule.MONTHLY
      break
    case 2:
      booking_input_frequency = RRule.WEEKLY
      break
    case 3:
      booking_input_frequency = RRule.DAILY
      break
    }

    if (!isNaN(start_year) || !isNaN(end_year)) {
      // IF RRule Breaks, this is where it will happen
      // Removed hours and minutes from date_start and until
      const date_start = new Date(Date.UTC(start_year, start_month - 1, start_day))
      const until = new Date(Date.UTC(end_year, end_month - 1, end_day))

      const rule: any = new RRule({
        freq: booking_input_frequency,
        count: this.selected_booking_count,
        byweekday: this.selected_booking_weekdays,
        dtstart: date_start,
        until: until
      })

      const array = rule.all()
      this.booking_rrule_text = rule.toText()
      array.forEach(date => {
        // created date_with_offset to fix pst -> utc 5pm bug
        const date_with_offset = moment(date).clone().set({ hour: local_start_hour, minute: start_minute }).add(new Date().getTimezoneOffset(), 'minutes')
        if (local_start_hour >= 8 && local_start_hour < 15) {
          date_with_offset.add(1, 'day')
        }
        const formatted_start_date = moment(date_with_offset).clone().set({ hour: local_start_hour, minute: start_minute }).format('YYYY-MM-DD HH:mm:ssZ')
        const formatted_end_date = moment(date_with_offset).clone().set({ hour: local_start_hour, minute: start_minute }).add(duration_minutes, 'minutes').format('YYYY-MM-DD HH:mm:ssZ')
        local_booking_dates_array.push({ start: formatted_start_date, end: formatted_end_date })
      })
    }
    this.booking_rrule_array = local_booking_dates_array
    this.selected_booking_count = ''
    this.selected_booking_frequency = []
    this.selected_booking_weekdays = []
    this.recurring_booking_start_date = null
    this.recurring_booking_start_time = null
    this.recurring_booking_end_date = null
    this.recurring_booking_end_time = null
    this.recurring_form_state = 'audit'
    this.showCollapse('collapse-information-audit')
    this.show_next = true
  }

  setSingle () {
    this.single_booking_blackout_boolean = !this.single_booking_blackout_boolean
    this.single_input_boolean = false
    this.blackout_date = null
    this.start_time = null
    this.end_time = null
    this.recurring_form_state = ''
    this.single_form_state = ''

    this.stat_dates = [{note:""}]
    this.stat_submit = false
    this.show_stat_next = false

    this.hideCollapse('collapse-single-booking')
    this.hideCollapse('collapse-recurring-stat')
  }

  setRecurring () {
    this.recurring_booking_blackout_boolean = !this.recurring_booking_blackout_boolean
    this.single_input_boolean = false
    this.selected_booking_count = ''
    this.selected_booking_frequency = []
    this.selected_booking_weekdays = []
    this.recurring_booking_start_date = null
    this.recurring_booking_start_time = null
    this.recurring_booking_end_date = null
    this.recurring_booking_end_time = null
    this.recurring_form_state = ''
    this.single_form_state = ''
    
    this.stat_dates = [{note:""}]
    this.stat_submit = false
    this.show_stat_next = false

    this.hideCollapse('collapse-recurring-booking')
    this.hideCollapse('collapse-recurring-stat')
  }

  setSTAT () {
    this.recurring_booking_blackout_boolean = !this.recurring_booking_blackout_boolean
    this.single_input_boolean = false
    this.selected_booking_count = ''
    this.selected_booking_frequency = []
    this.selected_booking_weekdays = []
    this.recurring_booking_start_date = null
    this.recurring_booking_start_time = null
    this.recurring_booking_end_date = null
    this.recurring_booking_end_time = null
    this.recurring_form_state = ''
    this.single_form_state = ''

    this.single_booking_blackout_boolean = !this.single_booking_blackout_boolean
    this.single_input_boolean = false
    this.blackout_date = null
    this.start_time = null
    this.end_time = null
    this.recurring_form_state = ''
    this.single_form_state = ''

    this.hideCollapse('collapse-single-booking')
    this.hideCollapse('collapse-recurring-booking')
  }

  checkSingleInput () {
    if (this.blackout_date !== null && this.start_time !== null && this.end_time !== null) {
      this.single_input_boolean = true
      this.single_form_state = 'event_information'
    } else {
      this.single_input_boolean = false
      this.single_form_state = ''
    }
  }

  checkRecurringInput () {
    this.reccuring_start_time_msg = ''
    this.reccuring_end_time_msg = ''
    if (this.selected_booking_frequency.length > 0 && this.recurring_booking_start_date !== null &&
      this.recurring_booking_start_time !== null && this.recurring_booking_end_date !== null &&
      this.recurring_booking_end_time !== null) {
      this.recurring_input_boolean = true
      this.recurring_form_state = 'rule_generated'
    } else {
      this.recurring_input_boolean = false
    }
    if (this.only_this_office.length === 0){
      this.only_bookings = []
    }
  }

  nextRoomSingleSelection () {
    let validate_flag =false
    this.start_time_msg = ''
    this.end_time_msg = ''
    const start_time = this.convertTimePickerValue(this.start_time)
    const end_time = this.convertTimePickerValue(this.end_time)

    if (start_time) {
      if ((new Date(start_time).getHours() <= 8) || (new Date(start_time).getHours() >= 17)){
        if ((new Date(start_time).getHours() === 8)) {
          if ((new Date(start_time).getMinutes() < 30)) {
              this.start_time_msg = "Time not allowed"
              this.start_time = null
              validate_flag = true
          } else {
            this.start_time_msg = ''
            validate_flag = false
          }
        } else if (new Date(start_time).getHours() === 17) {
          if ((new Date(start_time).getMinutes() > 0)) {
              this.start_time = null
              this.start_time_msg = "Time not allowed"
              validate_flag = true
          } else {
            this.start_time_msg = ''
            validate_flag = false
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
            validate_flag = false
          }
        } else if (new Date(end_time).getHours() === 17) {
          if ((new Date(end_time).getMinutes() > 0)) {
              this.end_time_msg = "Time not allowed"
              this.end_time = null
              validate_flag = true
          } else {
            this.end_time_msg = ''
            validate_flag = false
          }
        } else {
          this.end_time_msg = "Time not allowed"
          this.end_time = null
          validate_flag = true
        }
      }
    }
    if (validate_flag) {
      this.single_form_state = ''
      return false
    }
    this.hideCollapse('collapse-single-booking')
    this.hideCollapse('collapse-booking-event-selection')
    this.showCollapse('collapse-room-selection')
    this.single_form_state = 'room_selection'
  }

  nextRoomSelection () {
    this.hideCollapse('collapse-information-audit')
    this.showCollapse('collapse-room-selection')
    this.hideCollapse('collapse-booking-event-selection')
    this.recurring_form_state = 'room_selection'
  }

  nextSingleNotes () {
    this.hideCollapse('collapse-room-selection')
    this.showCollapse('collapse-booking-notes')
    this.single_form_state = 'notes'
  }

  nextNotes () {
    this.hideCollapse('collapse-room-selection')
    this.showCollapse('collapse-booking-notes')
    this.recurring_form_state = 'notes'
  }

  created () {
    this.blackout_name = 'BLACKOUT PERIOD'
    this.stat_user_name = 'STAT PERIOD'
    this.user_contact_info = this.$store.state.user.username
  }

  addField(value, fieldType) {
    fieldType.push({ value: "" });
  }
  
  removeField(index, fieldType) {
    fieldType.splice(index, 1);
  }
  
  nextStat () {
    this.hideCollapse('collapse-information-audit')
    this.hideCollapse('collapse-recurring-stat')
    this.booking_rrule_array = []
    this.stat_dates.forEach(item => {
      if (item.value) { 
        this.booking_rrule_array.push(item)
      }
    })
    this.is_stat = true
    this.showCollapse('collapse-information-audit')
    this.show_stat_next = false
    this.stat_submit = true
    
    
    this.hideCollapse('collapse-single-booking')
    this.hideCollapse('collapse-booking-event-selection')
  }

  mounted () {
    this.blackout_name = 'BLACKOUT PERIOD'
    this.stat_user_name = 'STAT PERIOD'
  }

  
  private delay(ms: number) {
      return new Promise(resolve => setTimeout(resolve, ms))
  }

  async bulkApiCall(axiosArray, flag=false) {
    const res = await this.callBulkAxios({'axiosArray': axiosArray, 'flag': flag})
    if (res) {
      apiProgressBus.$emit(APIProgressBusEvents.APIProgressEvent, axiosArray.length)
      await this.delay(3000)
      showBookingFlagBus.$emit(ShowBookingFlagBusEvents.ShowBookingFlagEvent, false)
      this.getAppointments()
      this.getBookings()
      this.setApiTotalCount(0)
    } else {
      apiProgressBus.$emit(APIProgressBusEvents.APIProgressEvent, axiosArray.length)
      await this.delay(50000)
    }
  }

  async statSubmit () {
    this.setApiTotalCount(0)
    this.setApiTotalCount(this.booking_rrule_array.length)
    showBookingFlagBus.$emit(ShowBookingFlagBusEvents.ShowBookingFlagEvent, true)
    const uuidv4 = require('uuid').v4
    const recurring_uuid = uuidv4()
    let axiosArray: any = []
    let rrule_ind = 0
    const all_offices = await this.getOffices('force')
    const stat_user_name = this.stat_user_name
    const user_contact_info = this.user_contact_info
    const createStatAxioObject = this.createStatAxioObject
    const booking_rrule_array = this.booking_rrule_array
    const stat_dates = this.stat_dates
    const bulkApiCall = this.bulkApiCall
    const getOfficeRooms =  this.getOfficeRooms
    const postBooking = this.postBooking
    this.booking_rrule_array = this.stat_dates
    const self = this
    if (this.booking_rrule_array.length > 0) {
      const limit = 10
      this.booking_rrule_array.forEach(async function (item) { 
        if (item.value) {
          rrule_ind += 1
          const date = moment(item.value).clone().format('YYYY-MM-DD')
          const start = moment(item.value).clone().format('HH:mm:ss')
          const end =  moment(item.value).add(59, 'minutes').add(23, 'hours').add(59, 'seconds').clone().format('HH:mm:ss')
          
          if (self.only_this_office.length == 1){
            if (self.only_this_office[0]){
              // stat for appointments
               if (self.only_bookings.length === 0) {
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
               }
              // stat for rooms
              const office_room = await getOfficeRooms({'office_id': self.$store.state.user.office.office_id})
              office_room.forEach(function (room) {
                const blackout_booking: any = {}
                if (room.id == '_offsite') {
                  blackout_booking.start_time = moment.tz(date+' '+start, self.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
                  blackout_booking.end_time = moment.tz(date+' '+end, self.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
                  blackout_booking.booking_name = stat_user_name+'_'+self.$store.state.user.office.office_name,
                  blackout_booking.booking_contact_information = user_contact_info,
                  blackout_booking.stat_flag = true,
                  blackout_booking.blackout_notes = item.note,
                  blackout_booking.office_id = self.$store.state.user.office.office_id,
                  blackout_booking.recurring_uuid = recurring_uuid
                  blackout_booking.for_stat = true
                } else {
                  blackout_booking.start_time = moment.tz(date+' '+start, self.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
                  blackout_booking.end_time = moment.tz(date+' '+end, self.$store.state.user.office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
                  blackout_booking.booking_name = stat_user_name+'_'+self.$store.state.user.office.office_name,
                  blackout_booking.booking_contact_information = user_contact_info,
                  blackout_booking.room_id = room.id
                  blackout_booking.stat_flag = true,
                  blackout_booking.blackout_notes = item.note,
                  blackout_booking.office_id = self.$store.state.user.office.office_id,
                  blackout_booking.recurring_uuid = recurring_uuid
                  blackout_booking.for_stat = true
                }
                axiosArray.push(self.postBookingStat(blackout_booking))
              })
            }

          }
          //if ends
          else if (self.only_this_office.length == 0) {
              all_offices.forEach(async function(office) {
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
                  office_room.forEach(function (room) {
                    const blackout_booking: any = {}
                    if (room.id == '_offsite') {
                      blackout_booking.start_time = moment.tz(date+' '+start, office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
                      blackout_booking.end_time = moment.tz(date+' '+end, office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
                      blackout_booking.booking_name = stat_user_name+'_'+office.office_name,
                      blackout_booking.booking_contact_information = user_contact_info,
                      blackout_booking.stat_flag = true,
                      blackout_booking.blackout_notes = item.note,
                      blackout_booking.office_id = office.office_id,
                      blackout_booking.recurring_uuid = recurring_uuid
                      blackout_booking.for_stat = true
                    } else {
                      blackout_booking.start_time = moment.tz(date+' '+start, office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ')
                      blackout_booking.end_time = moment.tz(date+' '+end, office.timezone.timezone_name).format('YYYY-MM-DD HH:mm:ssZ'),
                      blackout_booking.booking_name = stat_user_name+'_'+office.office_name,
                      blackout_booking.booking_contact_information = user_contact_info,
                      blackout_booking.room_id = room.id
                      blackout_booking.stat_flag = true,
                      blackout_booking.blackout_notes = item.note,
                      blackout_booking.office_id = office.office_id,
                      blackout_booking.recurring_uuid = recurring_uuid
                      blackout_booking.for_stat = true
                    }
                    axiosArray.push(self.postBookingStat(blackout_booking))
                  }) 
                }) 
                //end of office list
            }
            //bulk call
            if ((axiosArray.length == limit)) {
                bulkApiCall(axiosArray)
                axiosArray = []
            } else if (rrule_ind == booking_rrule_array.length) {
              bulkApiCall(axiosArray, true)
              axiosArray = []
            }
          }

        })
        //end of items

    }
    this.getAppointments()
    this.booking_rrule_text = ''
    this.booking_rrule_array = []
    this.single_input_boolean = ''

    this.toggleBookingBlackoutModal(false)

    this.hideCollapse('collapse-information-audit')
    this.hideCollapse('collapse-recurring-stat')
    this.is_stat = false
    this.hideCollapse('collapse-information-audit')
    this.show_stat_next = false
    this.stat_submit = false
  }
  
  checkStatInput () {
    if (this.stat_dates[0].value) {
        this.show_stat_next = true
    } else {
        this.show_stat_next = false
    }
  }
  
  formatDate (value) {
    return moment(value).format('DD MMM, YYYY')
  }

  convertTimePickerValue(model:any){
    const hh = model ? model.hh : '00'
    const mm = model ? model.mm : '00'
    const aa = model ? model.A : 'AM'
    const currentDate = new Date()
    const fullformat = moment(hh + ':' + mm + ' ' + aa ,'hh:mm A').format('HH:mm:ss')
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
.vue__time-picker input.display-time{
  width: 213px;
  height: 40px;
}
</style>
