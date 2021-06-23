<template>
  <div id="examModal" class="q-custom-modal" v-if="showModal && date">
    <div class="q-custom-booking-modal">
      <div style="display: flex; justify-content: space-between">
        <div style="font-weight: 600; font-size: 1.3rem">
          {{ formStep === 1 ? 'Confirm Booking' : '' }}
          {{ formStep === 2 ? 'Assign Invigilator' : '' }}
        </div>
        <div>
          <button
            class="btn btn-link"
            @click="minimized ? minimize(false) : minimize(true)"
          >
            {{ minimized ? 'Maximize' : 'Minimize' }}
          </button>
        </div>
      </div>
      <div v-show="formStep === 1 && !minimized">
        <DataSummaryTable :displayData="displayData" class="w-100 p-0 m-0" />
        <b-form class="mt-3">
          <b-form-row v-if="!challengerExam">
            <b-col>
              <b-form-group>
                <label>Contact Information (Email or Phone Number)</label>
                <font-awesome-icon
                  v-if="this.booking_contact_information !== ''"
                  icon="check"
                  style="font-size: 1rem; color: green"
                />
                <br />
                <input
                  id="contact_information"
                  style="height: 38px; font-size: 0.8rem"
                  class="form-control"
                  @focus="setRef"
                  type="text"
                  ref="contact_information"
                  v-model="booking_contact_information"
                />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="12">
              <b-form-group v-if="individualExamInd">
                <label>Invigilator Selection Options</label>
                <b-select
                  :options="invigilatorIndividualOptions"
                  v-model="selectedOption"
                  @input="handleSelect"
                />
              </b-form-group>
              <b-form-group v-else>
                <label>Invigilator Selection Options</label>
                <b-select
                  :options="invigilatorGroupOptions"
                  v-model="selectedOption"
                  @input="handleSelect"
                />
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col>
              <b-form-group>
                <label>Notes</label><br />
                <textarea
                  :rows="2"
                  id="booking_notes"
                  class="form-control"
                  ref="booking_notes"
                  maxlength="255"
                  @focus="setRef"
                  v-model="notes"
                />
              </b-form-group>
            </b-col>
          </b-form-row>
        </b-form>
      </div>
      <div v-show="formStep === 2 && !minimized">
        <div>
          <b-form autocomplete="off">
            <b-form-row>
              <b-col>
                <div>
                  <div class="ai-modal-title">
                    Selected:
                    <strong class="mr-2">{{
                      invigilatorDetails.invigilator_name
                    }}</strong>
                  </div>
                  <div class="info-display-grid-container mt-1">
                    <div class="q-id-grid-outer">
                      <div class="id-grid-col">
                        <div class="mr-1"><strong>Phone: </strong></div>
                        <div>
                          <strong>{{
                            invigilatorDetails.contact_phone
                          }}</strong>
                        </div>
                      </div>
                      <div class="q-id-grid-col">
                        <div class="mr-1">Email:</div>
                        <div>
                          <strong>{{
                            invigilatorDetails.contact_email
                          }}</strong>
                        </div>
                      </div>
                      <div class="q-id-grid-full-col">
                        <div class="mr-1">Notes:</div>
                        <div>
                          <strong>{{
                            invigilatorDetails.invigilator_notes
                          }}</strong>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </b-col>
            </b-form-row>
            <b-form-row class="mt-2 mb-0">
              <b-col>Click an Invigilator on the List Below to Select:</b-col>
            </b-form-row>
            <b-form-row>
              <b-col>
                <b-table
                  :items="invigilator_multi_select"
                  :fields="fields"
                  outlined
                  inverse
                  striped
                  @row-clicked="rowClicked"
                  sort-by="invigilator_name"
                  class="mr-3 mt-1 mb-0 pr-3 pl-3"
                  small
                >
                  <template #cell(invigilator_name)="row">
                    <div class="table-pointer">{{ row.item.name }}</div>
                    <div style="display: none">
                      {{
                        row.item.value == invigilatorId
                          ? (row.item._rowVariant = 'info')
                          : (row.item._rowVariant = '')
                      }}
                    </div>
                  </template>
                </b-table>
              </b-col>
            </b-form-row>
          </b-form>
        </div>
      </div>
      <div class="button-flex-end">
        <div><b-button @click="cancel" class="mt-3">Cancel</b-button></div>
        <div class="button-flex-end">
          <b-button
            class="btn-secondary mt-3"
            v-if="formStep === 2"
            @click="formStep = 1"
            ><font-awesome-icon
              icon="caret-left"
              class="mr-1 p-0"
              style="font-size: 1rem"
            />Back</b-button
          >
          <div v-if="selectedOption === 'invigilator' && formStep === 1">
            <b-button @click="clickNext" class="mt-3 px-3 ml-1 btn-primary"
              >Next
              <font-awesome-icon
                icon="caret-right"
                class="ml-1 p-0"
                style="font-size: 1rem"
            /></b-button>
          </div>
          <div v-if="selectedOption !== 'invigilator' || formStep === 2">
            <b-button
              v-if="this.booking_contact_information.length > 0"
              class="mt-3 ml-1 btn-primary"
              size="md"
              id="final-submit"
              @click="clickOk"
            >
              Submit
            </b-button>
            <b-button
              v-else
              disabled
              variant="primary"
              class="mt-3 ml-1"
              id="disabled-submit"
              size="md"
            >
              Submit
            </b-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
