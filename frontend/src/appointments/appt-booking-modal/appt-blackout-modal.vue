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
        <b-button v-if="this.recurring_input_state === 'notes' || this.single_input_state === 'notes'"
                  variant="primary"
                  class="ml-2"
                  size="md"
                  @click="submit">
          Submit</b-button>
        <b-button v-else
                  class="ml-2"
                  size="md"
                  disabled>
          Submit
        </b-button>
        <b-button v-if="this.recurring_input_state === 'event_information'"
                  variant="primary"
                  class="w-100 ml-2"
                  size="md"
                  v-b-toggle.recurring-dates-collapse
                  @click="generateRule">
          Next
        </b-button>
        <b-button v-else-if="this.single_input_state === 'event_information'"
                  variant="primary"
                  class="w-100 ml-2"
                  size="md"
                  @click="nextSingleNotes">
          Next
        </b-button>
        <b-button v-else-if="this.recurring_input_state === 'audit_information'"
                  variant="primary"
                  class="w-100 ml-2"
                  size="md"
                  @click="nextRecurringNotes">
          Next
        </b-button>
        <b-button v-else-if="this.single_input_state === 'notes' || this.recurring_input_state === 'notes'"
                  disabled
                  class="w-100 ml-2"
                  size="md">
          Next
        </b-button>
        <b-button @click="cancel"
                  size="md">
          Cancel
        </b-button>
      </div>
    </template>
    <span style="font-size:1.75rem;">Schedule Appointment Blackout</span><br>
    <b-form>
      <b-collapse id="collapse-event-selection">
        <b-card>
          <b-form-row class="mb-2">
            <label>Step 1: Select Event Type</label>
          </b-form-row>
          <b-form-row>
            <b-col class="w-50 mb-1">
              <b-button variant="primary"
                        class="w-100 mb-1"
                        v-b-toggle.collapse-single-event
                        @click="setRecurring">
                Create Single Blackout
              </b-button>
            </b-col>
            <b-col v-if="is_recurring_enabled"
                   class="w-50">
              <b-button variant="primary"
                        class="w-100 mb-1"
                        v-b-toggle.collapse-recurring-events
                        @click="setSingle">
                Create Recurring Blackout
              </b-button>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-single-event">
        <b-card class="mt-2 mb-2">
          <b-form-row style="justify-content: center;">
            <h4>Single Event</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label stlye="font-weight: bold;">Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>User Name</label><br>
              <b-form-input v-model="this.user_name"
                            disabled/>
            </b-col>
            <b-col cols="6">
              <label>Contact Information (optional)</label>
              <b-form-input v-model="this.user_contact_info"/>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Date:</label>
                <font-awesome-icon v-if="this.blackout_date !== null"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="blackout_date"
                            id="appointment_blackout_date"
                            type="date"
                            lang="en"
                            class="w-100"
                            @change="checkSingleInput"
                            @input="checkSingleInput"
                            @clear="checkSingleInput">
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Start Time:</label>
                <font-awesome-icon v-if="this.start_time !== null"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="start_time"
                            id="appointment_blackout_start_time"
                            :time-picker-options="{ start: '8:00', step: '00:30', end: '16:30' }"
                            lang="en"
                            format="h:mm a"
                            autocomplete="off"
                            placeholder="Select Start Time"
                            class="w-100"
                            type="time"
                            @change="checkSingleInput"
                            @input="checkSingleInput"
                            @clear="checkSingleInput">
                </DatePicker>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout End Time:</label>
                <font-awesome-icon v-if="this.end_time !== null"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="end_time"
                            id="appointment_blackout_end_time"
                            :time-picker-options="{ start: '8:30', step: '00:30', end: '17:00' }"
                            lang="en"
                            format="h:mm a"
                            autocomplete="off"
                            placeholder="Select End Time"
                            class="w-100"
                            type="time"
                            @change="checkSingleInput"
                            @input="checkSingleInput"
                            @clear="checkSingleInput">
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-recurring-events">
        <b-card class="mt-2">
          <b-form-row style="justify-content: center;">
            <h4>Recurring Event</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label style="font-weight: bold;">Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>User Name:</label><br>
              <b-form-input v-model="this.user_name"
                            disabled/>
            </b-col>
            <b-col cols="6">
              <label>Contact Information (optional):</label>
              <b-form-input v-model="this.user_contact_info"/>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Start Time:</label>
                <font-awesome-icon v-if="this.recurring_start_time !== null"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="recurring_start_time"
                            id="recurring_blackout_start_time"
                            :time-picker-options="{ start: '8:00', step: '00:30', end: '16:30' }"
                            lang="en"
                            format="h:mm a"
                            autocomplete="off"
                            placeholder="Select Start Time"
                            class="w-100"
                            type="time"
                            @change="checkRecurringInput"
                            @input="checkRecurringInput"
                            @clear="checkRecurringInput">
                </DatePicker>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout End Time:</label>
                <font-awesome-icon v-if="this.recurring_end_time !== null"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="recurring_end_time"
                            id="recurring_blackout_end_time"
                            :time-picker-options="{ start: '8:30', step: '00:30', end: '17:00' }"
                            lang="en"
                            format="h:mm a"
                            autocomplete="off"
                            placeholder="Select End Time"
                            class="w-100"
                            type="time"
                            @change="checkRecurringInput"
                            @input="checkRecurringInput"
                            @clear="checkRecurringInput">
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Start Date:</label>
                <font-awesome-icon v-if="this.recurring_start_date !== null"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker id="recurring_start_date"
                            class="w-100"
                            lang="en"
                            v-model="recurring_start_date"
                            placeholder="Select Start Date"
                            @change="checkRecurringInput"
                            @input="checkRecurringInput"
                            @clear="checkRecurringInput">
                </DatePicker>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout End Date:</label>
                <font-awesome-icon v-if="this.recurring_end_date !== null"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker id="recurring_end_date"
                            class="w-100"
                            lang="en"
                            v-model="recurring_end_date"
                            placeholder="Select End Date"
                            @change="checkRecurringInput"
                            @input="checkRecurringInput"
                            @clear="checkRecurringInput">
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-form-group class="mt-0 ml-1">
              <label>Frequency:</label>
              <font-awesome-icon v-if="this.selected_frequency.length === 1"
                                 icon='check'
                                 style="fontSize: 1rem; color: green;"/>
              <font-awesome-icon v-if="this.selected_frequency.length > 1"
                                 icon='exclamation-triangle'
                                 style="fontSize: 1rem; color: #FFC32B;"/>
              <b-form-checkbox-group id="frequency-checkboxes"
                                     v-model="selected_frequency"
                                     @input="checkRecurringInput">
                <b-form-checkbox :value="yearly">Yearly</b-form-checkbox>
                <b-form-checkbox :value="monthly">Monthly</b-form-checkbox>
                <b-form-checkbox :value="weekly">Weekly</b-form-checkbox>
                <b-form-checkbox :value="daily">Daily</b-form-checkbox>
              </b-form-checkbox-group>
            </b-form-group>
          </b-form-row>
          <b-form-group>
            <label>Select Weekdays:</label>
            <font-awesome-icon v-if="this.selected_weekdays.length >= 1"
                               icon='check'
                               style="fontSize: 1rem; color: green;"/>
            <b-form-checkbox-group id="weekday-checkboxes"
                                   v-model="selected_weekdays"
                                   @input="checkRecurringInput">
              <b-form-checkbox :value="monday">Mon.</b-form-checkbox>
              <b-form-checkbox :value="tuesday">Tues.</b-form-checkbox>
              <b-form-checkbox :value="wednesday">Wed.</b-form-checkbox>
              <b-form-checkbox :value="thursday">Thurs.</b-form-checkbox>
              <b-form-checkbox :value="friday">Fri.</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
          <b-form-group>
            <b-form-row>
              <label style="font-weight: bold" class="mt-0">Number of Occurences(optional): </label>
              <span v-if="this.selected_count !== ''">&nbsp; Limited to {{ this.selected_count }} occurences.</span>
              <font-awesome-icon v-if="this.selected_count !== ''"
                                 icon='check'
                                 style="fontSize: 1rem; color: green;"
                                 class="ml-1"/>
            </b-form-row>
            <b-form-row>
              <b-col cols="6">
              <b-form-input type="number"
                            class="mb-1 w-100"
                            v-model="selected_count"/>
              </b-col>
            </b-form-row>
          </b-form-group>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-information-audit">
        <b-card class="mb-2">
          <b-form-group>
            <b-form-row style="justify-content: center;">
              <h4>Recurring Event</h4>
            </b-form-row>
            <b-form-row class="mb-2">
              <label stlye="font-weight: bold;">Step 2 (continued): Confirm Recurring Event Dates</label>
            </b-form-row>
            <b-form-row>
              <b-col cols="12">
                <b-button variant="primary"
                          class="w-100 mb-2"
                          v-b-toggle.recurring-rule-collapse>
                  View Recurring Event Info
                </b-button>
              </b-col>
            </b-form-row>
            <b-form-row class="mb-0">
              <b-collapse id="recurring-rule-collapse"
                          class="mb-2 ml-2"
                          visible>
                {{ this.rrule_text }}
              </b-collapse>
            </b-form-row>
            <b-form-row>
              <b-col cols="12">
                <b-button variant="primary"
                          class="w-100 mb-2"
                          v-b-toggle.recurring-dates-collapse>
                  View Recurring Dates ({{ this.rrule_array.length }})
                </b-button>
              </b-col>
            </b-form-row>
            <b-form-row>
              <b-collapse id="recurring-dates-collapse"
                          class="mb-2">
                <div style="height: 75px; overflow-y: scroll; margin: 0px;">
                  <ul class="list-group"
                      v-for="date in this.rrule_array"
                      style="justify-content: center;">
                    <li class="list-group-item">
                      <b>Event:</b> {{ formatStartDate(date.start) }} until {{ formatEndDate(date.end) }}
                    </li>
                  </ul>
                </div>
              </b-collapse>
            </b-form-row>
          </b-form-group>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-blackout-notes">
        <b-card class="mt=2">
          <b-form-row style="justify-content: center;">
            <h4 v-if="this.single_input_boolean">Single Event</h4>
            <h4 v-if="this.recurring_input_boolean">Recurring Event</h4>
          </b-form-row>
          <b-form-row>
            <label v-if="this.recurring_input_boolean"
                   stlye="font-weight: bold;">
              Step 3 (optional): Event Notes
            </label>
            <label v-if="this.single_input_boolean"
                   stlye="font-weight: bold;">
              Step 2 (optional): Event Notes
            </label>
            <font-awesome-icon v-if="this.notes !== ''"
                               icon='check'
                               style="fontSize: 1rem; color: green;"/>
          </b-form-row>
          <b-form-row>
            <b-textarea v-model="notes"
                        id="single_appointment_blackout_notes"
                        placeholder="Enter notes about blackout period"
                        rows="3"
                        max-rows="6"
                        size="md">
            </b-textarea>
          </b-form-row>
        </b-card>
      </b-collapse>
    </b-form>
  </b-modal>
