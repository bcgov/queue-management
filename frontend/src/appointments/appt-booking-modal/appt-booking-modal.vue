<template>
  <b-modal v-model="modalVisible"
           @shown="show"
           size="md"
           modal-class="q-modal"
           body-class="q-modal"
           no-close-on-backdrop
           no-close-on-esc
           hide-header>
    <template slot="modal-footer">
      <div class="d-flex flex-row-reverse">
        <b-button class="disabled btn-primary ml-2"
                  v-if="submitDisabled"
                  @click="validate=true">Submit</b-button>
        <b-button class="btn-primary ml-2"
                  @click="submit"
                  v-if="!submitDisabled">Submit</b-button>
        <b-button @click="resetModal">Cancel</b-button>
      </div>
    </template>
      <span style="font-size:1.75rem;">Book Service Appointment</span><br>
      <b-form autocomplete="off">
        <b-form-row>
          <b-col cols="6">
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Citizen Name</label><br>
              <b-form-input v-model="citizen_name"
                            @input="clearMessage()"
                            :state="validated.citizen_name"/>
            </b-form-group>
          </b-col>
          <b-col cols="6">
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Contact Info</label><br>
              <b-form-input v-model="contact_information"
                            @input="clearMessage()"/>
            </b-form-group>
          </b-col>
        </b-form-row>

        <b-form-row>
          <b-col cols="4">
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Time</label><br>
              <b-form-input :value="displayStart"
                            disabled />
            </b-form-group>
          </b-col>
          <b-col cols="8">
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Date</label><br>
              <b-form-input :value="displayDate"
                            disabled />
            </b-form-group>
          </b-col>
        </b-form-row>

        <b-form-row>
          <b-col :cols="clickedAppt ? 6 : 12">
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Change Date/Time</label><br>
              <b-button @click="reschedule"
                        class="btn-secondary w-100">Reschedule</b-button>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Remove Appointment?</label><br>
              <b-button @click="deleteAppt"
                        v-if="clickedAppt"
                        class="btn-danger w-100">Delete</b-button>
            </b-form-group>
          </b-col>
        </b-form-row>

        <b-form-row>
          <b-col>
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Service Required by Citizen</label><br>
              <div style="width: 100%; display: flex;">
                <b-input-group>
                  <b-input-group-prepend>
                    <b-button-group>
                      <b-button variant="primary"
                                class="px-0"
                                style="width: 52px"
                                @click="addService">{{ editMode ? 'Edit' : 'Set' }}</b-button>
                      <b-button variant="secondary"
                                v-if="!editMode"
                                class="px-0"
                                style="width: 52px;border-radius: 0px;"
                                @click="clearService">Clear</b-button>
                    </b-button-group>
                  </b-input-group-prepend>
                  <b-form-input disabled
                                :state="validated.selectedService"
                                :value="service_name" />
                </b-input-group>

              </div>
            </b-form-group>
          </b-col>
        </b-form-row>

        <b-form-row>
          <b-col>
            <b-form-group class="mb-0 mt-2">
              <label class="mb-0">Notes</label><br>
              <b-textarea v-model="citizen_comments"
                          rows="2" />
            </b-form-group>
          </b-col>
        </b-form-row>
      </b-form>
      <div class="d-flex flex-row-reverse mt-2 mb-0">
        <div v-if="showMessage"
             style="color: red;"
             class="mb-0">Please complete all required fields.</div>
      </div>
  </b-modal>
</template>

