<template>
  <b-modal
    v-model="modalVisible"
    @shown="show"
    size="md"
    modal-class="q-modal"
    body-class="q-modal"
    no-close-on-backdrop
    no-close-on-esc
    hide-header
    class="appt-modal"
  >
    <div id="navi">
      <template v-if="this.$store.state.showServeCitizenSpinner">
        <div class="q-loader2"></div>
      </template>
    </div>
    <template slot="modal-footer">
      <div class="d-flex flex-row-reverse">
        <b-button
          class="disabled btn-primary ml-2"
          v-if="(submitDisabled) && (!submitStat)"
          @click="validate = true"
          >Submit</b-button
        >
        <b-button
          class="btn-primary ml-2"
          @click="submit"
          v-if="(!submitDisabled) && (!submitDisabled)"
          >Submit</b-button
        >
        <b-button
          class="btn-primary ml-2"
          @click="submitSingleStat"
          v-if="(submitStat) && (is_Support)"
          >Submit</b-button
        >
        <b-button @click="cancel()">Cancel</b-button>
      </div>
    </template>
    <span v-if="this.editDeleteSeries && !stat_flag" style="font-size: 1.75rem"
      >Book Service Appointment Series</span
    >
    <span v-if="this.editDeleteSeries && stat_flag" style="font-size: 1.75rem"
      >Recurring STAT</span
    >
    <span
      v-if="!this.editDeleteSeries && online_flag"
      style="font-size: 1.75rem"
      >Book Service Appointment (Online)</span
    ><br />
    <span
      v-if="!this.editDeleteSeries && !online_flag"
      style="font-size: 1.75rem"
      >Book Service Appointment</span>
      <br />
    <b-form autocomplete="off" v-if="!stat_flag">
      <!--  Citizen Name and Contact Info row -->
      <b-form-row>
        <b-col cols="6">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Citizen Name</label><br />
            <b-form-input v-if="isNotBlackoutFlag" v-model="citizen_name" />
            <b-form-input v-else v-model="citizen_name" readonly />
          </b-form-group>
        </b-col>
        <b-col cols="6">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Send Confirmation</label><br />
            <b-form-input
              v-if="isNotBlackoutFlag"
              v-model="contact_information"
              class="contact"
              placeholder="By email or SMS Text"
            />
            <b-form-input v-else v-model="contact_information" readonly />
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of Citizen Name and Contact Info row -->

      <!--  The Time and Date row. -->
      <b-form-row>
        <b-col cols="4">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Time</label><br />
            <b-form-input :value="displayStart" disabled />
            <b-button
                v-show="allow_reschedule"
                variant="primary"
                class="mr-3"
                @click="editAppointTime"
              >
                <font-awesome-icon
                  icon="edit"
                  class="p0"
                />
              </b-button>
          </b-form-group>
        </b-col>
        <b-col cols="8">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Date</label><br />
            <b-form-input :value="displayDate" disabled />
            <b-button
                v-show="allow_reschedule"
                variant="primary"
                class="mr-3"
                @click="editAppointDate"
              >
                <font-awesome-icon
                  icon="edit"
                  class="p0"
                />
              </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of the Time and Date row. -->
       <!--  The Time and Date edit row. -->
      <b-form-row>
        <b-col cols="4">
          <b-form-group class="mb-0 mt-2">
            <label v-if="allow_time_edit" class="mb-0">Select Time</label><br />
            <vue-timepicker
                v-if="allow_time_edit"
                id="app_timepicker_id"
                v-model="app_start_time"
                class="w-100"
                icon="clock"
                editable
                format="hh:mm A"
                locale="en-US"
                @change="setStartDateTime(true)"
                @input="setStartDateTime(true)"
                manual-input>
            </vue-timepicker>
            <br/>
            <span class="danger" v-if="time_msg">{{time_msg}}</span>
          </b-form-group>
        </b-col>
        <b-col cols="8">
          <b-form-group class="mb-0 mt-2">
            <label v-if="allow_date_edit" class="mb-0">Select Date</label><br />
            <DatePicker
              v-if="allow_date_edit"
              v-model="app_start_date"
              type="date"
              lang="en"
              class="w-100"
              @change="setStartDateTime(false)"
              @input="setStartDateTime(false)"
            >
            </DatePicker>
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of the Time and Date edit row. -->
      <!--  Service selected by the citizen row -->
      <b-form-row>
        <b-col>
          <b-form-group v-if="isNotBlackoutFlag" class="mb-0 mt-2">
            <label class="mb-0">Service Required by Citizen</label><br />
            <div style="width: 100%; display: flex">
              <b-input-group>
                <b-input-group-prepend>
                  <b-button-group>
                    <b-button
                      variant="primary"
                      class="px-0"
                      style="width: 52px"
                      @click="addService"
                      >{{ selectedService ? 'Edit' : 'Set' }}</b-button
                    >
                    <b-button
                      variant="secondary"
                      v-if="selectedService"
                      class="px-0"
                      style="width: 52px; border-radius: 0px"
                      @click="clearService"
                      >Clear</b-button
                    >
                  </b-button-group>
                </b-input-group-prepend>
                <b-form-input
                  disabled
                  :state="validated.selectedService"
                  :value="service_name"
                />
              </b-input-group>
            </div>
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of service selected by the citizen row -->
            <!--  The Date/Time row -->
      <b-form-row>
        <b-col>
          <b-form-group v-if="isNotBlackoutFlag" class="mb-0 mt-2">
            <label class="mb-0">Length</label><br />
            <b-select v-model="selectLength" :options="lengthOptions" @input="serviceTime"/>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group v-if="isNotBlackoutFlag && allow_reschedule" class="mb-0 mt-2">
            <label class="mb-0">Change Date/Time</label><br />
            <b-button @click="reschedule" class="btn-secondary w-100"
              >Reschedule</b-button
            >
          </b-form-group>
          <b-form-group v-if="isNotBlackoutFlag && !allow_reschedule" class="mb-0 mt-2">
            <label class="mb-0">Change Date/Time</label><br />
            <span id="disabled-wrapper">
            <b-button disabled @click="reschedule" class="btn-secondary w-100"
              >Reschedule</b-button>
            </span>
          </b-form-group>
          <b-tooltip target="disabled-wrapper">Appointments in the past can't be rescheduled - please create new appointment</b-tooltip>
        </b-col>
        <!--  Column to delete blackout period or series (if a clicked appointment?) -->
        <b-col v-if="clickedAppt">
          <b-form-group class="mb-0 mt-2">
            <label v-if="this.editDeleteSeries" class="mb-0"
              >Remove Appointment</label
            >
            <label v-else class="mb-0">Remove Appointment</label><br />
            <b-button
              v-if="clickedAppt && !this.editDeleteSeries"
              @click="deleteAppt"
              class="btn-danger w-100"
            >
              Delete
            </b-button>
            <b-button
              v-else
              @click="deleteRecurringAppts"
              class="btn-danger w-100"
            >
              Delete Series
            </b-button>
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of the Date/Time row -->

      <!--  The Notes row. -->
      <b-form-row>
        <b-col>
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Notes</label><br />
            <b-textarea v-model="comments" maxlength="255" rows="2" />
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of the Notes row. -->
    </b-form>
    <b-form autocomplete="off" v-if="stat_flag">
      <!--  Citizen Name and Contact Info row -->
      <b-form-row>
        <b-col cols="6">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Citizen Name</label><br />
            <b-form-input v-model="citizen_name" readonly />
          </b-form-group>
        </b-col>
        <b-col cols="6">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Contact Info</label><br />
            <b-form-input v-model="contact_information" readonly />
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of Citizen Name and Contact Info row -->

      <!--  The Time and Date row. -->
      <b-form-row>
        <b-col cols="4">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Time</label><br />
            <b-form-input :value="displayStart" disabled />
          </b-form-group>
        </b-col>
        <b-col cols="8">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Date</label><br />ee
            <b-form-input :value="displayDate" disabled />
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col >
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Note</label><br />
            <b-form-input v-if="is_Support" v-model="comments" maxlength="255"/>
            <b-form-input v-else :value="comments" disabled/>
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of the Time and Date row. -->

      <!--  The Date/Time row -->
      <b-form-row v-if="is_Support">
        <!--  Column to delete blackout period or series (if a clicked appointment?) -->
        <b-col v-if="clickedAppt">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0"
              >Remove STAT</label
            >
            <br />
            <b-row>
              <v-col>
                <b-button
                  @click="deleteAppt"
                  class="btn-danger w-100"
                >
                  Delete STAT
                </b-button>
              </v-col>
            </b-row>
            <b-row>
              <v-col>
                <b-button
                    @click="deleteRecurringAppts"
                    class="btn-danger w-100"
                  >
                    Delete STAT Series from this Office
                  </b-button>
              </v-col>
            </b-row>
            <b-row>
              <v-col>
                <b-button
                    @click="deleteRecurringStatAppts"
                    class="btn-danger w-100"
                  >
                    Delete All STAT Series
                  </b-button>
              </v-col>
            </b-row>
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of the Date/Time row -->

    </b-form>
    <div class="d-flex flex-row-reverse mt-2 mb-0">
      <div v-if="showMessage" style="color: red" class="mb-0">
        Please complete all required fields.
      </div>
    </div>
  </b-modal>
