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
          v-if="submitDisabled"
          @click="validate = true"
          >Submit</b-button
        >
        <b-button
          class="btn-primary ml-2"
          @click="submit"
          v-if="!submitDisabled"
          >Submit</b-button
        >
        <b-button @click="cancel()">Cancel</b-button>
      </div>
    </template>
    <span v-if="this.editDeleteSeries" style="font-size: 1.75rem"
      >Book Service Appointment Series</span
    >
    <span
      v-if="!this.editDeleteSeries && online_flag"
      style="font-size: 1.75rem"
      >Book Service Appointment (Online)</span
    ><br />
    <span
      v-if="!this.editDeleteSeries && !online_flag"
      style="font-size: 1.75rem"
      >Book Service Appointment</span
    ><br />

    <b-form autocomplete="off">
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
            <label class="mb-0">Contact Info</label><br />
            <b-form-input
              v-if="isNotBlackoutFlag"
              v-model="contact_information"
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
          </b-form-group>
        </b-col>
        <b-col cols="8">
          <b-form-group class="mb-0 mt-2">
            <label class="mb-0">Date</label><br />
            <b-form-input :value="displayDate" disabled />
          </b-form-group>
        </b-col>
      </b-form-row>
      <!--  End of the Time and Date row. -->

      <!--  The Date/Time row -->
      <b-form-row>
        <b-col>
          <b-form-group v-if="isNotBlackoutFlag" class="mb-0 mt-2">
            <label class="mb-0">Length</label><br />
            <b-select v-model="length" :options="timeOptions" />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group v-if="isNotBlackoutFlag" class="mb-0 mt-2">
            <label class="mb-0">Change Date/Time</label><br />
            <b-button @click="reschedule" class="btn-secondary w-100"
              >Reschedule</b-button
            >
          </b-form-group>
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
    <div class="d-flex flex-row-reverse mt-2 mb-0">
      <div v-if="showMessage" style="color: red" class="mb-0">
        Please complete all required fields.
      </div>
    </div>
  </b-modal>
</template>

<script lang="ts">

import { Component, Prop, Vue } from 'vue-property-decorator'
import moment from 'moment'
import { namespace } from 'vuex-class'

const appointmentsModule = namespace('appointmentsModule')

@Component
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

  @appointmentsModule.Action('clearAddModal') public clearAddModal: any
  @appointmentsModule.Action('deleteAppointment') public deleteAppointment: any
  @appointmentsModule.Action('deleteRecurringAppointments') public deleteRecurringAppointments: any
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

  public baseEnd: any = null
  public booking: boolean = false
  public citizen_id: any = null
  public citizen_name: any = null
  public oldLength: any = null
  public comments: any = null
  public contact_information: any = null
  public fieldsEdited: boolean = false
  public length: any = 0
  public selectingService: boolean = false
  public showMessage: boolean = false
  public start: any = null
  public validate: boolean = false
  public online_flag: boolean = false

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
    if (this.clickedTime) {
      return moment(this.clickedTime.start).clone().add(this.length, 'minutes')
    }
    if (this.clickedAppt) {
      return moment(this.clickedAppt.start).clone().add(this.length, 'minutes')
    }
  }

  get timeOptions () {
    const options: any = []
    if (this.clickedTime) {
      const event = this.clickedTime
      const time = 60
      for (let l = 15; l <= time; l += 15) {
        options.push(l)
      }
      return options
    }
    if (this.clickedAppt) {
      const event = this.clickedAppt
      // let start = moment(event.start).clone()
      // for (let l of [15, 30, 45, 60]) {
      // let testEnd = start.clone().add(l, 'minutes')
      // if (this.appointments.find(appt => moment(appt.start).isBetween(start, testEnd))) {
      //   break
      // }
      // options.push(l)
      // }
      const time = 60
      for (let l = 15; l <= time; l += 15) {
        options.push(l)
      }

      return options
    }
  }

  get service_name () {
    this.$store.commit('setDisplayServices', 'Dashboard')
    const services = this.$store.getters.filtered_services
    if (services && services.length > 0) {
      if (this.selectedService) {
        return services.find(srv => srv.service_id === this.selectedService).service_name
      }
    }
    return 'Please choose a service'
  }

  get displayDate () {
    if (this.start) {
      // JSTOTS TOCHECK removed new from mopment. no need to use new with moment
      return moment(this.start).clone().format('dddd MMMM Do, YYYY')
    }
    return ''
  }

  get displayStart () {
    if (this.start) {
      // JSTOTS TOCHECK removed new from mopment. no need to use new with moment
      return moment(this.start).clone().format('h:mm a')
    }
    return ''
  }

  get modalVisible () { return this.showApptBookingModal }

  set modalVisible (e) { this.toggleApptBookingModal(e) }

  get submitDisabled () {
    if (this.citizen_name && this.selectedService) {
      return false
    }
    return true
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
  }

  deleteRecurringAppts () {
    this.$store.commit('toggleServeCitizenSpinner', true)
    this.deleteRecurringAppointments(this.clickedAppt.recurring_uuid).then(() => {
      this.cancel()
      this.$store.commit('toggleServeCitizenSpinner', false)
    })
  }

  reschedule () {
    if (this.clickedTime) {
      this.$root.$emit('removeTempEvent')
    }

    // need to navigate to appointments
    this.$router.push('/appointments')
    // Problem - if -rescheduling from Agenda in the queue, it loses appointment data
    // same data in clickedAppt
    // But it keeps clickedTime?
    // Idea - need to et "clickedAppt" as state.


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
  }

  show () {
    this.clearMessage()
    if (this.selectingService) {
      this.selectingService = false
      return
    }
    if (this.apptRescheduling) {
      this.$store.commit('toggleRescheduling', false)
      this.setRescheduling(false)
      this.start = this.clickedTime.start.clone()
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
      this.start = this.clickedTime.start.clone()
      this.clearAddModal()
    }
    if (this.clickedAppt && this.clickedAppt.end) {
      this.citizen_name = this.clickedAppt.title
      this.comments = this.clickedAppt.comments
      this.contact_information = this.clickedAppt.contact_information
      this.start = this.clickedAppt.start.clone()
      this.length = this.clickedAppt.end.clone().diff(this.start, 'minutes')
      this.online_flag = this.clickedAppt.online_flag
      const { service_id } = this.clickedAppt
      this.setSelectedService(service_id)
      this.$store.commit('updateAddModalForm', { type: 'service', value: service_id })
    } else {
      this.citizen_name = ''
      this.comments = ''
      this.contact_information = ''
      this.start = this.clickedTime.start.clone()
    }
  }

  submit () {
    if (!this.submitClicked) {
      this.toggleSubmitClicked(true)
      this.$store.commit('toggleServeCitizenSpinner', true)
      this.clearMessage()
      const service_id = this.selectedService
      const start = moment(this.start).clone()
      const end = moment(this.end).clone()
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
          debugger;
          this.putAppointment(payload).then(() => {
            this.getAppointments().then(() => {
              finish()
              this.$store.commit('toggleServeCitizenSpinner', false)
              setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
            })
          })
        }
        return
      }
      console.log('e', e)
      this.postAppointment(e).then(() => {
        this.getAppointments().then(() => {
          finish()
          this.$store.commit('toggleServeCitizenSpinner', false)
          setTimeout(() => { this.toggleSubmitClicked(false) }, 2000)
        })
      })
    }
  }

  mounted () {
    if (this.$store.state.services.length === 0) {
      this.getServices()
    }
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
</style>
