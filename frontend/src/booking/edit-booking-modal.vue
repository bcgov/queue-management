<template>
  <b-modal v-model="modalVisible"
           :no-close-on-backdrop="true"
           :no-enforce-focus="true"
           :lazy="true"
           :centered="confirm && !minimized"
           @shown="show"
           @cancel="cancel"
           @ok="submit"
           :hide-footer="confirm"
           hide-header
           :size="confirm && !minimized ? 'sm' : 'md'">
    <div v-if="event && showModal" style="margin: 10px">
      <div v-if="minimized || !confirm" style="display: flex; justify-content: space-between">
        <div><h5>Edit Booking</h5></div>
        <div>
          <button class="btn btn-link"
                  @click="minimize">{{ minimized ? "Maximize" : "Minimize" }}</button>
        </div>
      </div>
      <template v-if="!confirm">
        <b-form autocomplete="off">
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
                    <div>{{ this.event.exam.exam_type.number_of_hours }} hrs {{ this.event.exam.exam_type.number_of_minutes }} min</div>
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
                <label :style="{color: labelColor}">Scheduling Party</label><br>
                <b-input :state="state"
                         id="title"
                         type="text"
                         @input.native="checkValue"
                         v-model="title" />
              </b-form-group>
            </b-col>
            <b-col cols="4">
              <b-form-group>
                <label>Collect Fees</label><br>
                <b-select id="fees"
                          v-model="fees"
                          @change.native="checkValue"
                          :options="feesOptions" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group>
                <label>Contact Information (Email or Phone Number)</label><br>
                <b-input autocomplete="off"
                         id="contact_information"
                         type="text"
                         @change.native="checkValue"
                         v-model="booking_contact_information"/>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group v-if="checkBookingBlackout">
                <label>Blackout Notes</label><br>
                <b-form-textarea id="blackout_notes"
                                 v-model="blackout_notes"
                                 class="mb-2"
                                 @change.native="checkValue">
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
          <b-form-row>
            <b-col class="w-100">
              <b-form-group>
                <label>Start Time</label><br>
                <b-input type="text"
                         readonly
                         :value="displayDates.start" />
              </b-form-group>
            </b-col>
            <b-col class="w-100">
              <b-form-group>
                <label>End Time</label><br>
                <b-input type="text"
                         readonly
                         :value="displayDates.end" />
              </b-form-group>
            </b-col>
            <b-col cols="5" v-if="examAssociated">
              <b-form-group>
                <label>Invigilator</label><br>
                <b-select v-model="invigilator"
                          :options="invigilator_dropdown"
                          id="invigilator"
                          :value="invigilator"
                          @change="setInvigilator"/>
              </b-form-group>
            </b-col>
            <b-col cols="5" v-if="!examAssociated">
              <b-form-group>
                <label>Duration</label><br>
                <b-button-group>
                  <b-button @click="decrement" >
                    <font-awesome-icon icon="minus"
                                       class="m-0 p-0"
                                       style="font-size: .8rem; color: white"/>
                  </b-button>
                  <b-input :value="displayDuration"
                           readonly
                           id="duration"
                           @change.native="checkValue"
                           style="border-radius: 0px" />
                  <b-button @click="increment" >
                    <font-awesome-icon icon="plus"
                                       class="m-0 p-0"
                                       style="font-size: .8rem; color: white"/>
                  </b-button>
                </b-button-group>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <template v-if="this.currentShadowInvigilator != null">
              <b-row style="display: flex;" class="w-100 ml-0 mb-2">
                <b-col class="w-50 ml-1 mr-1 pr-1">
                  <b-button v-if="this.changeState"
                            v-b-toggle.collapse-1
                            variant="primary"
                            @click="setRemove">
                    Change Shadow Invigilator
                  </b-button>
                  <b-button v-else-if="!this.changeState"
                            disabled
                            variant="primary">
                    Change Shadow Invigilator
                  </b-button>
                </b-col>
                <b-col class="w-50 ml-1 mr-1 pl-1">
                  <b-button v-if="this.removeState"
                            v-b-toggle.collapse-2
                            variant="danger"
                            @click="setChange">
                    Remove Shadow Invigilator
                  </b-button>
                  <b-button v-else-if="!this.removeState"
                            disabled
                            variant="danger">
                    Remove Shadow Invigilator
                  </b-button>
                </b-col>
              </b-row>
            </template>
            <template v-else>
              <b-button v-if="examAssociated"
                        v-b-toggle.collapse-1
                        variant="primary"
                        class="w-100 m-1">
                Add Shadow Invigilator
              </b-button>
            </template>
            <b-collapse id="collapse-1"
                        class="mt-2 w-100">
              <b-form-group class="q-info-display-grid-container">
                <label>Shadow Invigilators</label>
                <b-form>
                  <b-row>
                    <b-col cols="7">
                      <b-table selectable
                               select-mode="single"
                               :fields="shadowFields"
                               :items="shadow_invigilator_options"
                               @row-selected="rowSelectedShadow"
                               responsive
                               selected-variant="success"
                               style="height: 75px; width: 250px;"
                               bordered
                               striped>
                        <template slot="selected" slot-scope=" { rowSelected } ">
                          <span v-if="rowSelected">✔</span>
                        </template>
                      </b-table>
                    </b-col>
                    <b-col cols="4">
                      <b-row>
                        Shadow Invigilator Limit: 1
                      </b-row>
                      <b-row v-if="this.currentShadowInvigilator != null"
                             class="mb-1">
                        Current Invigilator
                      </b-row>
                      <b-row v-if="this.currentShadowInvigilator != null"
                             style="justify-content: center;"
                             class="mb-1">
                        {{ this.currentShadowInvigilatorName }}
                      </b-row>
                      <b-row style="font-weight: bold;"
                             class="mb-1">
                        Selected Invigilators
                      </b-row>
                      <b-row v-for="select in selectedShadow"
                             style="justify-content: center;"
                             class="mb-1">
                        {{ select.name }}
                      </b-row>
                    </b-col>
                  </b-row>
                </b-form>
              </b-form-group>
            </b-collapse>
            <b-collapse id="collapse-2"
                        class="mt-2 w-100">
              <b-form-group class="q-info-display-grid-container">
                <b-row class="ml-1">
                  <span style="font-weight: bold;">Current Shadow Invigilator: </span>
                </b-row>
                <b-row class="mb-2"
                       style="justify-content: center;">
                  <span>{{ this.currentShadowInvigilatorName}}</span>
                </b-row>
                <b-row class="ml-1">
                  <span style="font-weight: bold;">Would you like to remove this shadow invigilator?</span>
                </b-row>
                <template>
                  <b-row style="display: flex; justify-content: center;"
                         class="w-100 mb-0">
                    <b-button class="mr-2 mt-1"
                              variant="danger"
                              @click="setSelectedShadowNull">
                      Yes
                    </b-button>
                    <b-button class="ml-2 mt-1"
                              variant="primary"
                              v-b-toggle.collapse-2
                              @click="setChange">
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
                <label>Delete Booking?</label><br>
                <b-btn class="w-100 btn-danger"
                       @click="confirm = true">Delete Booking</b-btn>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group>
                <label>Change Date, Time or Room?</label><br>
                <b-btn class="w-100 mb-0"
                       @click="reschedule">
                  Reschedule Booking
                </b-btn>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row v-if="message">
            <b-col>
              <div style="display: flex; justify-content: flex-end; width: 100%;">
                <span style="color: red; font-weight: 600; font-size: .9rem;">{{ message }}</span>
              </div>
            </b-col>
          </b-form-row>
        </b-form>
      </template>
      <template v-if="confirm">
        <template v-if="!minimized">
          Are you sure you want to delete this booking?<br>
          <div style="display:flex; justify-content: center">
            <b-button class="mr-2 btn-primary"
                      @click="confirm = false">No</b-button>
            <b-button class="ml-2 btn-danger"
                      @click="clickYes">Yes</b-button>
          </div>
        </template>
      </template>
    </div>
  </b-modal>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import moment from 'moment'

  export default {
    name: "EditBooking",
    props: ['tempEvent'],
    data() {
      return {
        minimized: false,
        confirm: false,
        added: 0,
        invigilator: null,
        shadowInvigilator: null,
        currentShadowInvigilator: null,
        currentShadowInvigilatorName: '',
        editedFields: [],
        fees: '',
        feesOptions: [
          {text: 'No', value: "false"},
          {text: 'Yes', value: "true"},
          {text: 'HQ to Invoice', value: "HQFin"}
        ],
        invoice: null,
        invoiceOptions: [ {text: 'Custom', value: 'custom'} ],
        labelColor: 'black',
        message: '',
        newEnd: null,
        newStart: null,
        rate: null,
        roomRates: [
          {value: 125, text: '$125 for 1/2 Day'},
          {value: 250, text: '$250 for Whole Day'}
        ],
        state: null,
        title: '',
        booking_contact_information: '',
        rescheduling: false,
        blackout_notes: '',
        selectedShadow: [],
        shadowFields: ['selected', 'name'],
        changeState: true,
        removeState: true,
        removeFlag: false,
        rescheduleInvigilator: null,
        rescheduleShadowInvigilator: null,
        cancel_flag: false,
      }
    },
    computed: {
      ...mapGetters([
        'invigilator_dropdown',
        'shadow_invigilators',
        'shadow_invigilator_options',
      ]),
      ...mapState(
        {
          event: state => state.editedBooking,
          actualEvent: state => state.editedBookingOriginal,
          newEvent: state => state.clickedDate,
          showModal: state => state.showEditBookingModal,
          invigilators: state => state.invigilators,
          selectedExam: state => state.selectedExam,
          shadowInvigilators: state => state.shadowInvigilators,
        }
      ),
      checkBookingBlackout(){
        if(this.event.blackout_flag === 'Y'){
          return true
        }
        return false
      },
      displayDates() {
        if (this.event.start && this.event.end) {
          return {
            end: this.event.end.format('h:mm a'),
            start: this.event.start.format('h:mm a'),
            date: this.event.start.format('ddd MMM D, YYYY')
          }
        }
        return {end: '', start: '', date: ''}
      },
      displayDuration() {
        if (this.duration) {
          let output = this.duration.toFixed(1)
          return `${output} hrs`
        }
      },
      duration() {
        if (this.start && this.end) {
          return this.end.diff(this.start, 'hours', true)
        }
        return ''
      },
      end() {
        if (this.examAssociated && this.newEvent) {
          return new moment(this.newEvent.end)
        }
        if (this.examAssociated && !this.newEvent) {
          return new moment(this.event.end)
        }
        if (!this.newEnd && this.event && this.event.end) {
          return new moment(this.event.end).add(this.added, 'hours')
        }
        if (this.newEnd) {
          return new moment(this.newEnd).add(this.added, 'hours')
        }
      },
      examAssociated() {
        if (this.event && this.event.exam) {
          return true
        }
        return false
      },
      expiryDate() {
        if (this.examAssociated && this.event.exam) {
          let d = new moment(this.event.exam.expiry_date)
          if (d.isValid()) {
            return d.format('MMM Do, YYYY')
          }
        }
        return 'not applicable'
      },
      modalVisible: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleEditBookingModal(e)
        }
      },
      resource() {
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
      },
      start() {
        if (this.examAssociated && this.newEvent) {
          return new moment(this.newEvent.start)
        }
        if (this.examAssociated && !this.newEvent) {
          return new moment(this.event.start)
        }
        if (!this.newStart && this.event && this.event.start) {
          return new moment(this.event.start)
        }
        if (this.newStart) {
          return this.newStart
        }
      },
    },
    methods: {
      ...mapActions([
        'getBookings',
        'deleteBooking',
        'finishBooking',
        'getInvigilators',
        'postBooking',
        'putBooking',
        'putInvigilatorShadow',
      ]),
      ...mapMutations([
        'setClickedDate',
        'setEditedBooking',
        'setSelectedExam',
        'toggleEditBookingModal',
        'toggleScheduling',
        'toggleRescheduling',
      ]),
      cancel() {
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
      },
      checkValue(e) {
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
            let i = this.editedFields.indexOf(e.target.id)
            this.editedFields.splice(i,1)
          }
        }
        if (this.message === 'No Changes Made') {
          if (this.editedFields.length > 0) {
            this.message = ''
          }
        }
      },
      clickYes(e) {
        e.preventDefault()
        let id = this.event.id
        this.deleteBooking(id).then(() => {
          this.finishBooking()
          this.resetModal()
        })
      },
      decrement() {
        if (this.duration == .5) {
          return
        }
        this.added -= .5
        let params = {
          end: this.end
        }
        if (this.tempEvent) {
          return
        }
        this.$root.$emit('updateEvent', this.actualEvent, params)
      },
      increment() {
        if (this.end.format('H') == 18) {
          return
        }
        this.added += .5
        let params = {
          end: this.end
        }
        if (this.tempEvent) {
          return
        }
        this.$root.$emit('updateEvent', this.actualEvent, params)
      },
      minimize() {
        if (this.minimized) {
          this.minimized = false
          this.confirm = false
        } else {
          this.minimized = true
          this.confirm =  true
        }
      },
      reschedule() {
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
      },
      resetModal() {
        this.added = null
        this.newStart = null
        this.newEnd = null
        this.editedFields = []
        this.fee = false
        this.labelColor = 'black'
        this.message = null
        this.state = null
        this.title = null
        this.confirm = false
      },
      setInvigilator(e) {
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
      },
      show() {
        this.changeState = true
        this.removeState = true
        if (this.newEvent && this.newEvent.start) {
          this.newStart = new moment(this.newEvent.start)
          this.newEnd = new moment(this.newEvent.end)
        }
        if (this.event.exam && this.event.exam.booking) {
          let currentID = this.currentShadowInvigilator = this.event.exam.booking.shadow_invigilator_id || null
          let currentName = ''
          this.shadow_invigilators.forEach(function(invigilator) {
            if(invigilator['id'] == currentID){
              currentName = invigilator['name']
            }
          })
          this.currentShadowInvigilatorName = currentName
          if (!this.editedFields.includes('invigilator')) {
            if(this.rescheduling){
              this.invigilator = null
            }
            if(this.event.exam.booking.invigilators.length == 1){
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
          this.title = this.event.title
        }
        if (!this.editedFields.includes('fees')) {
          this.fees = this.event.fees
        }
        if (!this.editedFields.includes('booking_contact_information')){
          this.booking_contact_information = this.event.booking_contact_information
        }
        if(!this.editedFields.includes('blackout_notes')){
          this.blackout_notes = this.event.blackout_notes
        }
        if(this.rescheduling){
          if(this.cancel_flag){
            this.invigilator = this.rescheduleInvigilator
            this.currentShadowInvigilator = this.rescheduleShadowInvigilator
            this.rescheduleInvigilator = null
            this.cancel_flag = false
          }else {
            this.invigilator = null
            this.currentShadowInvigilator = null
            this.currentShadowInvigilatorName = null
          }
        }
        this.rescheduling = false
        this.cancel_flag = false
        this.rescheduleInvigilator = null
      },
      rowSelectedShadow(shadows, e){
        this.message = ''
        this.selectedShadow = shadows
        if (this.event.exam && this.event.exam.booking) {
          if (this.event.exam.booking.shadow_invigilator_id !== e) {
            if (!this.editedFields.includes('shadow_invigilator')) {
              this.editedFields.push('shadow_invigilator')
            }
          }else if (this.event.exam.booking.shadow_invigilator_id == e) {
            if (this.editedFields.includes('shadow_invigilator')) {
              this.editedFields.splice(this.editedFields.indexOf('shadow_invigilator'), 1)
            }
          }
        }
        if(shadows[0] == null){
          this.shadowInvigilator = null
        }else{
          this.shadowInvigilator = shadows[0].id
        }
      },
      submit() {
        if (this.title.length === 0) {
          this.labelColor = 'red'
          this.state = 'danger'
          this.message = 'A title is required'
          return
        }
        let changes = {}
        if (!this.start.isSame(this.event.start)) {
          if (this.examAssociated) {
            if (this.start.isAfter(this.event.exam.expiry_date)) {
              this.message = `Selected date/time is after the exam's expiry date.  Press reschedule to pick a new time.`
              return
            }
          }
          if (moment().isAfter(this.start)) {
            this.message = 'Selected date/time is is in the past. Press Reschedule and pick a new time.'
            return
          }
          changes['start_time'] = this.start.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
        }
        if (!this.end.isSame(this.event.end)) {
          changes['end_time'] = this.end.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
        }
        if (this.newEvent && !(this.newEvent.resource.id == this.event.resourceId)) {
          changes['room_id'] = this.newEvent.resource.id
        }
        if (this.editedFields.includes('title')) {
          changes['booking_name'] = this.title
        }
        if (this.editedFields.includes('fees')) {
          changes['fees'] = this.fees
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
          if (this.rescheduling){
            changes.invigilator_id = null
            changes.sbc_staff_invigilated = 0
            this.rescheduling = false
          }
        }
        if (this.editedFields.includes('shadow_invigilator')){
          if(this.removeFlag){
            changes['shadow_invigilator_id'] = null
          } else {
            changes['shadow_invigilator_id'] = this.shadowInvigilator
          }
          if(this.rescheduleShadowInvigilator !== null){
            changes['shadow_invigilator_id'] = this.shadowInvigilator
          }
        }
        if (this.editedFields.includes('contact_information')){
          changes['booking_contact_information'] = this.booking_contact_information
        }
        if (this.editedFields.includes('invigilator_id')){
          changes['invigilator_id'] = this.invigilator
        }
        if(this.editedFields.includes('blackout_notes')){
          changes['blackout_notes'] = this.blackout_notes
        }
        if (Object.keys(changes).length === 0) {
          this.message = 'No Changes Made'
        } else {
          let invigilatorPayload = {
            id: null,
            params: null,
          }
          let changePayload = {
            id: null,
            params: null,
          }
          if (this.removeFlag) {
            invigilatorPayload.id = this.currentShadowInvigilator
            invigilatorPayload.params = '?add=False&subtract=True'
          } else if(this.rescheduleShadowInvigilator !== null) {
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
          if(invigilatorPayload.id ){
            this.putInvigilatorShadow(invigilatorPayload)
          }
          if(changePayload.id){
            this.putInvigilatorShadow(changePayload)
          }
          let payload = {
            id: this.event.id,
            changes
          }
          if(changes.invigilator_id === 'sbc'){
            delete changes.invigilator_id
          }
          this.putBooking(payload).then( () => {
            setTimeout( () => {
              this.$root.$emit('initialize')
              this.finishBooking()
              this.resetModal()
            }, 250)
          })
        }
        this.selectedShadow = []
        this.shadowInvigilator = null
        this.removeFlag = false
      },
      setChange(){
        this.changeState = !this.changeState
        return
      },
      setRemove(){
        this.removeState = !this.removeState
        return
      },
      setSelectedShadowNull(e){
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
      },
    }
  }
</script>

<style scoped>
  .table-responsive {
    line-height: 5px;
  }
</style>