</template>

<script lang="ts">
/* eslint-disable */
import { Action, namespace } from 'vuex-class'
import { Component, Prop, Vue } from 'vue-property-decorator'
import DatePicker from 'vue2-datepicker'
import VueTimepicker from 'vue2-timepicker'
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
export default class ApptBookingModal extends Vue {
  @Prop({ default: '' })
  private clickedTime!: any

  @Prop({ default: '' })
  private clickedAppt!: any

  @appointmentsModule.State('showApptBookingModal') private showApptBookingModal!: any
  @appointmentsModule.State('selectedService') private selectedService!: any
  @appointmentsModule.State('editDeleteSeries') private editDeleteSeries!: any
  @appointmentsModule.State('apptRescheduling') private apptRescheduling!: any
  @appointmentsModule.State('submitClicked') private submitClicked!: any

  @appointmentsModule.Getter('services') private services!: any
  @appointmentsModule.Getter('appointment_events') private appointment_events!: any
  @appointmentsModule.Getter('is_Support') private is_Support!: any;


  @appointmentsModule.Action('clearAddModal') public clearAddModal: any
  @appointmentsModule.Action('deleteAppointment') public deleteAppointment: any
  @appointmentsModule.Action('deleteRecurringAppointments') public deleteRecurringAppointments: any
  @appointmentsModule.Action('deleteRecurringStatAppointments') public deleteRecurringStatAppointments: any
  @appointmentsModule.Action('getAppointments') public getAppointments: any
  @appointmentsModule.Action('getServices') public getServices: any
  @appointmentsModule.Action('postAppointment') public postAppointment: any
  @appointmentsModule.Action('putAppointment') public putAppointment: any
  @appointmentsModule.Action('putRecurringAppointment') public putRecurringAppointment: any
  @appointmentsModule.Action('resetAddModalForm') public resetAddModalForm: any
  @appointmentsModule.Action('toggleAddModal') public toggleAddModal: any