/* eslint-disable */
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

// import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
import DataSummaryTable from './../exams/data-summary-table.vue'
import moment from 'moment'

@Component({
  components: {
    DataSummaryTable
  }
})
export default class BookingModal extends Vue {
  public $refs: any = {
    contact_information: HTMLElement
  };

  @State('selectedExam') private exam!: any
  @State('clickedDate') private date!: any
  @State('showBookingModal') private showModal!: any
  @State('invigilators') private invigilators!: any
  @State('addExamModule') private module!: any
  @State('capturedExam') private capturedExam!: any

  @Getter('invigilator_multi_select') private invigilator_multi_select!: any;

  @Action('finishBooking') public finishBooking: any
  @Action('getExams') public getExams: any
  @Action('getBookings') public getBookings: any
  @Action('getInvigilators') public getInvigilators: any
  @Action('putRequest') public putRequest: any
  @Action('scheduleExam') public scheduleExam: any

  @Mutation('captureExamDetail') public captureExamDetail: any
  @Mutation('setAddExamModalSetting') public setAddExamModalSetting: any
  @Mutation('saveChallengerBooking') public saveChallengerBooking: any
  @Mutation('setClickedDate') public setClickedDate: any
  @Mutation('toggleBookingModal') public toggleBookingModal: any

  public notes: any = ''
  public booking_contact_information: any = ''
  public invigilator: any = null
  public formStep: any = 1
  public fields: any = {
    invigilator_name: {
      label: 'Name',
      thClass: 'd-none'
    }
  }

  public savedRef: any = 'contact_information'
  public selectedOption: any = null
  public invigilatorId: any = null
  public invigilatorIndividualOptions: any = [
    { text: 'ServiceBC Staff', value: 'sbc' },
    { text: 'Contract Invigilator', value: 'invigilator' }
  ]

  public invigilatorGroupOptions: any = [
    { text: 'ServiceBC Staff', value: 'sbc' },
    { text: 'Assign Later', value: 'unassigned' },
    { text: 'Contract Invigilator', value: 'invigilator' }
  ]

  public minimized: any = false
  public pressedSubmit: any = false
  public expiry_date: any = ''
  // TODO Defined clickedRown check Functionality
  public clickedRow: any;

  get buttonStatus () {
    if (!this.selectedOption) {
      return true
    }
    if (this.selectedOption === 'invigilator' && !this.invigilatorId && this.formStep == 2) {
      return true
    }
    return false
  }

  get buttonText () {
    if (this.selectedOption === 'invigilator' && this.formStep == 1) {
      return 'Continue'
    }
    return 'Submit'
  }

