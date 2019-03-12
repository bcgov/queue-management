<template>
  <b-modal v-model="modalVisible"
           modal-class="q-modal"
           body-class="q-modal"
           no-close-on-backdrop
           no-close-on-esc
           lazy
           :ok-disabled="buttonStatus"
           :ok-title="buttonText"
           @cancel="cancel"
           @ok="clickOk"
           @shown="setupModal"
           hide-header
           size="md">
    <div v-if="showModal && formStep == 1">
      <span style="font-weight: 600; font-size: 1.3rem;">Confirm Booking</span>
      <DataSummaryTable :displayData="displayData" class="w-100 p-0 m-0" />
      <b-form class="mt-3">
        <b-form-row>
          <b-col cols="12">
            <b-form-group>
              <label>Invigilator Selection Options</label>
              <b-select :options="invigilatorOptions" v-model="selectedOption" @input="handleSelect"/>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group>
              <label>Notes</label><br>
              <b-textarea :rows="2" v-model="notes" />
            </b-form-group>
          </b-col>
        </b-form-row>
      </b-form>
    </div>
    <div v-if="showModal && formStep == 2">
      <span style="font-weight: 600; font-size: 1.3rem;">Assign Invigilator</span>
      <b-form>
        <b-form-row>
          <b-col>
            <div class="table-holder">
              <div class="info-display-grid-container mt-1">
                <div class="q-id-grid-outer">
                  <div class="q-id-grid-head mb-1">
                    <strong class="mr-2">Selected:</strong> {{ invigilatorDetails.invigilator_name }}</div>
                  <div class="id-grid-col">
                    <div class="mr-1"><strong>Phone: </strong></div>
                    <div>{{ invigilatorDetails.contact_phone }}</div>
                  </div>
                  <div class="q-id-grid-col">
                    <div class="mr-1">Email: </div>
                    <div>{{ invigilatorDetails.contact_email }}</div>
                  </div>
                  <div class="q-id-grid-full-col">
                    <div class="mr-1">Notes: </div>
                    <div>{{ invigilatorDetails.invigilator_notes }}</div>
                  </div>
                </div>
              </div>
            </div>
          </b-col>
        </b-form-row>
        <b-form-row class="mt-2 mb-0">
          <b-col>Click an Invigilator to Select</b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-table :items="invigilators"
                     :fields="fields"
                     outlined
                     inverse
                     striped
                     :selectable="true"
                     select-mode="multi"
                     selectedVariant="success"
                     @row-clicked="rowClicked"
                     sort-by="invigilator_name"
                     class="mr-3 mt-1 mb-0 pr-3 pl-3"
                     small>
              <template slot="invigilator_name" slot-scope="row">
                <div class="table-pointer">{{ row.item.invigilator_name }}</div>
                <div style="display: none">
                  {{ row.item.invigilator_id == selectedInvigilator ?
                  row.item._rowVariant='info' : row.item._rowVariant=''
                  }}
                </div>
              </template>
            </b-table>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col><b-button class="btn-secondary mt-3"
                           @click="formStep=1"><font-awesome-icon icon="caret-left"
                             class="mr-1 p-0"
                             style="font-size: 1rem;"/>Back</b-button></b-col>
        </b-form-row>
      </b-form>
    </div>
  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState } from 'vuex'
  import moment from 'moment'
  import DataSummaryTable from './../exams/data-summary-table'

  export default {
    name: "BookingModal",
    components: { DataSummaryTable },
    mounted(){
      this.getInvigilators()
    },
    data() {
      return {
        notes: '',
        invigilator: null,
        formStep: 2,
        fields: {
          invigilator_name: {
            label: 'Name',
            thClass: 'd-none',
          },
        },
        selectedOption: null,
        selectedInvigilator: null,
        invigilatorOptions: [
          {text: 'ServiceBC Staff', value: 'sbc'},
          {text: 'Assign Later', value: 'unassigned'},
          {text: 'Contract Invigilator', value: 'invigilator'},
        ]
      }
    },
    computed: {
      ...mapState({
        exam: state => state.selectedExam,
        date: state => state.clickedDate,
        showModal: state => state.showBookingModal,
        invigilators: state => state.invigilators,
        module: state => state.addExamModule,
        capturedExam: state => state.capturedExam,
      }),
      buttonStatus() {
        if (!this.selectedOption) {
          return true
        }
        if (this.selectedOption === 'invigilator' && !this.selectedInvigilator && this.formStep == 2) {
          return true
        }
        return false
      },
      buttonText() {
        if (this.selectedOption === 'invigilator' && this.formStep == 1) {
          return 'Continue'
        }
        return 'Submit'
      },
      huh() {
        return this.notes == this.exam.notes
      },
      displayData() {
        let items = [
          { key: 'Exam:', value: this.exam.exam_name },
          { key: 'Exam Date:', value: this.date.start.local().format('dddd MMM D, YYYY') },
          { key: '', value: this.exam.exam_type.exam_type_name },
          { key: 'Exam Time:', value: this.date.start.local().format('h:mm a') },
          { key: 'Exam Expiry:', value: this.formatExpiry(this.exam.expiry_date) },
          { key: 'Writer:', value: this.exam.examinee_name },
          { key: 'Format of Exam:', value: this.exam.exam_method },
          { key: 'Length of Exam:', value: this.exam.exam_type.number_of_hours + ' hrs' },
          { key: 'ServiceBC to Provide Reader:', value: this.invigilatorRequired ? 'Yes' : 'No' },
          { key: 'Room:', value: this.date.resource.title },
        ]
        if (this.exam.exam_type.exam_type_name === 'Challenger Exam Session') {
          let i = items.findIndex(x => x.key === 'Exam Expiry:')
          items[i] = {key: 'Exam Expiry:', value: 'n/a'}
        }
        return {
          title: 'Booking Details',
          items
        }
      },
      invigilatorDetails() {
        if (this.invigilator) {
          return this.invigilator
        }
        return {
          invigilator_name: '',
          contact_phone: '',
          contact_email: '',
          invigilator_notes: '',
        }
      },
      challengerExam() {
        if (this.capturedExam && this.capturedExam.on_or_off && this.capturedExam.on_or_off === 'on') {
          return true
        }
        return false
      },
      invigilatorRequired() {
        if (this.exam && this.exam.exam_type) {
          if (this.exam.exam_type.exam_type_name.includes('SBC Reader')) {
            return true
          }
        }
        return false
      },
      handleSelect(e) {
        if (!this.selectedOption || e !== this.selectedOption) {
          this.selectedInvigilator = null
          this.invigilator = null
        }
      },
      modalVisible: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleBookingModal(e)
        }
      },
      endTime() {
        if (this.date && this.exam) {
          let l = parseInt(this.exam.exam_type.number_of_hours)
          return new moment(this.date.start).add(l, 'hours')
        }
      },
    },
    methods: {
      ...mapActions([
        'actionRestoreAll',
        'finishBooking',
        'getExams',
        'getBookings',
        'getInvigilators',
        'putRequest',
        'scheduleExam',
      ]),
      ...mapMutations(['captureExamDetail', 'saveBooking', 'setClickedDate', 'toggleBookingModal', ]),
      formatExpiry(d) {
        return new moment(d).local().format('MMM D, YYYY')
      },
      cancel() {
        this.toggleBookingModal(false)
        this.setClickedDate(null)
        this.$root.$emit('removeSavedSelection')
      },
      clickOk(e) {
        e.preventDefault()
        if (this.challengerExam) {
          this.saveBooking(this.date)
          this.actionRestoreAll().then( () => {
            this.cancel()
            this.$router.push('/exams')
          })
          return
        }
        if (this.selectedOption === 'invigilator') {
          this.formStep = 2
          return
        }
        if (this.selectedOption) {
          this.postEvent()
        }
      },
      resetModal() {
        this.formStep = 1
        this.selectedInvigilator = null
        this.invigilator = null
        this.notes = ''
      },
      setupModal() {
        this.resetModal()
        if (this.exam.exam_type.exam_type_name.includes('SBC Reader')) {
          this.selectedOption = 'unassigned'
          return
        }
        if (this.exam.exam_type.exam_type_name.includes('Challenger')) {
          this.selectedOption = 'unassigned'
          return
        }
        this.selectedOption = 'sbc'
        if (!this.exam.notes) {
          this.notes = null
          return
        }
        this.notes = this.exam.notes.valueOf()
      },
      rowClicked(item) {
        this.selectedInvigilator = item.invigilator_id
        this.invigilator = item
      },
      postEvent() {
        let exam_id = null
        //notes are the only field editable on this form that would need a PUT to '/exams/'
        //if they have not changed, we only need to POST the booking to '/booking/']
        if (this.notes) {
          if (this.exam.notes) {
            if (this.notes != this.exam.notes) {
              exam_id = this.exam.exam_id.valueOf()
            }
          }
          if (!this.exam.notes) {
            exam_id = this.exam.exam_id.valueOf()
          }
        }
        if (!this.notes) {
          if (this.exam.notes) {
            exam_id = this.exam.exam_id.valueOf()
          }
        }
        let start = new moment(this.date.start).utc()
        let end = new moment(this.endTime).utc()
        let booking = {
          room_id: this.date.resource.id,
          start_time: start.format('DD-MMM-YYYY[T]HH:mm:ssZ'),
          end_time: end.format('DD-MMM-YYYY[T]HH:mm:ssZ'),
          fees: 'false',
          booking_name: this.exam.exam_name,
          sbc_staff_invigilated: 0,
        }
        if (this.selectedOption === 'sbc') {
          booking.sbc_staff_invigilated = 1
        }
        if (this.selectedOption === 'invigilator') {
          booking.invigilator_id = this.selectedInvigilator
        }
        this.scheduleExam(booking).then( () =>{
          if (exam_id) {
            let payload = {
              url: `/exams/${exam_id}/`,
              data: {
                notes: this.notes
              }
            }
            this.putRequest(payload).then( () => {
              this.getExams().then( () => {
                this.getBookings().then( () => {
                  this.finishBooking()
                })
              })
            })
          } else {
            this.getExams().then( () => {
              this.getBookings().then( () => {
                this.finishBooking()
              })
            })
          }
        })
      }
    },
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
    font-size: .9rem;
    font-weight: normal !important;
  }
  .info-display-grid-container {
    height: 100%;
    width: 100%;
    padding: 4px;
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

</style>