  @appointmentsModule.Mutation('setEditedStatus') public setEditedStatus: any
  @appointmentsModule.Mutation('setSelectedService') public setSelectedService: any
  @appointmentsModule.Mutation('setRescheduling') public setRescheduling: any
  @appointmentsModule.Mutation('toggleApptBookingModal') public toggleApptBookingModal: any
  @appointmentsModule.Mutation('toggleEditDeleteSeries') public toggleEditDeleteSeries: any
  @appointmentsModule.Mutation('toggleSubmitClicked') public toggleSubmitClicked: any
  @Action('deleteRecurringStatBooking') public deleteRecurringStatBooking: any
  @Action('deleteRecurringStatAllOfficeBooking') public deleteRecurringStatAllOfficeBooking: any
  @Action('finishBooking') public finishBooking: any
  

  public baseEnd: any = null
  public booking: boolean = false
  public citizen_id: any = null
  public citizen_name: any = null
  public oldLength: any = null
  public comments: any = null
  public contact_information: any = null
  public fieldsEdited: boolean = false
  public length: any = 15
  public selectingService: boolean = false
  public showMessage: boolean = false
  public start: any = null
  public validate: boolean = false
  public online_flag: boolean = false
  public allow_reschedule : boolean = false
  public stat_flag: boolean = false 
  public stat_single_edit: boolean = false
  public allow_time_edit: boolean = false
  public allow_date_edit: boolean = false
  public selectedServiceObj: any =  null
  public lengthOptions: any = []
  public appt_time: any = null
  public appt_date: any = null
  public curr_date: any = null
  public selectLength: any = ""
  public is_first_edit: boolean = false
  public time_msg: any = ''
  public shallDisable: boolean = false
  public app_start_time: any = null
  public app_start_date: any = null


