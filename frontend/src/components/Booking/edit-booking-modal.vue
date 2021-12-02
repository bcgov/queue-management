<template>
  <b-modal
    v-model="modalVisible"
    :no-close-on-backdrop="true"
    :no-enforce-focus="true"
    :lazy="true"
    :centered="confirm && !minimized"
    @shown="show"
    @cancel="cancel"
    @ok="submit"
    :hide-footer="confirm"
    hide-header
    :size="confirm && !minimized ? 'sm' : 'md'"
  >
    <div v-if="event && showModal" style="margin: 10px">
      <div
        v-if="minimized || !confirm"
        style="display: flex; justify-content: space-between"
      >
        <div v-if="!stat_flag"><h5>Edit Booking</h5></div>
        <div v-else>
            <h5 v-if="is_Support">Edit STAT</h5>
            <h5 v-else>View STAT</h5>
          </div>
        <div>
          <button class="btn btn-link" @click="minimize">
            {{ minimized ? 'Maximize' : 'Minimize' }}
          </button>
        </div>
      </div>
      <template v-if="!confirm">
        <b-form autocomplete="off" v-if="stat_flag">
          <b-form-row>
            <b-col>
              <b-form-group>
                <label>Contact Information (Email or Phone Number)</label>
                <font-awesome-icon
                  v-if="this.booking_contact_information !== ''"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <b-input
                  autocomplete="off"
                  id="contact_information"
                  type="text"
                  readonly
                  v-model="booking_contact_information"
                />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group>
                <label>STAT Notes</label><br />
                <b-input v-if="is_Support"
                  id="blackout_notes"
                  v-model="blackout_notes"
                  class="mb-2"
                  maxlength="255"
                >
                </b-input>
                <b-input v-else
                  id="blackout_notes"
                  :value="blackout_notes"
                  readonly
                  class="mb-2"
                  maxlength="255"
                >
                </b-input>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Room</label>
                <b-input readonly :value="resource.name" />
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Date</label>
                <b-input readonly :value="displayDates.date" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row v-if="!edit_recurring">
            <b-col class="w-100">
              <b-form-group>
                <label>Start Time</label><br />
                <b-input type="text" readonly :value="displayDates.start" />
              </b-form-group>
            </b-col>
            <b-col class="w-100">
              <b-form-group>
                <label>End Time</label><br />
                <b-input type="text" readonly :value="displayDates.end" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row class="mt-0" v-if="is_Support">
            <b-col>
              <b-form-group>
                <label>Delete STAT?</label><br />
                <b-btn class="w-100 btn-danger" @click="confirm = true"
                  >Delete this STAT</b-btn
                >
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-collapse id="delete_recurring_stat_collapse" visible  v-if="is_Support">
            <b-form-row v-if="this.event.recurring_uuid">
              <b-col class="w-100">
                <b-form-group>
                  <label>Delete All STAT Series?</label>
                  <b-button
                    class="w-100 btn-danger"
                    @click="toggleConfirmStatDeleteRecurringCollapse"
                  >
                    Delete All STAT Series
                  </b-button>
                </b-form-group>
              </b-col>
            </b-form-row>
          </b-collapse>
          <b-collapse id="delete_recurring_stat_curroff_collapse" visible  v-if="is_Support">
            <b-form-row v-if="this.event.recurring_uuid">
              <b-col class="w-100">
                <b-form-group>
                  <label>Delete All STAT Series from this Office?</label>
                  <b-button
                    class="w-100 btn-danger"
                    @click="toggleConfirmStatCurrOffDeleteRecurringCollapse"
                  >
                    Delete All STAT Series from this Office
                  </b-button>
                </b-form-group>
              </b-col>
            </b-form-row>
          </b-collapse>
          <b-collapse id="confirm_delete_recurring_stat_curroff_collapse"  v-if="is_Support">
            <b-form-row>
              <b-form-group>
                <label
                  >Are you sure you want to delete this STAT series from this Office?</label
                ><br />
                <b-row
                  style="
                    display: flex;
                    justify-content: center;
                    margin-left: 150px;
                  "
                >
                  <b-button
                    size="sm"
                    variant="primary"
                    class="ml-1 mr-1"
                    @click="toggleStatCurrOffDeleteRecurringCollapse"
                  >
                    No
                  </b-button>
                  <b-button
                    size="sm"
                    variant="danger"
                    class="ml-1 mr-1"
                    @click="clickYesStatRecurring"
                  >
                    Yes
                  </b-button>
                </b-row>
              </b-form-group>
            </b-form-row>
          </b-collapse>
          <b-collapse id="confirm_delete_recurring_stat_collapse"  v-if="is_Support">
            <b-form-row>
              <b-form-group>
                <label
                  >Are you sure you want to delete this STAT series?</label
                ><br />
                <b-row
                  style="
                    display: flex;
                    justify-content: center;
                    margin-left: 150px;
                  "
                >
                  <b-button
                    size="sm"
                    variant="primary"
                    class="ml-1 mr-1"
                    @click="toggleStatDeleteRecurringCollapse"
                  >
                    No
                  </b-button>
                  <b-button
                    size="sm"
                    variant="danger"
                    class="ml-1 mr-1"
                    @click="clickYesStatAllOfficeRecurring"
                  >
                    Yes
                  </b-button>
                </b-row>
              </b-form-group>
            </b-form-row>
          </b-collapse>
          <b-form-row v-if="message">
            <b-col>
              <div
                style="display: flex; justify-content: flex-end; width: 100%"
              >
                <span style="color: red; font-weight: 600; font-size: 0.9rem">{{
                  message
                }}</span>
              </div>
            </b-col>
          </b-form-row>
        </b-form>
        <b-form autocomplete="off" v-else>
          <b-form-row v-if="examAssociated">
            <b-col class="mb-2">
              <div class="q-info-display-grid-container">
                <div class="q-id-grid-outer">
                  <div class="q-id-grid-head">Exam Details</div>
                  <div class="q-id-grid-col">
                    <div>Writer:</div>
                    <div>{{ this.event.exam.examinee_name }}</div>
                  </div>
                  <div class="q-id-grid-col">
                    <div>Exam:</div>
                    <div>{{ this.event.exam.exam_name }}</div>
                  </div>
                  <div class="q-id-grid-col">
                    <div>Method:</div>
                    <div>{{ this.event.exam.exam_method }}</div>
                  </div>
                  <div class="q-id-grid-col">
                    <div>Event ID:</div>
                    <div>{{ this.event.exam.event_id }}</div>
                  </div>
                  <div class="q-id-grid-col">
                    <div>Duration:</div>
                    <div>
                      {{ this.event.exam.exam_type.number_of_hours }} hrs
                      {{ this.event.exam.exam_type.number_of_minutes }} min
                    </div>
                  </div>
                  <div class="q-id-grid-col">
                    <div>Expiry:</div>
                    <div>{{ expiryDate }}</div>
                  </div>
                </div>
              </div>
            </b-col>
          </b-form-row>
          <b-form-row v-if="!examAssociated">
            <b-col>
              <b-form-group>
                <label :style="{ color: labelColor }">Scheduling Party</label
                ><br />
                <b-input
                  :state="state"
                  id="title"
                  type="text"
                  @input.native="checkValue"
                  v-model="title"
                />
              </b-form-group>
            </b-col>
            <b-col cols="4">
              <b-form-group>
                <label>Collect Fees</label><br />
                <b-select
                  id="fees"
                  v-model="fees"
                  @change.native="checkValue"
                  :options="feesOptions"
                />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group>
                <label>Contact Information (Email or Phone Number)</label>
                <font-awesome-icon
                  v-if="this.booking_contact_information !== ''"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <b-input
                  autocomplete="off"
                  id="contact_information"
                  type="text"
                  @change.native="checkValue"
                  v-model="booking_contact_information"
                />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group v-if="checkBookingBlackout">
                <label>Blackout Notes</label><br />
                <b-form-textarea
                  id="blackout_notes"
                  v-model="blackout_notes"
                  class="mb-2"
                  maxlength="255"
                  @change.native="checkValue"
                >
                </b-form-textarea>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Room</label>
                <b-input readonly :value="resource.name" />
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Date</label>
                <b-input readonly :value="displayDates.date" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row v-if="!edit_recurring">
            <b-col class="w-100">
              <b-form-group>
                <label>Start Time</label><br />
                <b-input type="text" readonly :value="displayDates.start" />
              </b-form-group>
            </b-col>
            <b-col class="w-100">
              <b-form-group>
                <label>End Time</label><br />
                <b-input type="text" readonly :value="displayDates.end" />
              </b-form-group>
            </b-col>
            <b-col cols="5" v-if="examAssociated">
              <b-form-group>
                <label>Invigilator</label><br />
                <b-select
                  v-model="invigilator"
                  :options="invigilator_dropdown"
                  id="invigilator"
                  :value="invigilator"
                  @change="setInvigilator"
                />
              </b-form-group>
            </b-col>
            <b-col cols="5" v-if="!examAssociated">
              <b-form-group>
                <label>Duration</label><br />
                <b-button-group>
                  <b-button @click="decrement">
                    <font-awesome-icon
                      icon="minus"
                      class="m-0 p-0"
                      style="font-size: 0.8rem; color: white"
                    />
                  </b-button>
                  <b-input
                    :value="displayDuration"
                    readonly
                    id="duration"
                    @change.native="checkValue"
                    style="border-radius: 0px"
                  />
                  <b-button @click="increment">
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
          <b-form-row>
            <template v-if="this.currentShadowInvigilator != null">
              <b-row style="display: flex" class="w-100 ml-0 mb-2">
                <b-col class="w-50 ml-1 mr-1 pr-1">
                  <b-button
                    v-if="this.changeState"
                    v-b-toggle.collapse-1
                    variant="primary"
                    @click="setRemove"
                  >
                    Change Shadow Invigilator
                  </b-button>
                  <b-button
                    v-else-if="!this.changeState"
                    disabled
                    variant="primary"
                  >
                    Change Shadow Invigilator
                  </b-button>
                </b-col>
                <b-col class="w-50 ml-1 mr-1 pl-1">
                  <b-button
                    v-if="this.removeState"
                    v-b-toggle.collapse-2
                    variant="danger"
                    @click="setChange"
                  >
                    Remove Shadow Invigilator
                  </b-button>
                  <b-button
                    v-else-if="!this.removeState"
                    disabled
                    variant="danger"
                  >
                    Remove Shadow Invigilator
                  </b-button>
                </b-col>
              </b-row>
            </template>
            <template v-else-if="!this.event.exam.is_pesticide">
              <b-button
                v-if="examAssociated"
                v-b-toggle.collapse-1
                variant="primary"
                class="w-100 m-1"
              >
                Add Shadow Invigilator
              </b-button>
            </template>
            <b-collapse id="collapse-1" class="mt-2 w-100">
              <b-form-group class="q-info-display-grid-container">
                <label>Shadow Invigilators</label>
                <b-form>
                  <b-row>
                    <b-col cols="7">
                      <b-table
                        selectable
                        select-mode="single"
                        :fields="shadowFields"
                        :items="shadow_invigilator_options"
                        @row-selected="rowSelectedShadow"
                        responsive
                        selected-variant="success"
                        style="height: 75px; width: 250px"
                        bordered
                        striped
                      >
                        <template #cell(selected)="{ rowSelected }">
                          <span v-if="rowSelected">✔</span>
                        </template>
                      </b-table>
                    </b-col>
                    <b-col cols="4">
                      <b-row> Shadow Invigilator Limit: 1 </b-row>
                      <b-row
                        v-if="this.currentShadowInvigilator != null"
                        class="mb-1"
                      >
                        Current Invigilator
                      </b-row>
                      <b-row
                        v-if="this.currentShadowInvigilator != null"
                        style="justify-content: center"
                        class="mb-1"
                      >
                        {{ this.currentShadowInvigilatorName }}
                      </b-row>
                      <b-row style="font-weight: bold" class="mb-1">
                        Selected Invigilators
                      </b-row>
                      <b-row
                        v-for="select in selectedShadow"
                        style="justify-content: center"
                        class="mb-1"
                        :key="select.name"
                      >
                        {{ select.name }}
                      </b-row>
                    </b-col>
                  </b-row>
                </b-form>
              </b-form-group>
            </b-collapse>
            <b-collapse id="collapse-2" class="mt-2 w-100">
              <b-form-group class="q-info-display-grid-container">
                <b-row class="ml-1">
                  <span style="font-weight: bold"
                    >Current Shadow Invigilator:
                  </span>
                </b-row>
                <b-row class="mb-2" style="justify-content: center">
                  <span>{{ this.currentShadowInvigilatorName }}</span>
                </b-row>
                <b-row class="ml-1">
                  <span style="font-weight: bold"
                    >Would you like to remove this shadow invigilator?</span
                  >
                </b-row>
                <template>
                  <b-row
                    style="display: flex; justify-content: center"
                    class="w-100 mb-0"
                  >
                    <b-button
                      class="mr-2 mt-1"
                      variant="danger"
                      @click="setSelectedShadowNull"
                    >
                      Yes
                    </b-button>
                    <b-button
                      class="ml-2 mt-1"
                      variant="primary"
                      v-b-toggle.collapse-2
                      @click="setChange"
                    >
                      No
                    </b-button>
                  </b-row>
                </template>
              </b-form-group>
            </b-collapse>
          </b-form-row>
          <b-form-row class="mt-0">
            <b-col>
              <b-form-group>
                <label>Delete Booking?</label><br />
                <b-btn class="w-100 btn-danger" @click="confirm = true"
                  >Delete Booking</b-btn
                >
              </b-form-group>
            </b-col>
            <b-col v-if="!this.edit_recurring">
              <b-form-group>
                <label>Change Date, Time or Room?</label><br />
                <b-btn class="w-100 mb-0" @click="reschedule">
                  Reschedule Booking
                </b-btn>
              </b-form-group>
            </b-col>
            <b-col v-else></b-col>
          </b-form-row>
          <b-collapse id="delete_recurring_collapse" visible>
            <b-form-row v-if="this.event.recurring_uuid">
              <b-col class="w-100">
                <b-form-group>
                  <label>Delete Booking Series?</label>
                  <b-button
                    class="w-100 btn-danger"
                    @click="toggleConfirmDeleteRecurringCollapse"
                  >
                    Delete Booking Series
                  </b-button>
                </b-form-group>
              </b-col>
              <b-col class="w-100">
                <label>Edit Entire Series?</label>
                <b-form-checkbox switch size="lg" @change="toggleEditRecurring">
                  <span v-if="this.edit_recurring" style="font-size: 0.75em"
                    >Editing entire series.</span
                  >
                  <span v-else style="font-size: 0.75em"
                    >Editing single event</span
                  >
                </b-form-checkbox>
              </b-col>
            </b-form-row>
          </b-collapse>
          <b-collapse id="confirm_delete_recurring_collapse">
            <b-form-row>
              <b-form-group>
                <label
                  >Are you sure you want to delete this booking series?</label
                ><br />
                <b-row
                  style="
                    display: flex;
                    justify-content: center;
                    margin-left: 150px;
                  "
                >
                  <b-button
                    size="sm"
                    variant="primary"
                    class="ml-1 mr-1"
                    @click="toggleDeleteRecurringCollapse"
                  >
                    No
                  </b-button>
                  <b-button
                    size="sm"
                    variant="danger"
                    class="ml-1 mr-1"
                    @click="clickYesRecurring"
                  >
                    Yes
                  </b-button>
                </b-row>
              </b-form-group>
            </b-form-row>
          </b-collapse>
          <b-form-row v-if="message">
            <b-col>
              <div
                style="display: flex; justify-content: flex-end; width: 100%"
              >
                <span style="color: red; font-weight: 600; font-size: 0.9rem">{{
                  message
                }}</span>
              </div>
            </b-col>
          </b-form-row>
        </b-form>
      </template>

      <template v-if="confirm">
        <template v-if="!minimized">
          <span>Are you sure you want to delete this booking?<br /></span>
          <div style="display: flex; justify-content: center">
            <b-button class="mr-2 btn-primary" @click="confirm = false">
              No
            </b-button>
            <b-button class="ml-2 btn-danger" @click="clickYes"> Yes </b-button>
          </div>
        </template>
      </template>
    </div>
  </b-modal>