</template>

<script>
    import { createNamespacedHelpers } from 'vuex'
    import moment from 'moment'
    import DatePicker from 'vue2-datepicker'
    import { RRule } from 'rrule'
    const { mapMutations, mapState, mapActions, mapGetters } = createNamespacedHelpers( 'appointmentsModule' )

    export default {
        name: "AppointmentBlackoutModal",
        components: { DatePicker },
        created(){
          this.user_name = "BLACKOUT PERIOD"
          this.user_contact_info = this.$store.state.user.username
        },
        mounted(){
        },
        data() {
          return {
            blackout_date: null,
            start_time: null,
            end_time: null,
            notes: '',
            user_name: '',
            user_contact_info: '',
            selected_frequency: [],
            selected_weekdays: [],
            selected_count: '',
            recurring_start_time: null,
            recurring_end_time: null,
            recurring_start_date: null,
            recurring_end_date: null,
            recurring_array: '',
            yearly: RRule.YEARLY,
            monthly: RRule.MONTHLY,
            weekly: RRule.WEEKLY,
            daily: RRule.DAILY,
            monday: RRule.MO,
            tuesday: RRule.TU,
            wednesday: RRule.WE,
            thursday: RRule.TH,
            friday: RRule.FR,
            single_blackout_boolean: true,
            recurring_blackout_boolean: true,
            rrule_array: [],
            rrule_text: '',
            recurring_input_boolean: false,
            single_input_boolean: false,
            next_boolean: false,
            single_input_state: '',
            recurring_input_state: ''
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
          show(){
            this.showCollapse('collapse-event-selection')
            this.hideCollapse('collapse-single-event')
            this.hideCollapse('collapse-information-audit')
            this.hideCollapse('collapse-blackout-notes')
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
          },
          cancel(){
            this.recurring_blackout_boolean = true
            this.single_blackout_boolean = true
            this.single_input_boolean = false
            this.recurring_input_boolean =false
            this.rrule_text = ''
            this.rrule_array = []
            this.toggleAppointmentBlackoutModal(false)
          },
          submit(){
            let date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
            let start = moment(this.start_time).clone().format('HH:mm:ss')
            let start_date = moment(date + " " + start).format('YYYY-MM-DD HH:mm:ssZ')
            let end = moment(this.end_time).clone().format('HH:mm:ss')
            let end_date = moment(date + " " + end).format('YYYY-MM-DD HH:mm:ssZ')
            const uuidv4 = require('uuid/v4')
            let recurring_uuid = uuidv4()
            if(this.rrule_array.length > 0){
              this.rrule_array.forEach(item => {
                let e = {
                  start_time: item.start,
                  end_time: item.end,
                  citizen_name: this.user_name,
                  contact_information: this.user_contact_info,
                  blackout_flag: 'Y',
                  recurring_uuid: recurring_uuid
                }
                if(this.notes){
                  e.comments = this.notes
                }
                this.postAppointment(e)
                this.getAppointments()
              })
            }else if(this.rrule_array.length === 0) {
              let e = {
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
              this.getAppointments()
            }

            this.recurring_blackout_boolean = true
            this.single_blackout_boolean = true
            this.getAppointments()
            this.toggleAppointmentBlackoutModal(false)
            this.rrule_text = ''
            this.rrule_array = []
            this.recurring_input_state = ''
            this.single_input_boolean = ''
          },
          formatStartDate(date){
            let formatted_start_date = moment(date).format('YYYY-MM-DD HH:mm')
            return formatted_start_date
          },
          formatEndDate(date){
            let formatted_end_date = moment(date).format('HH:mm')
            return formatted_end_date
          },
          generateRule(){

            this.hideCollapse('collapse-event-selection')
            this.hideCollapse('collapse-recurring-events')
            this.recurring_blackout_boolean = true
            this.single_blackout_boolean = true
            this.next_boolean = false
            let start_year = parseInt(moment(this.recurring_start_date).utc().clone().format('YYYY'))
            let start_month = parseInt(moment(this.recurring_start_date).utc().clone().format('MM'))
            let start_day = parseInt(moment(this.recurring_start_date).utc().clone().format('DD'))
            let start_hour = parseInt(moment(this.recurring_start_time).utc().clone().format('HH'))
            let local_start_hour = parseInt(moment(this.recurring_start_time).clone().format('HH'))
            let start_minute = parseInt(moment(this.recurring_start_time).utc().clone().format('mm'))
            let end_year = parseInt(moment(this.recurring_end_date).utc().clone().format('YYYY'))
            let end_month = parseInt(moment(this.recurring_end_date).utc().clone().format('MM'))
            let end_day = parseInt(moment(this.recurring_end_date).utc().clone().format('DD'))
            let end_hour = parseInt(moment(this.recurring_end_time).utc().clone().format('HH'))
            let end_minute = parseInt(moment(this.recurring_end_time).utc().clone().format('mm'))
            let duration = moment.duration(moment(this.recurring_end_time).diff(moment(this.recurring_start_time)))
            let duration_minutes = duration.asMinutes()
            let input_frequency = null
            let local_dates_array = []

            switch(this.selected_frequency[0]){
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

            if(isNaN(start_year) == false || isNaN(end_year) == false) {
              // TODO Might be Deprecated -- IF RRule Breaks, this is where it will happen
              // TODO remove tzid from rule object
              let date_start = new Date(Date.UTC(start_year, start_month - 1, start_day, start_hour, start_minute))
              let until = new Date(Date.UTC(end_year, end_month - 1, end_day, end_hour, end_minute))
              const rule = new RRule({
                freq: input_frequency,
                count: this.selected_count,
                byweekday: this.selected_weekdays,
                dtstart: date_start,
                until: until,
                tzid: Intl.DateTimeFormat().resolvedOptions().timeZone,
              })
              let array = rule.all()
              this.rrule_text = rule.toText()

              array.forEach(date => {
                let formatted_start_date = moment(date).clone().set({hour: local_start_hour}).format('YYYY-MM-DD HH:mm:ssZ')
                let formatted_end_date = moment(date).clone().set({hour: local_start_hour}).add(duration_minutes, 'minutes').format('YYYY-MM-DD HH:mm:ssZ')
                local_dates_array.push({start: formatted_start_date, end: formatted_end_date})
              })
            }
            this.rrule_array = local_dates_array
            this.selected_count = ''
            this.selected_weekdays = []
            this.selected_frequency = []
            this.recurring_start_date = ''
            this.recurring_start_time = ''
            this.recurring_end_date = ''
            this.recurring_end_time = ''
            this.recurring_input_boolean = true
            this.recurring_input_state = 'audit_information'
            this.hideCollapse('collapse-blackout-notes')
            this.showCollapse('collapse-information-audit')
          },
          setSingle(){
            this.single_blackout_boolean = !this.single_blackout_boolean
            this.single_input_boolean = false
            this.recurring_input_boolean = false
            this.blackout_date = null
            this.start_time = null
            this.end_time = null
            this.recurring_input_state = ''
            this.single_input_state = ''
            this.hideCollapse('collapse-single-event')
          },
          setRecurring(){
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
            this.hideCollapse('collapse-recurring-events')
          },
          checkRecurringInput(){
            if(this.selected_frequency.length > 0
              && this.recurring_start_date !== null && this.recurring_start_time !== null && this.recurring_end_date !== null
              && this.recurring_end_time !== null){
              this.recurring_input_boolean = true
              this.next_boolean = true
              this.recurring_input_state = 'event_information'
            }else {
              this.recurring_input_boolean = false
            }
          },
          checkSingleInput(){
            if(this.blackout_date !== '' && this.start_time !== '' && this.end_time){
              this.single_input_boolean = true
              this.single_input_state = 'event_information'
            }else {
              this.single_input_boolean = false
              this.single_input_state = ''
            }

          },
          nextSingleNotes(){
            this.hideCollapse('collapse-event-selection')
            this.hideCollapse('collapse-single-event')
            this.showCollapse('collapse-blackout-notes')
            this.single_input_state = 'notes'
          },
          nextRecurringNotes(){
            this.hideCollapse('collapse-information-audit')
            this.showCollapse('collapse-blackout-notes')
            this.recurring_input_boolean = true
            this.recurring_input_state = 'notes'
          },
        },
        computed: {
          ...mapState({
            showAppointmentBlackoutModal: state => state.showAppointmentBlackoutModal,
          }),
          ...mapGetters([
            'is_recurring_enabled',
          ]),
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
  .list-group{
    max-height: 75px;
    min-height: 50px;
    overflow-y: scroll;
  }
</style>