  get appointments () {
    if (this.clickedAppt) {
      const appointments = Object.assign([], this.appointment_events)
      const i = this.appointment_events.indexOf(this.clickedAppt)
      appointments.splice(i, 1)
      return appointments
    }
  }

  get isNotBlackoutFlag () {
    if (this.clickedAppt) {
      if (this.clickedAppt.blackout_flag) {
        if (this.clickedAppt.blackout_flag == 'Y') {
          return false
        } else if (this.clickedAppt.blackout_flag == 'N') {
          return true
        }
      } else {
        return true
      }
    }
    return true
  }

  get end () {
    if (this.app_start_time && this.app_start_date) {
        const start = this.app_start_time ? this.convertTimePickerValue(this.app_start_time) : this.app_start_time
        return moment(start).clone().add(this.length, 'minutes')
    }
    if (this.clickedTime) {
      return moment(this.clickedTime.start).clone().add(this.length, 'minutes')
    }
    if (this.clickedAppt) {
      return moment(this.clickedAppt.start).clone().add(this.length, 'minutes')
    }
  }

  serviceTime () {
    this.length = this.selectLength
    this.time_msg = ''
    this.shallDisable = false
  }
  timeOptions () {
    if (this.clickedTime) {
      const event = this.clickedTime
      const time = 60
      for (let l = 15; l <= time; l += 15) {
        if (!this.lengthOptions.includes(l)) {
          this.lengthOptions.push(l)
        }
      }
      this.lengthOptions.push(75)
      return this.lengthOptions
    }
    if (this.clickedAppt) {
      const event = this.clickedAppt
      const time = 60
      for (let l = 15; l <= time; l += 15) {
        if (!this.lengthOptions.includes(l)) {
          this.lengthOptions.push(l)
        }
      }
      this.lengthOptions.push(75)
      return this.lengthOptions
    }
    const timeDefault = 60
    if (this.selectedServiceObj) {
      this.selectLength = 15
      if (this.selectedServiceObj.timeslot_duration) {
          this.selectLength = this.selectedServiceObj.timeslot_duration
      }
    } else {
      if (this.clickedAppt) {
        if (this.clickedAppt.start && this.clickedAppt.end ) {
          this.length = this.clickedAppt.end.diff(this.clickedAppt.start, 'minutes')
          this.selectLength = this.clickedAppt.end.diff(this.clickedAppt.start, 'minutes')
        }
      } else {
        this.selectLength = 15
      }
    }
    for (let l = 15; l <= timeDefault; l += 15) {
      if (!this.lengthOptions.includes(l)) {
          this.lengthOptions.push(l)
        }
    }
    this.lengthOptions.push(75)
    return this.lengthOptions
  }

  get service_name () {
    this.$store.commit('setDisplayServices', 'Dashboard')
    const services = this.$store.getters.filtered_services
      if (services && services.length > 0) {
        if (this.selectedService) {
          this.selectedServiceObj = services.find(srv => srv.service_id === this.selectedService)
          if (this.selectedServiceObj.timeslot_duration) {
            if (this.clickedAppt && !this.is_first_edit) {
              if (this.clickedAppt.start && this.clickedAppt.end ) {
              const serviceMin =this.clickedAppt.end.diff(this.clickedAppt.start, 'minutes')
              if (!this.lengthOptions.includes(serviceMin)) {
                this.lengthOptions.push(serviceMin)
              }
              }
            } else {
            if (!this.lengthOptions.includes(this.selectedServiceObj.timeslot_duration)) {
                this.lengthOptions.push(this.selectedServiceObj.timeslot_duration)
              }
              this.selectLength = this.selectedServiceObj.timeslot_duration
            }
          }
          return this.selectedServiceObj.service_name
        }
      }
    this.lengthOptions = []
    this.timeOptions()
    this.length = this.selectLength
    return 'Please choose a service'
  }