</template>

<script lang="ts">
/* eslint-disable */
import { Action, Getter, Mutation, State, namespace } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'

import moment from 'moment'
const appointmentsModule = namespace('appointmentsModule')


@Component({})
export default class EditBooking extends Vue {
  @Prop({ default: '' })
  private tempEvent!: any

  @State('editedBooking') private event!: any
  @State('editedBookingOriginal') private actualEvent!: any
  @State('clickedDate') private newEvent!: any
  @State('showEditBookingModal') private showModal!: any
  @State('invigilators') private invigilators!: any
  @State('selectedExam') private selectedExam!: any
  @State('shadowInvigilators') private shadowInvigilators!: any
  @State('editDeleteSeries') private editDeleteSeries!: any

  @Getter('invigilator_dropdown') private invigilator_dropdown!: any;
  @Getter('shadow_invigilators') private shadow_invigilators!: any;
  @Getter('shadow_invigilator_options') private shadow_invigilator_options!: any;

  @Action('getBookings') public getBookings: any
  @Action('deleteBooking') public deleteBooking: any
  @Action('deleteRecurringBooking') public deleteRecurringBooking: any
  @Action('deleteRecurringStatBooking') public deleteRecurringStatBooking: any
  @Action('deleteRecurringStatAllOfficeBooking') public deleteRecurringStatAllOfficeBooking: any
  @Action('finishBooking') public finishBooking: any
  @Action('getInvigilators') public getInvigilators: any
  @Action('postBooking') public postBooking: any
  @Action('putBooking') public putBooking: any
  @Action('putRecurringBooking') public putRecurringBooking: any
  @Action('putInvigilatorShadow') public putInvigilatorShadow: any

