<template>
  <b-modal v-model="modalVisible"
           :no-close-on-backdrop="true"
           hide-header
           @shown="setValues"
           hide-footer
           size="md">
    <div v-if="showModal">
      <span class="q-modal-header">Edit Group Exam Booking</span>
      <b-form>
        <b-form-row>
          <b-col class="mb-2">
            <div class="q-info-display-grid-container">
              <div class="q-id-grid-outer">
                <div class="q-id-grid-head">Exam Details</div>
                <div class="q-id-grid-col">
                  <div>Exam: </div>
                  <div>{{ actionedExam.exam_name }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Event ID: </div>
                  <div>{{ actionedExam.event_id }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Type: </div>
                  <div>{{ actionedExam.exam_type.exam_type_name }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Writers: </div>
                  <div>{{ actionedExam.number_of_students }}</div>
                </div>
                <div class="q-id-grid-col" v-if="is_liaison_designate">
                  <div>Office: </div>
                  <div>{{ actionedExam.booking.office.office_name }}</div>
                </div>
              </div>
            </div>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col cols="6" v-if="is_liaison_designate || role_code === 'GA'">
            <b-form-group>
              <label>Exam Date</label><br>
              <DatePicker v-model="date"
                          name="date"
                          class="w-100"
                          @input="checkDate"
                          lang="en"></DatePicker>
            </b-form-group>
          </b-col>
          <b-col cols="6" v-if="role_code !== 'GA' && !is_liaison_designate">
            <b-form-group>
              <label>Exam Time</label><br>
              <b-input disabled :value="formatTime(actionedExam.booking.start_time)" />
            </b-form-group>
          </b-col>
          <b-col cols="6" v-if="role_code !== 'GA' && !is_liaison_designate">
            <b-form-group>
              <label>Exam Date</label><br>
              <b-input disabled :value="formatDate(actionedExam.booking.start_time)" />
            </b-form-group>
          </b-col>
          <b-col cols="6" v-if="is_liaison_designate || role_code === 'GA'">
            <b-form-group>
              <label>Exam Time</label><br>
              <DatePicker v-model="time"
                          class="w-100"
                          :time-picker-options="{ start: '8:00', step: '00:30', end: '17:00' }"
                          lang="en"
                          format="h:mm a"
                          confirm
                          name="time"
                          @input="checkTime"
                          type="time">
                <template slot="calendar-icon">
                  <font-awesome-icon icon="clock"
                                     class="m-0 p-0"
                                     style="font-size: .9rem;"/>
                </template>
              </DatePicker>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group>
              <label>Location</label><br>
              <b-textarea v-model="offsite_location"
                          :disabled="role_code !== 'GA' && !is_liaison_designate"
                          class="mb-0"
                          :rows="2"
                          name="offsite_location"
                          @input.native="checkInput" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row align-content="end" align-h="end">
          <b-col :cols="is_liaison_designate || role_code === 'GA' ? 10 : '' ">
            <b-form-group>
              <label>Invigilator</label><br>
              <b-select v-model="invigilator_id"
                        name="invigilator_id"
                        @change.native="checkInput"
                        :options="invigilator_dropdown" />
            </b-form-group>
          </b-col>
          <b-col cols="2" align-self="start" v-if="is_liaison_designate || role_code === 'GA'">
            <label>Clear Form?</label><br>
            <b-btn class="w-100 btn-warning" @click="setValues">Reset</b-btn>
          </b-col>
        </b-form-row>
      </b-form>
      <div v-if="showMessage"
            class="mb-3"
            style="color: red;">Nothing has changed.  All fields contain their initial values.</div>
      <div style="display: flex; justify-content: flex-end; width: 100%">
        <b-btn class="btn-secondary mr-2" @click="cancel">Cancel</b-btn>
        <b-btn v-if="editedFields.length === 0"
               class="btn-primary disabled"
               @click="showMessage=true">Submit</b-btn>
        <b-btn v-else-if="editedFields.length > 0"
               class="btn-primary"
               @click="submit">Submit</b-btn>
      </div>
    </div>
  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState, mapGetters } from 'vuex'
  import moment from 'moment'
  import zone from 'moment-timezone'
  import DatePicker from 'vue2-datepicker'

  export default {
    name: "EditGroupExamBookingModal",
    components: { DatePicker },
    props: ['actionedExam', 'resetExam'],
    data () {
      return {
        invigilator_id: '',
        date: '',
        time: '',
        offsite_location: '',
        editedFields: [],
        showMessage: false,
        itemCopy: {},
      }
    },
    computed: {
      ...mapGetters(['role_code', 'invigilator_dropdown', 'is_liaison_designate']),
      ...mapState({
        showModal: state => state.showEditGroupBookingModal,
        invigilators: 'invigilators',
        user: 'user',
      }),
      editedTimezone() {
        if (this.actionedExam && this.actionedExam.booking) {
          return this.actionedExam.booking.office.timezone.timezone_name
        }
        return ''
      },
      modalVisible: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleEditGroupBookingModal(e)
        }
      },
    },
    methods: {
      ...mapActions(['getBookings', 'getExams', 'putRequest']),
      ...mapMutations(['toggleEditGroupBookingModal']),
      cancel() {
        this.toggleEditGroupBookingModal(false)
        this.reset()
        this.resetExam()
      },
      formatDate(d) {
        return new moment(d).format('ddd, MMM DD, YYYY')
      },
      formatTime(d) {
        return new moment(d).format('h:mm a')
      },
      checkDate(e) {
        this.showMessage = false
        let date = new moment(this.itemCopy.booking.start_time).format('ddmmyyyy').toString()
        let newDate = new moment(e).format('ddmmyyyy').toString()
        if (newDate === date) {
          if (this.editedFields.includes('date')) {
            let i = this.editedFields.indexOf('date')
            this.editedFields.splice(i,1)
          }
        }
        if (newDate !== date) {
          if (!this.editedFields.includes('date')) {
            this.editedFields.push('date')
          }
        }
      },
      checkTime(e) {
        this.time = e
        this.showMessage = false
        let time = zone.tz(this.itemCopy.booking.start_time, this.editedTimezone).format('HH:mm').toString()
        let newTime = new moment(e).format('HH:mm').toString()
        if (newTime === time) {
          if (this.editedFields.includes('time')) {
            let i = this.editedFields.indexOf('time')
            this.editedFields.splice(i,1)
          }
        }
        if (newTime !== time) {
          if (!this.editedFields.includes('time')) {
            this.editedFields.push('time')
          }
        }
      },
      checkInput(e) {
        let { name } = e.target
        let { value } = e.target

        this.showMessage = false
        if (name === 'offsite_location') {
          if (value !== this.itemCopy[name]) {
            if (!this.editedFields.includes(e.target.name)) {
              this.editedFields.push(e.target.name)
            }
            this[e.target.name] = e.target.value
            return
          }
          if (value === this.itemCopy[name]) {
            if (this.editedFields.includes(e.target.name)) {
              let i = this.editedFields.indexOf(e.target.name)
              this.editedFields.splice(i, 1)
            }
            this[name] = value
            return
          }
        }
        if (name === 'invigiator_id' && value == '') {
          if (this.itemCopy.booking.invigiator_id) {
            if (!this.editedFields.includes(name)) {
              this.editedFields.push(name)
            }
          }
          if (!this.itemCopy.booking.invigiator_id) {
            if (this.editedFields.includes(e.target.name)) {
              let i = this.editedFields.indexOf(e.target.name)
              this.editedFields.splice(i, 1)
            }
          }
          this.invigiator_id = ''
          return
        }
        value = parseInt(value)
        if (value !== this.itemCopy.booking[name]) {
          if (!this.editedFields.includes(e.target.name)) {
            this.editedFields.push(e.target.name)
          }
          this[e.target.name] = e.target.value
          return
        }
        if (value == this.itemCopy.booking[name]) {
          if (this.editedFields.includes(e.target.name)) {
            let i = this.editedFields.indexOf(e.target.name)
            this.editedFields.splice(i, 1)
          }
          this[e.target.name] = e.target.value
          return
        }
      },
      submit() {
        let edits = this.editedFields
        let putRequests = []
        let local_timezone_name = this.user.office.timezone.timezone_name
        let edit_timezone_name = this.actionedExam.booking.office.timezone.timezone_name
        let bookingChanges = {}
        if (edits.includes('time') || edits.includes('date') || edits.includes('invigilator_id')) {
          let baseDate = this.date
          let baseTime = moment(this.time).format('HH:mm:ss').toString()
          if (edits.includes('date')) {
            baseDate = new moment(this.date).format('YYYY-MM-DD').toString()
          }
          let start
          if (local_timezone_name !== edit_timezone_name) {
            console.log('different time zones')
            start =  zone.tz(`${baseDate}T${baseTime}`, edit_timezone_name)
          }
          if (local_timezone_name === edit_timezone_name) {
            console.log('same time zones')
            start = moment(`${baseDate}T${baseTime}`)
          }
          let end = start.clone().add(parseInt(this.itemCopy.exam_type.number_of_hours), 'h')
          bookingChanges['start_time'] = start.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
          bookingChanges['end_time'] = end.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
          bookingChanges['invigilator_id'] = this.invigilator_id
          if (bookingChanges.invigilator_id == '') {
            bookingChanges.invigilator_id = null
          }
          putRequests.push({url:`/bookings/${this.itemCopy.booking.booking_id}/`, data: bookingChanges})
        }
        let examChanges = {}
        if (edits.includes('offsite_location')) {
          examChanges['offsite_location'] = this.offsite_location
          putRequests.push({url:`/exams/${this.itemCopy.exam_id}/`, data: examChanges})
        }
        let promises = []
        putRequests.forEach( put => {
          promises.push(this.putRequest(put))
        })
        Promise.all(promises).then( () => {
          this.getBookings().then( () => {
            this.getExams().then( () => {
              this.cancel()
            })
          })
        })
      },
      setValues() {
        let tempItem = Object.assign({}, this.actionedExam)
        let { timezone_name } = this.actionedExam.booking.office.timezone
        let time = zone.tz(tempItem.booking.start_time, timezone_name).format('HH:mm:ss')
        let date = moment(tempItem.booking.start_time).format('YYYY-MM-DD')
        this.time = date + 'T' + time
        this.date = date
        this.offsite_location = tempItem.offsite_location
        this.invigilator_id = tempItem.booking.invigilator_id
        this.editedFields = []
        this.itemCopy = tempItem
      },
      reset() {
        this.time = null
        this.date = null
        this.offsite_location = null
        this.invigilator_id = null
        this.itemCopy = {}
        this.editedFields = []
      }
    },
  }
</script>

<style scoped>
  .id-grid-1st-col {
    margin-left: auto;
    margin-right: 20px;
  }
  .id-grid-1st-col {
    grid-column: 1 / span 2;
    margin-right: 20px;
  }
</style>