  get displayDate () {
    if (this.app_start_date) {
      // JSTOTS TOCHECK removed new from mopment. no need to use new with moment
      return moment(this.app_start_date).clone().format('dddd MMMM Do, YYYY')
    }
    if (this.clickedTime) {
      // JSTOTS TOCHECK removed new from mopment. no need to use new with moment
      return moment(this.clickedTime.start).clone().format('dddd MMMM Do, YYYY')
    }
    if (this.clickedAppt) {
      // JSTOTS TOCHECK removed new from mopment. no need to use new with moment
      return moment(this.clickedAppt.start).clone().format('dddd MMMM Do, YYYY')
    }
    return ''
  }

  get displayStart () {
    if (this.app_start_time) {
      // JSTOTS TOCHECK removed new from mopment. no need to use new with moment
      const start = this.app_start_time ? this.convertTimePickerValue(this.app_start_time) : this.app_start_time
      return moment(start).clone().format('h:mm a')
    }
    if (this.clickedTime) {
      // JSTOTS TOCHECK removed new from mopment. no need to use new with moment
      return moment(this.clickedTime.start).clone().format('h:mm a')
    }
    if (this.clickedAppt) {
      // JSTOTS TOCHECK removed new from mopment. no need to use new with moment
      return moment(this.clickedAppt.start).clone().format('h:mm a')
    }
    return ''
  }

  get modalVisible () {
     return this.showApptBookingModal  
  }

  set modalVisible (e) { this.toggleApptBookingModal(e) }

  get submitDisabled () {
    if (this.citizen_name && this.selectedService && (!this.shallDisable)) {
      return false
    }
    return true
  }

  get submitStat () {
    if (this.stat_flag) {
      return true
    }
    return false
  }

  get validated () {
    const output: any = {}
    if (!this.citizen_name) {
      output.citizen_name = false
    }
    if (!this.selectedService) {
      output.selectedService = false
    }
    if (this.validate && Object.keys(output).length > 0) {
      this.showMessage = true
      return output
    }
    this.showMessage = false
    return {
      citizen_name: null,
      selectedService: null
    }
  }

  addService () {
    this.selectingService = true
    this.is_first_edit = true
    this.clearMessage()
    this.toggleApptBookingModal(false)
    this.toggleAddModal(true)
    if (this.selectedService) {
      this.$store.commit('updateAddModalForm', { type: 'service', value: this.selectedService })
      return
    }
    this.clearService()
  }

  clearEvents () {
    this.$root.$emit('clear-clicked-time')
    if (!this.apptRescheduling && !this.selectingService) {
      this.$root.$emit('clear-clicked-appt')
    }
  }

  clearMessage () {
    this.validate = false
    this.showMessage = false
  }

  clearService () {
    this.clearMessage()
    this.clearAddModal()
    this.resetAddModalForm()
  }

  deleteAppt () {
    this.$store.commit('toggleServeCitizenSpinner', true)
    this.deleteAppointment(this.clickedAppt.appointment_id).then(() => {
      this.cancel()
      this.$store.commit('toggleServeCitizenSpinner', false)
    })
    this.stat_flag = false
  }

  deleteRecurringAppts () {
    this.$store.commit('toggleServeCitizenSpinner', true)
    this.deleteRecurringAppointments(this.clickedAppt.recurring_uuid).then(() => {
      this.deleteRecurringStatBooking(this.clickedAppt.recurring_uuid).then(() => {
        this.finishBooking()
      })
      this.cancel()
      this.$store.commit('toggleServeCitizenSpinner', false)
    })
    this.stat_flag = false
  }

  deleteRecurringStatAppts () {
    this.$store.commit('toggleServeCitizenSpinner', true)
    this.deleteRecurringStatAppointments(this.clickedAppt.recurring_uuid).then(() => {
      this.deleteRecurringStatAllOfficeBooking(this.clickedAppt.recurring_uuid).then(() => {
        this.finishBooking()
      })
      this.cancel()
      this.$store.commit('toggleServeCitizenSpinner', false)
    })
    this.stat_flag = false
  }

  reschedule () {
    if (this.clickedTime) {
      this.$root.$emit('removeTempEvent')
    }
    this.$router.push('/appointments')

    this.$store.commit('toggleEditApptModal', false)
    this.$store.commit('toggleRescheduling', true)
    this.$store.commit('toggleApptEditMode', true)
    this.clearMessage()
    this.oldLength = this.length
    this.toggleApptBookingModal(false)
    this.setRescheduling(true)
  }