  @Mutation('setClickedDate') public setClickedDate: any
  @Mutation('setEditedBooking') public setEditedBooking: any
  @Mutation('setSelectedExam') public setSelectedExam: any
  @Mutation('toggleEditBookingModal') public toggleEditBookingModal: any
  @Mutation('toggleScheduling') public toggleScheduling: any
  @Mutation('toggleRescheduling') public toggleRescheduling: any
  @Mutation('toggleEditDeleteSeries') public toggleEditDeleteSeries: any

  
  @appointmentsModule.Action('deleteRecurringAppointments') public deleteRecurringAppointments: any
  @appointmentsModule.Action('deleteRecurringStatAppointments') public deleteRecurringStatAppointments: any
  @appointmentsModule.Getter('is_Support') private is_Support!: any;

  public minimized: any = false
  public confirm: any = false
  public added: any = 0
  public invigilator: any = null
  public shadowInvigilator: any = null
  public currentShadowInvigilator: any = null
  public currentShadowInvigilatorName: any = ''
  public editedFields: any = []
  public fees: any = ''
  public feesOptions: any = [
    { text: 'No', value: 'false' },
    { text: 'Yes', value: 'true' },
    { text: 'HQ to Invoice', value: 'HQFin' }
  ]

  public invoice: any = null
  public invoiceOptions: any = [{ text: 'Custom', value: 'custom' }]
  public labelColor: any = 'black'
  public message: any = ''
  public newEnd: any = null
  public newStart: any = null
  public rate: any = null
  public roomRates: any = [
    { value: 125, text: '$125 for 1/2 Day' },
    { value: 250, text: '$250 for Whole Day' }
  ]