<script>
  import Vue from 'vue'
  import moment from 'moment'
  import { createNamespacedHelpers } from 'vuex'
  const { mapActions, mapGetters, mapMutations, mapState } = createNamespacedHelpers('appointmentsModule')

  export default {
    name: 'ApptBookingModal',
    props: ['clickedTime', 'clickedAppt'],
    data() {
      return {
        showMessage: false,
        validate: false,
        booking: false,
        start: null,
        end: null,
        citizen_comments: null,
        citizen_name: null,
        contact_information: null,
        fieldsEdited: false,
      }
    },
    mounted() {
      this.getServices()
    },
    computed: {
      ...mapGetters(['services',]),
      ...mapState(['editing', 'showApptBookingModal', 'rescheduling', 'selectedService' ]),
      appointment() {
        if (this.selectedService) {
          return this.clickedAppt.concat(this.selectedService)
        }
        let clickedAppt = this.clickedAppt
        clickedAppt.selectedService
        return this.clickedAppt
      },
      service_name() {
        let { services } = this.$store.state
        if (services && services.length > 0) {
          if (this.selectedService) {
            return services.find(srv => srv.service_id === this.selectedService).service_name
          }
        }
        return 'Please choose a service'
      },
      displayDate() {
        if (this.start) {
          return new moment(this.start).clone().format('dddd MMMM Do, YYYY')
        }
        return ''
      },
      displayEnd() {
        if (this.end) {
          return new moment(this.end).clone().format('h:mm a')
        }
        return ''
      },
      editMode() {
        if (this.clickedAppt && this.clickedAppt.start) {
          return true
        }
        return false
      },
      displayStart() {
        if (this.start) {
          return new moment(this.start).clone().format('h:mm a')
        }
        return ''
      },
      modalVisible: {
        get() { return this.showApptBookingModal },
        set(e) { this.toggleApptBookingModal(e) }
      },
      submitDisabled() {
        if (!this.clickedAppt) {
          if (this.citizen_name && this.selectedService) {
            return false
          }
          return true
        }
        if (this.clickedAppt) {
          return false
        }
        return true
      },
      validated() {
        let output = {}
        if (!this.citizen_name) {
          output.citizenName = false
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
    },
    methods: {
      ...mapActions([
        'clearAddModal',
        'deleteAppointment',
        'getAppointments',
        'getServices',
        'postAppointment',
        'putAppointment',
        'resetAddModalForm',
        'toggleAddModal',
      ]),
      ...mapMutations(['setEditedStatus', 'setSelectedService', 'setRescheduling', 'toggleApptBookingModal', ]),
      addService() {
        if (this.editMode) {
          this.setEditedStatus(true)
        }
        this.clearMessage()
        this.toggleAddModal(true)
      },
      clearMessage() {
        this.validate = false
        this.showMessage = false
      },
      clearService() {
        this.clearMessage()
        this.clearAddModal()
        this.resetAddModalForm()
      },
      reschedule() {
        this.setRescheduling(true)
        this.setEditedStatus(true)
        this.clearMessage()
        this.$root.$emit('removeTempEvent')
        this.toggleApptBookingModal(false)
      },
      resetModal() {
        this.booking = false
        this.$root.$emit('removeTempEvent')
        this.$root.$emit('clearappt')
        this.$root.$emit('cleardate')
        this.toggleApptBookingModal(false)
        this.resetAddModalForm()
      },
      show() {
        if (this.rescheduling) {
          this.setReschedulign(false)
          this.start = this.clickedAppt.start.clone()
          this.end = this.clickedAppt.end.clone()
          this.citizen_name = this.clickedAppt.title.valueOf()
        }
        if (!this.clickedAppt) {
          this.start = this.clickedTime.start.clone()
          this.end = this.clickedTime.end.clone()
          if (!this.booking) {
            this.clearAddModal()
            this.clearMessage()
            this.citizen_comments = null
            this.citizen_name = null
            this.contact_information = null
            this.booking = true
          }
          return
        }
        this.start = this.clickedAppt.start.clone()
        this.end = this.clickedAppt.end.clone()
        this.citizen_name = this.clickedAppt.title.valueOf()
        this.contact_information = this.clickedAppt.contact_information.valueOf()
        let { service_id } = this.clickedAppt
        if (!this.editing) {
          this.setSelectedService(service_id)
        }
        this.setEditedStatus(false)
      },
      deleteAppt() {
        this.deleteAppointment(this.clickedAppt.appointment_id).then( () => {
          this.resetModal()
        })
      },
      submit() {
        this.clearMessage()
        let service_id = this.selectedService
        let start = moment(this.start).clone()
        let end = moment(this.end).clone()
        let e = {
          start_time: moment.utc(start).format(),
          end_time: moment.utc(end).format(),
          service_id,
          citizen_name: this.citizen_name,
          contact_information: this.contact_information,
        }
        if (this.citizen_comments) {
          e.comments = this.citizen_comments
        }
        if (this.clickedAppt) {
          let payload = {
            id: this.clickedAppt.appointment_id,
            data: e
          }
          this.putAppointment(payload).then( () => {
            this.getAppointments().then( () => {
              this.resetModal()
              this.$root.$emit('clearappt')
              this.$root.$emit('cleardate')
            })
          })
          return
        }
        this.postAppointment(e).then( () => {
          this.getAppointments().then( () => {
            this.resetModal()
            this.$root.$emit('clearappt')
            this.$root.$emit('cleardate')
          })
        })
      }
    },
  }
</script>