  cancel () {
    this.$root.$emit('removeTempEvent')
    this.$root.$emit('clear-clicked-time')
    this.$root.$emit('clear-clicked-appt')
    this.toggleApptBookingModal(false)
    this.setRescheduling(false)
    this.allow_time_edit = false
    this.allow_date_edit = false
    this.stat_flag = false
    this.start = null
    this.appt_time = null
    this.appt_date = null
    this.selectedServiceObj = null
    this.setSelectedService(null)
    this.is_first_edit = false
    // this.timeOptions()
    this.app_start_time = null
    this.app_start_date = null
  }

  show () {
    if (!this.selectedServiceObj) {
      this.start = null
      this.appt_time = null
      this.appt_date = null
      this.curr_date = null
      this.app_start_time = null
      this.app_start_date = null
    }
    this.clearMessage()
    if (this.selectingService) {
      this.selectingService = false
      return
    }
    if (this.apptRescheduling) {
      this.$store.commit('toggleRescheduling', false)
      this.setRescheduling(false)
      this.start = new Date(this.clickedTime.start.format())
      this.app_start_date = new Date(this.clickedTime.start.format('YYYY/MM/DD'))
      this.app_start_time = {
        'hh': this.clickedTime.start.format('hh'),
        'mm': this.clickedTime.start.format('mm'),
        'A': this.clickedTime.start.format('A')
      }
      this.curr_date = new Date(this.clickedTime.start.format())
      this.length = this.clickedTime.end.clone().diff(this.start, 'minutes')
      if (this.oldLength) {
        if (this.oldLength < this.length) {
          this.length = this.oldLength
        }
        this.oldLength = null
      }

      // Handles case when re-schedulng from the Agenda panel on The Queue
      if (this.clickedAppt && this.clickedAppt.end) {
        this.citizen_name = this.clickedAppt.title
        this.comments = this.clickedAppt.comments
        this.contact_information = this.clickedAppt.contact_information
        this.length = this.clickedAppt.end.clone().diff(this.clickedAppt.start, 'minutes')
        this.online_flag = this.clickedAppt.online_flag
        this.stat_flag = this.clickedAppt.stat_flag
        const { service_id } = this.clickedAppt
        this.setSelectedService(service_id)
        this.$store.commit('updateAddModalForm', { type: 'service', value: service_id })
      }

      return
    }
    if (this.clickedTime) {
      this.citizen_name =
      this.comments = null
      this.contact_information = null
      this.length = 15
      this.start = new Date(this.clickedTime.start.format())
      this.app_start_date = new Date(this.clickedTime.start.format('YYYY/MM/DD'))
      this.app_start_time = {
        'hh': this.clickedTime.start.format('hh'),
        'mm': this.clickedTime.start.format('mm'),
        'A': this.clickedTime.start.format('A')
      }
      this.curr_date = new Date(this.clickedTime.start.format())
       
      this.clearAddModal()
    }
    if (this.clickedAppt && this.clickedAppt.end) {
      // Incident INC0040389  - Appointments in Past can only be deleted not rescheduled
      if (this.clickedAppt.start && this.clickedAppt.end ) {
        this.length = this.clickedAppt.end.diff(this.clickedAppt.start, 'minutes')
        this.selectLength = this.clickedAppt.end.diff(this.clickedAppt.start, 'minutes')
      }
      this.allow_reschedule = true
      if (this.clickedAppt.start < moment.now()) {
          this.allow_reschedule = false
      }
      this.citizen_name = this.clickedAppt.title
      this.comments = this.clickedAppt.comments
      this.contact_information = this.clickedAppt.contact_information
      this.start = new Date(this.clickedAppt.start.format())
      this.app_start_date = new Date(this.clickedAppt.start.format('YYYY/MM/DD'))
      this.app_start_time = {
        'hh': this.clickedAppt.start.format('hh'),
        'mm': this.clickedAppt.start.format('mm'),
        'A': this.clickedAppt.start.format('A')
      }
      this.curr_date = new Date(this.clickedAppt.start.format())
      this.online_flag = this.clickedAppt.online_flag
      this.stat_flag = this.clickedAppt.stat_flag
      const { service_id } = this.clickedAppt
      this.setSelectedService(service_id)
      this.$store.commit('updateAddModalForm', { type: 'service', value: service_id })
    } else {
      this.citizen_name = ''
      this.comments = ''
      this.contact_information = ''
      this.start = null
      this.app_start_date = null
      this.app_start_time = null
      this.curr_date = null
      //todo, remove if consditon
      if (this.clickedTime) {
      this.start = new Date(this.clickedTime.start.format())
      this.app_start_date = new Date(this.clickedTime.start.format('YYYY/MM/DD'))
      this.app_start_time = {
        'hh': this.clickedTime.start.format('hh'),
        'mm': this.clickedTime.start.format('mm'),
        'A': this.clickedTime.start.format('A')
      }
      this.curr_date = new Date(this.clickedTime.start.format())
      }
    }
    var now = new Date();
    if (this.start > now) {
        this.allow_reschedule = true
      }else {
        this.allow_reschedule = false
      }
  }