  public state: any = null
  public title: any = ''
  public booking_contact_information: string = ''
  public rescheduling: boolean = false
  public blackout_notes: string = ''
  public selectedShadow: any = []
  public shadowFields: any = ['selected', 'name']
  public changeState: boolean = true
  public removeState: boolean = true
  public removeFlag: boolean = false
  public rescheduleInvigilator: any = null
  public rescheduleShadowInvigilator: any = null
  public cancel_flag: boolean = false
  public delete_recurring: boolean = false
  public edit_recurring: boolean = false
  public stat_flag: boolean = false


  get checkBookingBlackout () {
    if (this.event.blackout_flag === 'Y') {
      return true
    }
    return false
  }

  get displayDates () {
    if (this.event.start && this.event.end) {
      // change to moment time
      this.event.end = !moment.isMoment(this.event.end) ? moment(this.event.end) : this.event.end
      this.event.start = !moment.isMoment(this.event.start) ? moment(this.event.start) : this.event.start

      return {
        end: this.event.end.format('h:mm a'),
        start: this.event.start.format('h:mm a'),
        date: this.event.start.format('ddd MMM D, YYYY')
      }
    }
    return { end: '', start: '', date: '' }
  }

  get displayDuration () {
    if (this.duration) {
      const output = this.duration.toFixed(1)
      return `${output} hrs`
    }
  }

