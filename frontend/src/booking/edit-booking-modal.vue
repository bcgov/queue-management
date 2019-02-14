<template>
  <b-modal v-model="modalVisible"
           :no-close-on-backdrop="true"
           :no-close-on-esc="true"
           :no-enforce-focus="true"
           :lazy="true"
           :centered="confirm && !minimized"
           @shown="show"
           @cancel="cancel"
           @ok="submit"
           :hide-footer="confirm"
           hide-header
           :size="confirm && !minimized ? 'sm' : 'md'">
    <div v-if="showModal" style="margin: 10px">
      <div v-if="minimized || !confirm" style="display: flex; justify-content: space-between">
        <div><h5>Edit Booking</h5></div>
        <div>
          <button class="btn btn-link"
                  @click="minimize">{{ minimized ? "Maximize" : "Minimize" }}</button>
        </div>
      </div>
      <template v-if="!confirm">
        <b-form>
          <b-form-row v-if="examAssociated">
            <b-col class="mb-2">
              <div class="q-info-display-grid-container">
                <div class="q-id-grid-outer">
                  <div class="q-id-grid-top-head">Exam Details</div>
                  <div>Writer:</div>
                  <div class="q-id-grid-1st-col">{{ this.event.exam.examinee_name }}</div>
                  <div class="q-id-grid-2nd-head">Exam:</div>
                  <div class="q-id-grid-2nd-col">{{ this.event.exam.exam_name }}</div>
                  <div>Method:</div>
                  <div class="q-id-grid-1st-col">{{ this.event.exam.exam_method }}</div>
                  <div class="q-id-grid-2nd-head">Event ID:</div>
                  <div class="q-id-grid-2nd-col">{{ this.event.exam.event_id }}</div>
                  <div>Duration:</div>
                  <div class="q-id-grid-1st-col">{{ this.event.exam.exam_type.number_of_hours }} hrs</div>
                  <div class="q-id-grid-2nd-head">Expiry:</div>
                  <div class="q-id-grid-2nd-col">{{ expiryDate }}</div>
                </div>
              </div>
            </b-col>
          </b-form-row>
          <b-form-row v-if="!examAssociated">
            <b-col>
              <b-form-group>
                <label :style="{color: labelColor}">Event Title</label><br>
                <b-input :state="state"
                         id="title"
                         type="text"
                         @input.native="checkValue"
                         v-model="title" />
              </b-form-group>
            </b-col>
            <b-col cols="3">
              <b-form-group>
                <label>Collect Fees</label><br>
                <b-select v-model="fees"
                          @input.native="checkValue"
                          :options="feesOptions" />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row v-if="fees">
            <b-col cols="4">
              <b-form-group>
                <label>Fee Option</label>
                <b-select :options="roomRates" v-model="rate" />
              </b-form-group>
            </b-col>
            <b-col cols="8">
              <b-form-group>
                <label>Invoice To</label>
                <b-select :options="invoiceOptions" v-model="invoice"/>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row v-if="invoice==='custom'">
            <b-col cols="12">
              <b-form-group>
                <label>Enter Name of Entity to Invoice</label><br>
                <b-input />
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
                <b-select :options="invigilatorDropdown"
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
            <b-col>
              <b-form-group>
                <label>Delete Booking?</label><br>
                <b-btn class="w-100 btn-danger"
                       @click="confirm = true">Delete</b-btn>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group>
                <label>Change Date, Time or Room?</label><br>
                <b-btn class="w-100 mb-0" @click="reschedule">Reschedule</b-btn>
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
  import { mapActions, mapMutations, mapState } from 'vuex'
  import moment from 'moment'

  export default {
    name: "EditBooking",
    data() {
      return {
        minimized: false,
        confirm: false,
        added: 0,
        invigilator: null,
        editedFields: [],
        fees: false,
        feesOptions: [
          {text: 'No', value: false},
        ],
        invoice: null,
        invoiceOptions: [
          {text: 'Custom', value: 'custom'}
        ],
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
      }
    },
    mounted() {
      this.getInvigilators()
    },
    computed: {
      ...mapState(
        {
          event: state => state.editedBooking,
          actualEvent: state => state.editedBookingOriginal,
          newEvent: state => state.clickedDate,
          showModal: state => state.showEditBookingModal,
          invigilators: state => state.invigilators
        }
      ),
      displayDates() {
        if (this.start && this.end) {
          return {
            end: this.end.format('h:mm a'),
            start: this.start.format('h:mm a'),
            date: this.start.format('MMM Do, YYYY')
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
          return new moment(this.event.exam.expiry_date).format('MMM Do, YYYY')
        }
      },
      invigilatorDropdown() {
        return this.invigilators.map( i =>
          ({value: i.invigilator_id,
            text: i.invigilator_name})
        )
      },
      modalVisible: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleEditBookingModal(e)
        }
      },
      receivedDate() {
        if (this.examAssociated && this.event.exam) {
          return new moment(this.event.exam.received_date).format('MMM Do, YYYY')
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
        'deleteBooking',
        'finishBooking',
        'getInvigilators',
        'postBooking',
        'putBooking',
      ]),
      ...mapMutations([
        'navigationVisible',
        'setClickedDate',
        'setEditedBooking',
        'setSelectedExam',
        'toggleCalendarControls',
        'toggleEditBookingModal',
        'toggleFeedbackModalFromEditModal',
        'toggleScheduling',
        'toggleRescheduling',
        'toggleSchedulingIndicator',
        'toggleSchedulingOther',
      ]),
      cancel() {
        if (this.$route.params.date) {
          this.$router.push('/booking/')
        }
        this.$root.$emit('initialize')
        this.finishBooking()
        this.resetModal()
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
        this.toggleRescheduling(true)
        this.$root.$emit('toggleOffsite', false)
        this.message = ''
        this.$root.$emit('options', {name: 'selectable', value: true})
        this.toggleCalendarControls(false)
        this.toggleSchedulingIndicator(true)
        if (this.examAssociated) {
          this.toggleScheduling(true)
          this.setSelectedExam(this.event.exam)
        } else {
          this.toggleSchedulingOther(true)
        }
        this.toggleEditBookingModal(false)
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
        this.invigilator = null
      },
      setInvigilator(e) {
        this.message = ''
        if (this.event.invigilator.invigilator_id !== e) {
          if (!this.editedFields.includes('invigilator')) {
            this.editedFields.push('invigilator')
          }
        }
        if (this.event.invigilator.invigilator_id == e) {
          if (this.editedFields.includes('invigilator')) {
            this.editedFields.splice(this.editedFields.indexOf('invigilator'), 1)
          }
        }
        this.invigilator = e
      },
      show() {
        this.toggleRescheduling(false)
        if (this.newEvent && this.newEvent.start) {
          this.newStart = new moment(this.newEvent.start)
          this.newEnd = new moment(this.newEvent.end)
        }
        if (this.event.invigilator) {
          if (!this.editedFields.includes('invigilator')) {
            this.invigilator = this.event.invigilator.invigilator_id
          }
        }
        if (!this.editedFields.includes('title')) {
          this.title = this.event.title
        }
        if (!this.editedFields.includes('fee')) {
          this.fee = this.event.fee
        }
      },
      submit(e) {
        e.preventDefault()
        this.$root.$emit('toggleOffsite', true)
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
              this.message = 'Selected date/time is '
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
        if (this.editedFields.includes('fee')) {
          changes['fees'] = this.fee
        }
        if (this.editedFields.includes('invigilator')) {
          changes['invigilator_id'] = this.invigilator
        }
        if (Object.keys(changes).length === 0) {
          this.message = 'No Changes Made'
        } else {
          let payload = {
            id: this.event.id,
            changes
          }
          this.putBooking(payload).then(() => {
            this.$root.$emit('options', { name: 'selectable', value: false })
            this.finishBooking()
            this.resetModal()
          })
        }
      },
    }
  }
</script>