  submit () {
    this.length = this.selectLength
    if (!this.submitClicked && this.end) {
      // CSR TIME VALIDATION
      const start_time = this.app_start_time ? this.convertTimePickerValue(this.app_start_time) : this.app_start_time
      this.start = start_time
      let validate_flag = false
      if (this.app_start_time.hh === '') {
        this.time_msg = "Time is Invalid"
        validate_flag = true
      }
      if (start_time) {
        if ((new Date(start_time).getHours() <= 8) || (new Date(start_time).getHours() >= 17)){
          if ((new Date(start_time).getHours() === 8)) {
            if ((new Date(start_time).getMinutes() < 30)) {
                this.time_msg = "Selected length/time is not within the office time"
                validate_flag = true
            } 
          } else if (new Date(start_time).getHours() === 17) {
            if ((new Date(start_time).getMinutes() > 0)) {
                this.time_msg = "Selected length/time is not within the office time"
                validate_flag = true
            } 
          } else {
            this.time_msg = "Selected length/time is not within the office time"
            validate_flag = true
          }
        }
      }
      if (this.end) {
        if ((new Date(this.end.format()).getHours() <= 8) || (new Date(this.end.format()).getHours() >= 17)){
          if ((new Date(this.end.format()).getHours() === 8)) {
            if ((new Date(this.end.format()).getMinutes() < 30)) {
                this.time_msg = "Selected length/time is not within the office time"
                validate_flag = true
            } 
          } else if (new Date(this.end.format()).getHours() === 17) {
            if ((new Date(this.end.format()).getMinutes() > 0)) {
                this.time_msg = "Selected length/time is not within the office time"
                validate_flag = true
            }
          } else {
            this.time_msg = "Selected length/time is not within the office time"
            validate_flag = true
          }
        }
      }
      if (validate_flag) {
        this.shallDisable = true
        return false
      }
      this.time_msg = ''
    // END
      this.toggleSubmitClicked(true)
      this.$store.commit('toggleServeCitizenSpinner', true)
      this.clearMessage()
      const service_id = this.selectedService
      const startDateObj = start_time
      if (!moment.isMoment(start_time)) {
        this.start = moment(start_time)
      }
      const start = moment(moment.tz(this.start.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).format()).clone()
      const end = moment(moment.tz(this.end.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).format()).clone()
      
      this.start = startDateObj
      const e: any = {
        start_time: moment.utc(start).format(),
        end_time: moment.utc(end).format(),
        service_id,
        citizen_name: this.citizen_name,
        contact_information: this.contact_information
      }
      if (this.comments) {
        e.comments = this.comments
      }
      const finish = () => {
        this.cancel()
        this.$root.$emit('clear-clicked-appt')
        this.$root.$emit('clear-clicked-time')
      }
      this.$store.commit('toggleRescheduling', false)
      this.$store.commit('toggleApptEditMode', false)
      if (this.clickedAppt) {
        const payload = {
          id: this.clickedAppt.appointment_id,
          data: e
        }
        if (!this.stat_single_edit) {
          if (this.editDeleteSeries === true) {
            // IFF further fields are added to the appointment model that are intended to be edited,
            // and they belong to blackouts, and them to the following object below. Ensure that dates are
            // not included as all events in this series will be under the start/end time of the event
            // that is clicked in the calendar
            this.toggleEditDeleteSeries(false)
            const re_e: any = {
              comments: this.comments
            }
            const re_payload = {
              id: this.clickedAppt.appointment_id,
              data: re_e,
              recurring_uuid: this.clickedAppt.recurring_uuid
            }
            this.putRecurringAppointment(re_payload).then(() => {
              this.getAppointments().then(() => {
                finish()
                this.$store.commit('toggleServeCitizenSpinner', false)
              })
            })
          } else {
            this.putAppointment(payload).then(() => {
              this.getAppointments().then(() => {
                finish()
                this.$store.commit('toggleServeCitizenSpinner', false)
                setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
              })
            })
          }
        }  
        if (this.stat_single_edit) {
            const stat_payload = {
                id: this.clickedAppt.appointment_id,
                data: {comments: this.comments}
            }
          this.putAppointment(stat_payload).then(() => {
              this.getAppointments().then(() => {
                finish()
                this.$store.commit('toggleServeCitizenSpinner', false)
                this.stat_single_edit= true
                setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
              })
            })
        } 
        return
      }
      this.postAppointment(e).then(() => {
        this.getAppointments().then(() => {
          finish()
          this.$store.commit('toggleServeCitizenSpinner', false)
          setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
        })
      })
    }
    this.stat_flag = false
    this.is_first_edit = false
  }