  get duration () {
    if (this.start && this.end) {
      return this.end.diff(this.start, 'hours', true)
    }
    return ''
  }

  get end () {
    if (this.examAssociated && this.newEvent) {
      // TOCHECK removed new keyword in moment. not needed
      // return new moment(this.newEvent.end)
      return moment(this.newEvent.end)
    }
    if (this.examAssociated && !this.newEvent) {
      // TOCHECK removed new keyword in moment. not needed
      // return new moment(this.event.end)
      return moment(this.event.end)
    }
    if (!this.newEnd && this.event && this.event.end) {
      // TOCHECK removed new keyword in moment. not needed
      // return new moment(this.event.end).add(this.added, 'hours')
      return moment(this.event.end).add(this.added, 'hours')
    }
    if (this.newEnd) {
      // TOCHECK removed new keyword in moment. not needed
      // return new moment(this.newEnd).add(this.added, 'hours')
      return moment(this.newEnd).add(this.added, 'hours')
    }
  }

  get examAssociated () {
    if (this.event && this.event.exam) {
      return true
    }
    return false
  }

  get expiryDate () {
    if (this.examAssociated && this.event.exam) {
      // TOCHECK removed new keyword in moment. not needed
      // const d = new moment(this.event.exam.expiry_date)
      const d = moment(this.event.exam.expiry_date)
      if (d.isValid()) {
        return d.format('MMM Do, YYYY')
      }
    }
    return 'not applicable'
  }

  get modalVisible () {
    return this.showModal
  }

  set modalVisible (e) {
    this.toggleEditBookingModal(e)
  }

  get resource () {
    if (this.newEvent) {
      return {
        name: this.newEvent.resource.title,
        id: this.newEvent.resource.id
      }
    }
    if (this.event) {
      if (this.event.room && this.event.room.room_name) {
        return {
          name: this.event.room.room_name,
          id: this.event.room.room_id
        }
      }
    }
    return ''
  }

  get start () {
    if (this.examAssociated && this.newEvent) {
      // TOCHECK removed new keyword in moment. not needed
      return moment(this.newEvent.start)
    }
    if (this.examAssociated && !this.newEvent) {
      // TOCHECK removed new keyword in moment. not needed
      return moment(this.event.start)
    }
    if (!this.newStart && this.event && this.event.start) {
      // TOCHECK removed new keyword in moment. not needed
      return moment(this.event.start)
    }
    if (this.newStart) {
      return this.newStart
    }
  }

  // methods
  cancel () {
    this.cancel_flag = true
    let returnRoute = false
    if (this.selectedExam && this.selectedExam.referrer === 'rescheduling') {
      returnRoute = true
    }
    this.finishBooking()
    this.resetModal()
    this.getBookings()
    if (returnRoute) {
      this.$router.push('/exams')
    }
  }

  checkValue (e) {
    if (this.labelColor === 'red') {
      if (e.target.id === 'title' && e.target.value.length > 0) {
        this.labelColor = 'black'
        this.message = ''
      }
    }
    if (this.event[e.target.id] !== e.target.value) {
      if (!this.editedFields.includes(e.target.id)) {
        this.editedFields.push(e.target.id)
      }
    }
    if (this.event[e.target.id] === e.target.value) {
      if (this.editedFields.includes(e.target.id)) {
        const i = this.editedFields.indexOf(e.target.id)
        this.editedFields.splice(i, 1)
      }
    }
    if (this.message === 'No Changes Made') {
      if (this.editedFields.length > 0) {
        this.message = ''
      }
    }
  }

  clickYes (e) {
    e.preventDefault()
    const id = this.event.id
    this.deleteBooking(id).then(() => {
      this.finishBooking()
      this.resetModal()
    })
  }

  clickYesRecurring (e) {
    const re_id = this.event.recurring_uuid
    this.deleteRecurringBooking(re_id).then(() => {
      this.$root.$emit('removeTempEvent')
      this.$root.$emit('clear-clicked-time')
      this.$root.$emit('clear-clicked-appt')
      this.finishBooking()
      this.resetModal()
    })
    this.toggleEditDeleteSeries(false)
  }