  get displayData () {
    const mins = this.exam.exam_type.number_of_minutes ? (this.exam.exam_type.number_of_minutes / 60) : 0
    const length = `${this.exam.exam_type.number_of_hours}.${mins} hrs`
    const items = [
      { key: 'Exam:', value: this.exam.exam_name },
      { key: 'Exam Date:', value: this.date.start.format('dddd MMM D, YYYY') },
      { key: '', value: this.exam.exam_type.exam_type_name },
      { key: 'Exam Time:', value: this.date.start.format('h:mm a') },
      { key: 'Exam Expiry:', value: this.formatExpiry(this.exam.expiry_date) },
      { key: 'Writer:', value: this.exam.examinee_name },
      { key: 'Format of Exam:', value: this.exam.exam_method },
      { key: 'Length of Exam:', value: length },
      { key: 'ServiceBC to Provide Reader:', value: this.invigilatorRequired ? 'Yes' : 'No' },
      { key: 'Room:', value: this.date.resource.title }
    ]
    if (this.exam.exam_type.exam_type_name === 'Monthly Session Exam') {
      const i = items.findIndex(x => x.key === 'Exam Expiry:')
      items[i] = { key: 'Exam Expiry:', value: 'n/a' }
    }
    return {
      title: null,
      items
    }
  }

  get individualExamInd () {
    if (this.exam.exam_type.group_exam_ind === 0) {
      return true
    } else {
      return false
    }
  }

  get invigilatorDetails () {
    if (this.invigilator) {
      return this.invigilator
    }
    return {
      invigilator_name: '',
      contact_phone: '',
      contact_email: '',
      invigilator_notes: ''
    }
  }

  get challengerExam () {
    if (this.exam && this.exam.referrer && this.exam.referrer === 'scheduling') {
      return true
    }
    return false
  }

  get invigilatorRequired () {
    if (this.exam && this.exam.exam_type) {
      if (this.exam.exam_type.exam_type_name.includes('SBC Reader')) {
        return true
      }
    }
    return false
  }

  get endTime () {
    if (this.date && this.exam) {
      const l = parseInt(this.exam.exam_type.number_of_hours)
      const m = parseInt(this.exam.exam_type.number_of_minutes)
      // TOCHECK removed new keyword in moment. not needed
      // return new moment(this.date.start).add(l, 'hours').add(m, 'minutes')
      return moment(this.date.start).add(l, 'hours').add(m, 'minutes')
    }
  }

  formatExpiry (d) {
    // TOCHECK removed new keyword in moment. not needed
    // return new moment(d).format('MMM D, YYYY')
    return moment(d).format('MMM D, YYYY')
  }

  cancel () {
    this.toggleBookingModal(false)
    this.setClickedDate(null)
    this.$root.$emit('removeSavedSelection')
  }

  clickOk (e) {
    e.preventDefault()
    if (this.selectedOption === 'invigilator' && this.formStep === 1) {
      this.formStep++
      return
    }
    if (this.challengerExam) {
      this.setAddExamModalSetting({ fromCalendar: true })
      const date = Object.assign({}, this.date)
      if (this.invigilator && this.invigilator.invigilator_id) {
        date.invigilator = this.invigilator
      }
      if (this.selectedOption === 'sbc') {
        date.invigilator = 'sbc'
      }
      this.saveChallengerBooking(date)
      this.cancel()
      this.setAddExamModalSetting(true)
      this.$router.push('/exams')
      return
    }
    if (this.selectedOption) {
      this.submit()
    }
  }

  minimize (e: any) {
    this.minimized = e
    if (!e) {
      const el: any = this.$refs[this.savedRef]
      setTimeout(() => { el.focus() }, 50)
    }
  }

  resetModal () {
    this.formStep = 1
    this.invigilatorId = null
    this.invigilator = null
    this.notes = ''
    this.expiry_date = ''
  }

  handleSelect (e) {
    this.savedRef = null
    if (e !== 'invigilator') {
      this.invigilatorId = null
      this.invigilator = null
    }
  }

