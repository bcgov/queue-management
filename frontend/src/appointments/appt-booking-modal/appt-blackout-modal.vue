<template>
  <b-modal v-model="modal"
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
        <b-button class="btn-primary ml-2"
                  @click="submit"
                  >
          Submit</b-button>
        <b-button @click="cancel">
          Cancel
        </b-button>
      </div>
    </template>
    <span style="font-size:1.75rem;">Schedule Appointment Blackout</span><br>
    <b-form>
      <b-form-row class="mb-2">
        <b-col cols="6">
          <label>User Name</label><br>
          <b-form-input v-model="this.user_name"
                        disabled
                        >
          </b-form-input>
        </b-col>
        <b-col cols="6">
          <label>Contact Information (optional)</label>
          <b-form-input v-model="this.user_contact_info"
                        >
          </b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col cols="6">
          <b-form-group>
            <label>Blackout Date</label><br>
            <DatePicker v-model="blackout_date"
                        id="appointment_blackout_date"
                        type="date"
                        lang="en"
                        class="w-100"
                        >
            </DatePicker>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-col cols="6">
          <b-form-group>
            <label>Blackout Start Time</label><br>
            <DatePicker v-model="start_time"
                        id="appointment_blackout_start_time"
                        :time-picker-options="{ start: '8:00', step: '00:30', end: '16:30' }"
                        lang="en"
                        format="h:mm a"
                        autocomplete="off"
                        placeholder="Select Start Time"
                        class="w-100"
                        type="time"
                        >
            </DatePicker>
          </b-form-group>
        </b-col>
        <b-col cols="6">
          <b-form-group>
            <label>Blackout End Time</label><br>
            <DatePicker v-model="end_time"
                        id="appointment_blackout_end_time"
                        :time-picker-options="{ start: '8:30', step: '00:30', end: '17:00' }"
                        lang="en"
                        format="h:mm a"
                        autocomplete="off"
                        placeholder="Select End Time"
                        class="w-100"
                        type="time"
                        >

            </DatePicker>
          </b-form-group>
        </b-col>
      </b-form-row>
      <b-form-row>
        <b-form-group class="ml-1" style="width: 465px;">
            <label>Blackout Notes (optional)</label><br>
            <b-textarea v-model="notes"
                        id="appointment_blackout_notes"
                        placeholder="Enter notes about blackout period"
                        rows="3"
                        max-rows="6"
                        size="md"
                        >
            </b-textarea>
        </b-form-group>
      </b-form-row>
    </b-form>
  </b-modal>
</template>

<script>
    import { createNamespacedHelpers } from 'vuex'
    import moment from 'moment'
    import DatePicker from 'vue2-datepicker'
    const { mapMutations, mapState, mapActions } = createNamespacedHelpers( 'appointmentsModule' )

    export default {
        name: "AppointmentBlackoutModal",
        components: { DatePicker },
        created(){
          this.user_name = "APPOINTMENT BLACKOUT PERIOD"
          this.user_contact_info = this.$store.state.user.username
        },
        data() {
          return {
            blackout_date: '',
            start_time: '',
            end_time: '',
            notes: '',
            user_name: '',
            user_contact_info: '',
          }
        },
        methods: {
          ...mapActions([
            'getAppointments',
            'postAppointment',
          ]),
          ...mapMutations([
            'toggleAppointmentBlackoutModal'
          ]),
          show(){
            this.start_time = ''
            this.end_time = ''
            this.blackout_date = ''
            this.notes = ''
          },
          cancel(){
            this.toggleAppointmentBlackoutModal(false)
          },
          submit(){
            let date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
            let start = moment(this.start_time).clone().format('HH:mm:ss')
            let start_date = moment(date + " " + start).format('YYYY-MM-DD HH:mm:ssZ')
            let end = moment(this.end_time).clone().format('HH:mm:ss')
            let end_date = moment(date + " " + end).format('YYYY-MM-DD HH:mm:ssZ')

            let e = {
              start_time: start_date,
              end_time: end_date,
              citizen_name: this.user_name,
              contact_information: this.user_contact_info,
              blackout_flag: 'Y'
            }
            if(this.notes){
              e.comments = this.notes
            }
            this.postAppointment(e).then( () => {
              this.getAppointments().then( () => {
                this.toggleAppointmentBlackoutModal(false)
              })
            })
          },
        },
        computed: {
          ...mapState({
            showAppointmentBlackoutModal: state => state.showAppointmentBlackoutModal,
          }),
          modal: {
            get() {
              return this.showAppointmentBlackoutModal
            },
            set(e) {
              this.toggleAppointmentBlackoutModal(e)
            }
          },
        }
    }
</script>

<style scoped>
</style>