  clickYesStatRecurring (e) {
    const re_id = this.event.recurring_uuid
    this.deleteRecurringStatBooking(re_id).then(() => {
      this.deleteRecurringAppointments(re_id).then(() => {
        this.$root.$emit('removeTempEvent')
        this.$root.$emit('clear-clicked-time')
        this.$root.$emit('clear-clicked-appt')
      })
      this.finishBooking()
      this.resetModal()
    })
    this.toggleEditDeleteSeries(false)
  }

  clickYesStatAllOfficeRecurring (e) {
    const re_id = this.event.recurring_uuid
    this.deleteRecurringStatAllOfficeBooking(re_id).then(() => {
      this.deleteRecurringStatAppointments(re_id).then(() => {
        this.$root.$emit('removeTempEvent')
        this.$root.$emit('clear-clicked-time')
        this.$root.$emit('clear-clicked-appt')
      })
      this.finishBooking()
      this.resetModal()
    })
    this.toggleEditDeleteSeries(false)
  }

  decrement () {
    if (this.duration == 0.5) {
      return
    }
    this.added -= 0.5
    const params: any = {
      end: this.end
    }
    if (this.tempEvent) {
      return
    }
    this.$root.$emit('updateEvent', this.actualEvent, params)
  }

  increment () {
    if ((this.end as any).format('H') == 18) {
      return
    }
    this.added += 0.5
    const params = {
      end: this.end
    }
    if (this.tempEvent) {
      return
    }
    this.$root.$emit('updateEvent', this.actualEvent, params)
  }

  minimize () {
    if (this.minimized) {
      this.minimized = false
      this.confirm = false
    } else {
      this.minimized = true
      this.confirm = true
    }
  }

  reschedule () {
    this.rescheduleInvigilator = this.invigilator
    this.rescheduleShadowInvigilator = this.currentShadowInvigilator
    if (this.selectedExam && this.selectedExam.gotoDate) {
      this.setSelectedExam('clearGoto')
    }
    this.toggleRescheduling(true)
    this.toggleEditBookingModal(false)
    this.rescheduling = true
    this.editedFields.push('invigilator')
    this.editedFields.push('shadow_invigilator')
  }

  resetModal () {
    this.added = null
    this.newStart = null
    this.newEnd = null
    this.editedFields = []
    this.fees = false
    this.labelColor = 'black'
    this.message = null
    this.state = null
    this.title = null
    this.confirm = false
  }

  setInvigilator (e) {
    this.message = ''
    if (this.event.exam && this.event.exam.booking) {
      if (this.event.exam.booking.invigilator_id !== e) {
        if (!this.editedFields.includes('invigilator')) {
          this.editedFields.push('invigilator')
        }
      }
      if (this.event.exam.booking.invigilator_id == e) {
        if (this.editedFields.includes('invigilator')) {
          this.editedFields.splice(this.editedFields.indexOf('invigilator'), 1)
        }
      }
    }
    if (this.invigilator === 'sbc' && !e) {
      if (!this.editedFields.includes('invigilator')) {
        this.editedFields.push('invigilator')
      }
    }
    this.invigilator = e
  }

  show () {
    if (this.event.recurring_uuid) {
      this.toggleEditDeleteSeries(true)
    }
    this.edit_recurring = false
    this.changeState = true
    this.removeState = true
    if (this.newEvent && this.newEvent.start) {
      // TOCHECK removed new keyword in moment. not needed
      this.newStart = moment(this.newEvent.start)
      // TOCHECK removed new keyword in moment. not needed
      this.newEnd = moment(this.newEvent.end)
    }
    if (this.event.exam && this.event.exam.booking) {
      const currentID = this.currentShadowInvigilator = this.event.exam.booking.shadow_invigilator_id || null
      let currentName = ''
      this.shadow_invigilators.forEach(function (invigilator) {
        if (invigilator.id == currentID) {
          currentName = invigilator.name
        }
      })
      this.currentShadowInvigilatorName = currentName
      if (!this.editedFields.includes('invigilator')) {
        if (this.rescheduling) {
          this.invigilator = null
        }
        if (this.event.exam.booking.invigilators.length == 1) {
          this.invigilator = this.event.exam.booking.invigilators[0] || null
        }
      }
      if (this.event.exam.booking.sbc_staff_invigilated) {
        if (!this.editedFields.includes('invigilator')) {
          if (this.rescheduling) {
            this.invigilator = null
          }
          this.invigilator = 'sbc'
        }
      }
    }
    if (!this.editedFields.includes('title')) {
      this.title = this.event.name
    }
    if (!this.editedFields.includes('fees')) {
      this.fees = this.event.fees
    }
    if (!this.editedFields.includes('booking_contact_information')) {
      this.booking_contact_information = this.event.booking_contact_information
    }
    if (!this.editedFields.includes('stat_flag')) {
      this.stat_flag = this.event.stat_flag
    }

    if (!this.editedFields.includes('blackout_notes')) {
      this.blackout_notes = this.event.blackout_notes
    }
    if (this.rescheduling) {
      if (this.cancel_flag) {
        this.invigilator = this.rescheduleInvigilator
        this.currentShadowInvigilator = this.rescheduleShadowInvigilator
        this.rescheduleInvigilator = null
        this.cancel_flag = false
      } else {
        this.invigilator = null
        this.currentShadowInvigilator = null
        this.currentShadowInvigilatorName = null
      }
    }
    this.rescheduling = false
    this.cancel_flag = false
    this.rescheduleInvigilator = null
  }