  setupModal () {
    this.resetModal()
    this.pressedSubmit = false
    if (this.exam.notes) { this.notes = this.exam.notes.valueOf() }
    this.$nextTick(function () {
      if (this.$refs.contact_information) {
        this.$refs.contact_information.focus()
      }
    })
    if (this.exam.exam_type.exam_type_name.includes('SBC Reader')) {
      this.selectedOption = 'unassigned'
      return
    }
    if (this.exam.exam_type.exam_type_name === 'Monthly Session Exam') {
      this.selectedOption = 'unassigned'
      return
    }
    this.selectedOption = 'sbc'
    if (!this.exam.notes) {
      this.notes = null
    }
  }

  clickNext () {
    this.formStep = 2
    if (!this.invigilatorId && this.clickedRow) {
      this.clickedRow._rowVariant = ''
    }
  }

  rowClicked (item) {
    this.clickedRow = item
    this.invigilatorId = item.value
    this.invigilator = item
  }

  setRef (e) {
    this.savedRef = e.target.id
  }

  submit () {
    if (this.pressedSubmit == false) {
      this.pressedSubmit = true
      const { exam_id } = this.exam
      let notes = null
      let putNotes = false

      if (this.notes && !this.exam.notes) {
        notes = this.notes
        putNotes = true
      }
      if (!this.notes && this.exam.notes) {
        putNotes = true
      }
      if (this.notes && this.exam.notes) {
        if (this.notes !== this.exam.notes) {
          notes = this.notes
          putNotes = true
        }
      }
      // TOCHECK removed new keyword in moment. not needed
      // const start = new moment(this.date.start).utc()
      const end = moment(this.endTime).utc()
      const start = moment.tz(this.date.start.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).utc()
      if (this.endTime) {
      const end = moment.tz(this.endTime.format('YYYY-MM-DD HH:mm:ss'), this.$store.state.user.office.timezone.timezone_name).utc()
      }

      const booking: any = {
        room_id: this.date.resource.id,
        start_time: start.format('YYYY-MM-DD[T]HH:mm:ssZ'),
        end_time: end.format('YYYY-MM-DD[T]HH:mm:ssZ'),
        fees: 'false',
        booking_name: this.exam.exam_name,
        sbc_staff_invigilated: 0,
        booking_contact_information: this.booking_contact_information
      }
      if (this.selectedOption === 'sbc') {
        booking.sbc_staff_invigilated = 1
      }
      if (this.selectedOption === 'invigilator') {
        booking.invigilator_id = this.invigilatorId
      }
      this.scheduleExam(booking).then(() => {
        const payload: any = {
          url: `/exams/${exam_id}/`
        }
        // eslint-disable-next-line no-unused-expressions
        putNotes ? payload.data = { notes } : null
        let redirect = false
        if (this.exam.referrer === 'inventory') {
          redirect = true
        }
        this.putRequest(payload).then(() => {
          this.getExams().then(() => {
            this.getBookings().then(() => {
              this.finishBooking()
              if (redirect) {
                this.$router.push('/exams')
              }
            })
          })
        })
        this.booking_contact_information = ''
      })
    } else {
      console.log('you have pressed submit already!')
    }
  }

  mounted () {
    this.getInvigilators()
    this.$root.$on('showbookingmodal', () => { this.setupModal() })
  }
}
</script>

<style scoped>
.id-grid-outer {
  display: grid;
  grid-template-columns: 2fr 1fr 4fr 3fr;
}
.sum-td-l-col {
  margin-top: auto;
  margin-left: auto;
  grid-column: 1 / span 2;
  font-size: 1rem;
  font-weight: bold;
}
.sum-td-r-col {
  margin-top: auto;
  margin-left: 20%;
  margin-right: auto;
  grid-column: 3 / span 2;
  font-size: 0.925rem;
  font-weight: normal;
}
.table-holder {
  border: 1px solid lightgray;
  border-radius: 7px;
  font-size: 0.9rem;
  font-weight: normal !important;
}
.info-display-grid-container {
  height: 100%;
  width: 100%;
  padding: 8px 4px 8px 4px;
  border: 1px solid grey;
  border-radius: 5px;
}
.id-grid-col {
  margin-left: 4px;
  margin-right: 14px;
  display: flex;
  justify-content: space-between;
}
.table-pointer {
  cursor: pointer;
}
.button-flex-between {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.button-flex-end {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}
.ai-modal-title {
  font-size: 1rem;
}
</style>