  submitSingleStat (){
    this.stat_single_edit = true
    this.submit()
    this.stat_flag = false
  }

  editAppointTime () {
    this.allow_time_edit = !this.allow_time_edit
  }

  editAppointDate () {
    this.allow_date_edit = !this.allow_date_edit
  }

  mounted () {
    if (this.$store.state.services.length === 0) {
      this.getServices()
    }
    this.timeOptions()
    var now = new Date();
    if (this.start > now) {
        this.allow_reschedule = true
    } else {
      this.allow_reschedule = false
    }
  }

  convertTimePickerValue(model:any){
    if (this.app_start_date && this.app_start_time) {
      const currentDate = this.app_start_date
      const fullformat = moment(model.hh + ':' + model.mm + ' ' + model.A ,'hh:mm A').format('HH:mm:ss')
      const day = currentDate.getDate().toString().length === 1 ? '0' + currentDate.getDate().toString() : currentDate.getDate().toString()
      const month = currentDate.getMonth().toString().length === 1 ? '0' + (currentDate.getMonth() + 1).toString() : (currentDate.getMonth() + 1).toString()
      const year = currentDate.getFullYear()
      return new Date(year + '-' + month + '-' + day + ' ' + fullformat)
    }   
  }
  setStartDateTime(is_time) {
    this.start = new Date(moment(this.app_start_date).format('YYYY/MM/DD')+' '+this.app_start_time)
    this.time_msg = ''
    const start_time = this.app_start_time ? this.convertTimePickerValue(this.app_start_time) : this.app_start_time
    const startDateObj = moment(start_time)
    const currDateObj = moment(this.curr_date)
    if (is_time) {
      this.appt_time = startDateObj.format('HH:mm:ss')
      if (this.clickedTime || this.clickedAppt) {
        if ( this.curr_date) {
          if (this.appt_time && !this.appt_date) {
              this.start = new Date(currDateObj.format('YYYY-MM-DD')+' '+this.appt_time)
          }
        }
      }
    } else {
      this.appt_date = startDateObj.format('YYYY-MM-DD')
      if (this.clickedTime || this.clickedAppt) {
        if ( this.curr_date) {
          if (!this.appt_time && this.appt_date) {
            this.start = new Date(this.appt_date+' '+currDateObj.format('HH:mm:ss'))
          }
        }
      }
    }
    if (this.appt_time && this.appt_date) {
        this.start = new Date(this.appt_date+' '+this.appt_time)
    }
    var now = new Date();
    if (this.start > now) {
        this.allow_reschedule = true
    }else {
      this.allow_reschedule = false
    }
    this.shallDisable = false
  }
}
</script>

<style scoped>
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
#navi {
  position: relative;
}
.q-loader2 {
  position: absolute;
  z-index: 1100;
  text-align: center;
  margin: 250px auto auto 175px;
  width: 50px;
  height: 50px;
  border: 10px solid LightGrey;
  opacity: 0.9;
  border-radius: 50%;
  border-top-color: DodgerBlue;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}

.danger {
  color: red !important;
}
</style>