  rowSelectedShadow (shadows, e) {
    this.message = ''
    this.selectedShadow = shadows
    if (this.event.exam && this.event.exam.booking) {
      if (this.event.exam.booking.shadow_invigilator_id !== e) {
        if (!this.editedFields.includes('shadow_invigilator')) {
          this.editedFields.push('shadow_invigilator')
        }
      } else if (this.event.exam.booking.shadow_invigilator_id == e) {
        if (this.editedFields.includes('shadow_invigilator')) {
          this.editedFields.splice(this.editedFields.indexOf('shadow_invigilator'), 1)
        }
      }
    }
    if (shadows[0] == null) {
      this.shadowInvigilator = null
    } else {
      this.shadowInvigilator = shadows[0].id
    }
  }

  submit () {
      if (this.title) {
        if (this.title.length === 0) {
          this.labelColor = 'red'
          this.state = 'danger'
          this.message = 'A title is required'
          return
        }
      }
      const changes: any = {}
      if (!this.start.isSame(this.event.start)) {
        if (this.examAssociated) {
          //  fix for INC0042620
          const exp_date = moment(this.event.exam.expiry_date).add(1,'days')
          if (this.start.isAfter(exp_date)) {
            this.message = 'Selected date/time is after the exam\'s expiry date.  Press reschedule to pick a new time.'
            return
          }
        }
        if (moment().isAfter(this.start)) {
          this.message = 'Selected date/time is is in the past. Press Reschedule and pick a new time.'
          return
        }
        changes.start_time = this.start.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
      }
      if (!(this.end as any).isSame(this.event.end)) {
        changes.end_time = (this.end as any).utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
      }
      if (this.newEvent && !(this.newEvent.resource.id == this.event.resourceId)) {
        changes.room_id = this.newEvent.resource.id
      }
      if (this.editedFields.includes('title')) {
        changes.booking_name = this.title
      }
      if (this.editedFields.includes('fees')) {
        changes.fees = this.fees
      }
      if (this.editedFields.includes('invigilator')) {
        changes.invigilator_id = this.invigilator
        if (changes.invigilator_id !== 'sbc') {
          changes.sbc_staff_invigilated = 0
        }
        if (changes.invigilator_id === 'sbc') {
          changes.invigilator_id = null
          changes.sbc_staff_invigilated = 1
        }
        if (this.rescheduling) {
          changes.invigilator_id = null
          changes.sbc_staff_invigilated = 0
          this.rescheduling = false
        }
      }
      if (this.editedFields.includes('shadow_invigilator')) {
        if (this.removeFlag) {
          changes.shadow_invigilator_id = null
        } else {
          changes.shadow_invigilator_id = this.shadowInvigilator
        }
        if (this.rescheduleShadowInvigilator !== null) {
          changes.shadow_invigilator_id = this.shadowInvigilator
        }
      }
      if (this.editedFields.includes('contact_information')) {
        changes.booking_contact_information = this.booking_contact_information
      }
      
      if (!this.editedFields.includes('stat_flag')) {
        changes.stat_flag = this.stat_flag
      }
      if (this.editedFields.includes('invigilator_id')) {
        changes.invigilator_id = this.invigilator
      }
      if (this.editedFields.includes('blackout_notes')) {
        changes.blackout_notes = this.blackout_notes
      }
      if (Object.keys(changes).length === 0) {
        this.message = 'No Changes Made'
      } else {
        const invigilatorPayload: any = {
          id: null,
          params: null
        }
        const changePayload: any = {
          id: null,
          params: null
        }
        if (this.removeFlag) {
          invigilatorPayload.id = this.currentShadowInvigilator
          invigilatorPayload.params = '?add=False&subtract=True'
        } else if (this.rescheduleShadowInvigilator !== null) {
          invigilatorPayload.id = this.rescheduleShadowInvigilator
          invigilatorPayload.params = '?add=False&subtract=True'
          this.rescheduleShadowInvigilator = null
        } else if (this.shadowInvigilator && this.currentShadowInvigilator) {
          invigilatorPayload.id = this.shadowInvigilator
          invigilatorPayload.params = '?add=True&subtract=False'
          changePayload.id = this.currentShadowInvigilator
          changePayload.params = '?add=False&subtract=True'
        } else if (this.shadowInvigilator && !this.currentShadowInvigilator) {
          invigilatorPayload.id = this.shadowInvigilator
          invigilatorPayload.params = '?add=True&subtract=False'
        }
        changes.invigilator_id = this.invigilator
        if (invigilatorPayload.id) {
          this.putInvigilatorShadow(invigilatorPayload)
        }
        if (changePayload.id) {
          this.putInvigilatorShadow(changePayload)
        }
        const payload: any = {
          id: this.event.id,
          changes
        }
        if (changes.invigilator_id === 'sbc') {
          delete changes.invigilator_id
        }
        if (!this.stat_flag) { 
          if (!this.edit_recurring) {
            this.putBooking(payload).then(() => {
              setTimeout(() => {
                this.$root.$emit('initialize')
                this.finishBooking()
                this.resetModal()
              }, 250)
            })
          } else {
            // remove start and end times to ensure that recurring events do get moved to the date of
            // the event that was clicked
            delete changes.start_time
            delete changes.end_time
            payload.recurring_uuid = this.event.recurring_uuid
            this.putRecurringBooking(payload).then(() => {
              setTimeout(() => {
                this.$root.$emit('initialize')
                this.finishBooking()
                this.resetModal()
                this.edit_recurring = false
              }, 250)
            })
          }
        } else {
          if (this.is_Support){
            const stat_payload: any = {
              id: this.event.id,
              changes : { blackout_notes: this.blackout_notes}
            }
            this.putBooking(stat_payload).then(() => {
                setTimeout(() => {
                  this.$root.$emit('initialize')
                  this.finishBooking()
                  this.resetModal()
                }, 250)
              })
          }
        }
      }
      this.selectedShadow = []
      this.shadowInvigilator = null
      this.removeFlag = false
    }

  setChange () {
    this.changeState = !this.changeState
  }

  setRemove () {
    this.removeState = !this.removeState
  }

  setSelectedShadowNull (e) {
    this.removeFlag = true
    if (this.event.exam && this.event.exam.booking) {
      if (this.event.exam.booking.shadow_invigilator_id !== e) {
        if (!this.editedFields.includes('shadow_invigilator')) {
          this.editedFields.push('shadow_invigilator')
        }
      }
    }
    this.shadowInvigilator = null
    this.submit()
  }

  toggleEditRecurring () {
    this.edit_recurring = !this.edit_recurring
  }

  toggleConfirmDeleteRecurringCollapse () {
    const deleteRecurring = document.getElementById('delete_recurring_collapse')
    const confirmDelete = document.getElementById('confirm_delete_recurring_collapse')
    if (deleteRecurring) {
      if (deleteRecurring.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', 'delete_recurring_collapse')
      }
    }
    if (confirmDelete) {
      if (confirmDelete.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse', 'confirm_delete_recurring_collapse')
      }
    }
  }

  toggleConfirmStatDeleteRecurringCollapse () {
    const deleteRecurring = document.getElementById('delete_recurring_stat_collapse')
    const confirmDelete = document.getElementById('confirm_delete_recurring_stat_collapse')
    if (deleteRecurring) {
      if (deleteRecurring.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', 'delete_recurring_stat_collapse')
      }
    }
    if (confirmDelete) {
      if (confirmDelete.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse', 'confirm_delete_recurring_stat_collapse')
      }
    }
  }

  toggleConfirmStatCurrOffDeleteRecurringCollapse () {
    const deleteRecurring = document.getElementById('delete_recurring_stat_curroff_collapse')
    const confirmDelete = document.getElementById('confirm_delete_recurring_stat_curroff_collapse')
    if (deleteRecurring) {
      if (deleteRecurring.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', 'delete_recurring_stat_curroff_collapse')
      }
    }
    if (confirmDelete) {
      if (confirmDelete.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse', 'confirm_delete_recurring_stat_curroff_collapse')
      }
    }
  }

  toggleStatDeleteRecurringCollapse () {
    const deleteRecurring = document.getElementById('delete_recurring_stat_collapse')
    const confirmDelete = document.getElementById('confirm_delete_recurring_stat_collapse')
    if (deleteRecurring) {
      if (deleteRecurring.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse', 'delete_recurring_stat_collapse')
      }
    }
    if (confirmDelete) {
      if (confirmDelete.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', 'confirm_delete_recurring_stat_collapse')
      }
    }
  }

  toggleStatCurrOffDeleteRecurringCollapse () {
    const deleteRecurring = document.getElementById('delete_recurring_stat_curroff_collapse')
    const confirmDelete = document.getElementById('confirm_delete_recurring_stat_curroff_collapse')
    if (deleteRecurring) {
      if (deleteRecurring.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse', 'delete_recurring_stat_curroff_collapse')
      }
    }
    if (confirmDelete) {
      if (confirmDelete.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', 'confirm_delete_recurring_stat_curroff_collapse')
      }
    }
  }

  toggleDeleteRecurringCollapse () {
    const deleteRecurring = document.getElementById('delete_recurring_collapse')
    const confirmDelete = document.getElementById('confirm_delete_recurring_collapse')
    if (deleteRecurring) {
      if (deleteRecurring.style.display === 'none') {
        this.$root.$emit('bv::toggle::collapse', 'delete_recurring_collapse')
      }
    }
    if (confirmDelete) {
      if (confirmDelete.classList.contains('show')) {
        this.$root.$emit('bv::toggle::collapse', 'confirm_delete_recurring_collapse')
      }
    }
  }
}
</script>

<style scoped>
.table-responsive {
  line-height: 5px;
}
</style>
