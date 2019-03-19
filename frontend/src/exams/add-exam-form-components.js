import Vue from 'vue'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
import DatePicker from 'vue2-datepicker'
import moment from 'moment'
import OfficeDrop from './office-drop'

export const checkmark = Vue.component('checkmark', {
  props: ['validated'],
  template: `
    <b-col align-self="center"
               cols="1"
               v-if="validated">
      <font-awesome-icon icon="check"
                         class="p-0 ml-2"
                         style="color: green;
                                font-weight: 400;
                                font-size: 1.3rem;" />
    </b-col>
  `
})

export const DateQuestion = Vue.component('date-question', {
  props: ['error', 'exam', 'handleInput', 'q', 'radioChange','today', 'validationObj'],
  components: { checkmark, DatePicker },
  data() {
    return {
      date: null
    }
  },
  computed: {
    ...mapState(['user', 'addExamModal', 'capturedExam']),
  },
  methods: {
    selectDate(e) {
      this.handleInput({
        target: {
          name: 'expiry_date',
          value: e
        }
      })
    }
  },
  template: `
    <b-row no-gutters v-if="addExamModal.setup !== 'challenger' || capturedExam.on_or_off === 'off' ">
      <b-col cols="11">
        <b-form-group>
          <label>
            {{ addExamModal.setup == 'group' || addExamModal.setup == 'challenger' ? 'Exam Date' : 'Expiry Date' }}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label><br>
          <DatePicker :value="exam[q.key]" lang="en" @input="selectDate" class="w-50"></DatePicker>
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid" />
    </b-row>
  `
})

export const DropdownQuestion = Vue.component('dropdown-question',{
  props: ['question', 'exam', 'exam_object', 'examTypes', 'handleInput', 'selected', 'message', 'error'],
  components: { checkmark },
  data() {
    return {
      clicked: false,
    }
  },
  computed: {
    ...mapState(['addExamModal', 'capturedExam', 'nonITAExam' ]),
    dropItems() {
      let sorter = (a, b) => {
        var typeA = a.exam_type_name
        var typeB = b.exam_type_name
        if (typeA < typeB) {
          return -1
        }
        if (typeA > typeB) {
          return 1
        }
        return 0
      }
      if (this.addExamModal.setup === 'individual') {
        let exams = this.examTypes.filter(type => type.exam_type_name.includes('Single'))
        return exams.sort((a,b) => sorter(a,b))
      }
      // TODO reimplement filter for Pesticides when they are re-activated
      if(this.addExamModal.setup === 'other') {
        let exams = this.examTypes.filter( type =>
          !type.exam_type_name.includes('Group') &&
          !type.exam_type_name.includes('Single') &&
          !type.exam_type_name.includes('Challenger Exam Session')
        )
        return exams.sort((a,b) => sorter(a,b))
      }
      if (this.addExamModal.setup === 'group') {
        let exams = this.examTypes.filter(type => type.exam_type_name.includes('Group'))
        return exams.sort((a,b) => sorter(a,b))
      }
      if (this.addExamModal.setup === 'pesticide') {
        let exams = this.examTypes.filter(type => type.exam_type_name.includes('Pesticide'))
        return exams
      }
    },
    inputText() {
      if (this.exam_object && this.exam_object.exam_type_name) {
        return this.exam_object.exam_type_name
      }
      return ''
    },
    inputStyle() {
      if (this.exam_object && this.exam_object.exam_type_name) {
        return {backgroundColor: `${this.exam_object.exam_color}`}
      }
      return ''
    },
    dropclass() {
      if (!this.addExamModal.step1MenuOpen) {
        return 'dropdown-menu'
      }
      if (this.addExamModal.step1MenuOpen) {
        return 'dropdown-menu dropdown-menu-right show py-0 my-0 w-100'
      }
    }
  },
  methods: {
    ...mapMutations(['toggleAddExamModal', 'toggleAddExamModal']),
    clickInput() {
      if (!this.addExamModal.step1MenuOpen) {
        this.toggleAddExamModal({step1MenuOpen: true})
        return
      }
      this.toggleAddExamModal({step1MenuOpen: false})
    },
    preHandleInput(id) {
      this.handleInput({
        target: {
          name: 'exam_type_id',
          value: id
        }
      })
    }
  },
  template: `
    <b-row no-gutters>
      <b-col class="dropdown">
      <h5 v-if="addExamModal.setup === 'group' ">Add Group Exam</h5>
      <h5 v-if="addExamModal.setup === 'individual' ">Add Individual ITA Exam</h5>
      <h5 v-if="addExamModal.setup === 'other' ">Add Non-ITA Exam</h5>
      <label>Exam Type</label><br>
        <div @click="clickInput">
          <b-input read-only
                   :value="inputText"
                   placeholder="click here to see options"
                   :style="inputStyle" />
        </div>
        <div :class="dropclass"
             style="border: 1px solid grey"
             @click="clickInput">
          <template v-for="type in dropItems">
            <b-dd-header v-if="type.header"
                         :style="{backgroundColor: type.exam_color}"
                         :class="type.class">{{ type.exam_type_name }}</b-dd-header>
            <b-dd-item v-else :style="{backgroundColor: type.exam_color}"
                       @click="preHandleInput(type.exam_type_id)"
                       :name="type.exam_type_id"
                       :id="type.exam_type_id"
                       :class="type.class">{{ type.exam_type_name }}</b-dd-item>
          </template>
        </div>
      </b-col>
    </b-row>
  `
})

export const ExamReceivedQuestion = Vue.component('exam-received-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam',],
  components: { checkmark, DatePicker, moment },
  data() {
    return {
      date: null,
      options: [
        {text: 'Yes', value: true},
        {text: 'No', value: false}
      ],
      otherOptions: [
        {text: 'No', value: true},
        {text: 'Yes', value: false}
      ]
    }
  },
  computed: {
    ...mapState(['addExamModal', 'captureITAExamTabSetup',]),
    showRadio: {
      get() {
        return this.captureITAExamTabSetup.showRadio
      },
      set(e) {
        this.captureExamDetail({ key: 'exam_received_date', value: null })
        this.toggleIndividualCaptureTabRadio(e)
      }
    },
    modalSetup() {
      if (this.addExamModal && this.addExamModal.setup) {
        return this.addExamModal.setup
      }
      return ''
    }
  },
  methods: {
    ...mapMutations(['captureExamDetail', 'toggleIndividualCaptureTabRadio']),
    preSetDate() {
      if (this.modalSetup === 'other' || this.modalSetup === 'pesticide') {
        this.handleInput({
          target: {
            name: 'exam_received_date',
            value: moment()
          }
        })
      }
    },
    selectRecdDate(e) {
      console.log(e)
      this.handleInput({
        target: {
          name: 'exam_received_date',
          value: e
        }
      })
    }
  },
  template: `
    <b-row no-gutters>
      <b-col cols="6">
        <b-form-group v-if="showRadio">
          <label>{{ q.text1 }}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label><br>
          <b-form-radio-group v-model="showRadio"
                              @input="preSetDate()"
                              :options="['other', 'pesticide'].includes(modalSetup) ? otherOptions : options"/>
        </b-form-group>
        <b-form-group v-else>
          <label>{{ q.text2 }}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label>
          <DatePicker :value="exam[q.key]" lang="en" @input="selectRecdDate"></DatePicker>
        </b-form-group>
      </b-col>
      <b-col cols="5" />
      <checkmark :validated="validationObj[q.key].valid" />
    </b-row>
  `
})

export const InputQuestion = Vue.component('input-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState({
      setup: state => state.addExamModal.setup }),
  },
  methods: {
    preHandleInput(e) {
      this.handleInput(e)
    }
  },
  template: `
    <fragment v-if="q.key === 'exam_name' && setup === 'challenger'">
      <b-row no-gutters>
        <b-col cols="11"><h5>Adding a Challenger Exam</h5></b-col>
      </b-row>
      <b-row no-gutters>
        <b-col cols="11">
          <b-form-group>
            <label>
              {{q.text}}<span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
            </label>
            <b-form-input :value="exam[q.key]"
                          :name="q.key"
                          :key="q.key"
                          @input.native="preHandleInput" />
          </b-form-group>
        </b-col>
      <checkmark :validated="validationObj[q.key].valid"  />
    </b-row>
    </fragment>
    <fragment v-else>
      <b-row no-gutters>
        <b-col cols="11">
          <b-form-group>
            <label>{{q.text}}
              <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
            </label>
            <b-form-input :value="exam[q.key]"
                          :name="q.key"
                          :key="q.key"
                          @input.native="preHandleInput" />
          </b-form-group>
        </b-col>
        <checkmark v-if="setup !=='challenger' " :validated="validationObj[q.key].valid"  />
      </b-row>
    </fragment>
  `
})

export const LocationInput = Vue.component('input-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState({
      setup: state => state.addExamModal.setup,
      capturedExam: state => state.capturedExam,
      booking: state => state.addExamModule.booking,
      user: state => state.user,
    }),
    showBooking() {
      if (this.booking && Object.keys(booking).length > 1) {
        return 'some specifics when possible'
      }
      return 'Not Scheduled'
    },
    isOffsite() {
      if (this.capturedExam && this.capturedExam.on_or_off) {
        if (this.capturedExam.on_or_off === 'on') {
          return false
        }
        return true
      }
    },
    bookingDetails() {
      if (this.booking && this.booking.start) {
        let date = this.booking.start.format('ddd MMM Do, YYYY')
        let time = this.booking.start.format('h:mm a')
        let room = this.booking.resource.title
        return `${date} @ ${time} in ${room}`
      }
      return 'Not Yet Scheduled'
    }
  },
  methods: {
    ...mapActions(['actionSaveAll']),
    ...mapMutations(['toggleScheduling', 'toggleAddExamModal', 'setSelectedExam']),
    launchSchedule() {
      let exam = {
        exam_name: 'Challenger Exam',
        examinee_name: 'Challenger Exam',
        exam_method: 'tbd',
        offiice_id: this.user.office_id,
        exam_type: {
          exam_type_name: 'Challenger Exam Session',
          exam_type_id: 16,
          number_of_hours: 4,
        },
        number_of_students: 1,
      }
      this.actionSaveAll().then( () => {
        this.toggleScheduling(true)
        exam.referrer = 'scheduling'
        this.setSelectedExam(exam)
        this.$router.push('/booking')
        this.toggleAddExamModal(false)
      })
    }
    
  },
  template: `
    <fragment>
      <template v-if="capturedExam.on_or_off === 'off'">
        <b-row no-gutters>
          <b-col cols="11">
            <b-form-group>
              <label>
                {{q.text}}<span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
              </label>
              <b-form-input :value="exam[q.key]"
                            :name="q.key"
                            :key="q.key"
                            @input.native="handleInput" />
            </b-form-group>
          </b-col>
          <checkmark :validated="validationObj[q.key].valid"  />
        </b-row>
      </template>
      <template v-if="capturedExam.on_or_off === 'on'">
        <b-row no-gutters>
          <b-col>
            <b-form-group>
              <label>Confirm Room Availability</label><br>
              <b-button class="w-100 ml-1 btn-warning"
                        @click="launchSchedule()">Launch Scheduler</b-button>
            </b-form-group>
          </b-col>
        </b-row>
        <b-row no-gutters >
          <b-col cols="11">
            <b-form-group>
              <label>Scheduled For
                <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
              </label>
              <b-form-input :value="bookingDetails"
                            disabled />
            </b-form-group>
          </b-col>
           <checkmark :validated="validationObj[q.key].valid"  />
        </b-row>
      </template>
      </fragment>
  `
})

export const SelectQuestion = Vue.component('select-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState({
      addExamModal: state => state.addExamModal,
    }),
  },
  template: `
    <b-row no-gutters>
      <b-col cols="11">
        <b-form-group>
          <label>{{q.text}}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label><br>
          <b-form-select :options="q.options"
                         :value="exam[q.key]"
                         @change.native="handleInput"
                         :class="addExamModal.setup === 'group' ? 'w-50' : '' "
                         :name="q.key" />
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid"  />
    </b-row>
  `,
})

export const NotesQuestion = Vue.component('notes-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState(['captureITAExamTabSetup']),
    notes() {
      return this.captureITAExamTabSetup.notes
    }
  },
  methods: {
    ...mapMutations(['updateCaptureTab']),
    handleClick() {
      this.updateCaptureTab({ notes: true })
    }
  },
  template: `
    <b-row no-gutters >
      <b-col cols="12">
        <b-form-group v-if="!notes">
          <label>Click to Display the Notes Field (Optional)</label><br>
          <b-button @click="handleClick"
                    class="btn-secondary"
                    size="sm">Display Notes Field?</b-button>
        </b-form-group>
        <b-form-group v-if="notes">
          <label>Notes (Optional)</label><br>
          <b-textarea :value="exam[q.key]"
                      @input.native="handleInput"
                      :rows="3"
                      :name="q.key"
                      :id="q.key" />
        </b-form-group>
      </b-col>
    </b-row>
  `
})

export const OffsiteSelect = Vue.component('offsite-select', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState({
      addExamModal: 'addExamModal',
      capturedExam: 'capturedExam',
      user: 'user',
      booking: state => state.addExamModule.booking,
    }),
  },
  methods: {
    ...mapActions(['actionSaveAll']),
    ...mapMutations(['captureExamDetail']),
    resetGroupQuestions() {
      ['expiry_date', 'offsite_location', 'exam_time'].forEach(item => {
        this.captureExamDetail({key: item, value: null})
      })
    },
    preHandleInput(e) {
      if (this.exam.on_or_off && e.target.value !== this.exam.on_or_off) {
        this.resetGroupQuestions()
      }
      this.handleInput(e)
    }
  },
  template: `
    <b-row no-gutters>
      <b-col :cols="11">
        <b-form-group>
          <label>{{q.text}}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label><br>
          <b-form-select :options="q.options"
                         :value="exam[q.key]"
                         @change.native="preHandleInput"
                         :class="addExamModal.setup === 'group' ? 'w-50 mr-1' : 'mr-1' "
                         :name="q.key" />
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid" />
    </b-row>
  `,
})

export const SelectOffice = Vue.component('select-office', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam',],
  components: { checkmark, OfficeDrop },
  data() {
    return {}
  },
  computed: {
    ...mapGetters(['role_code', 'pesticide_designate', ]),
    ...mapState(['offices', 'user', 'addExamModal']),
    office_number() {
      return this.addExamModal.office_number
    },
    Error() {
      if (this.error && this.validationObj['office_id'].message) {
        return true
      }
      return false
    },
    message() {
      if (this.error && this.validationObj['office_id'].message) {
        return this.validationObj['office_id'].message
      }
      return `(Start typing to search or enter Office #)`
    }
  },
  methods: {
    ...mapMutations(['toggleAddExamModal']),
    setOffice(office_number) {
      office_number = parseInt(office_number)
      this.toggleAddExamModal({office_number})
      if (this.offices && this.offices.length > 0) {
        let office = this.offices.find(office => office.office_number == office_number) || null
        if (office) {
          let { office_id } = office
          this.handleInput({
            target: {
              name: 'office_id',
              value: office_id
            }
          })
          return
        }
        this.handleInput({
          target: {
            name: 'office_id',
            value: null
          }
        })
      }
    }
  },
  template: `
      <b-row no-gutters class="mb-2">
        <OfficeDrop columnW="9" :office_number="office_number" :setOffice="setOffice" :msg="message" :error="Error" />
        <checkmark :validated="validationObj[q.key].valid"  />
      </b-row>
  `
})

export const TimeQuestion = Vue.component('time-question', {
  props: ['error', 'exam', 'handleInput', 'q', 'radioChange','today', 'validationObj'],
  components: { checkmark, DatePicker },
  data() {
    return {
      date: ''
    }
  },
  computed: {
    ...mapState(['user', 'capturedExam', 'addExamModal']),
  },
  methods: {
    selectTime(e) {
      this.handleInput({
        target: {
          name: 'exam_time',
          value: e
        }
      })
    }
  },
  template: `
    <b-row no-gutters  v-if="addExamModal.setup !== 'challenger' || capturedExam.on_or_off === 'off' ">
      <b-col cols="11">
        <b-form-group>
          <label>
            Exam Time
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label><br>
          <DatePicker :value="exam[q.key]"
                      :time-picker-options="{ start: '8:00', step: '00:30', end: '17:00' }"
                      lang="en"
                      @input="selectTime"
                      format="h:mm a"
                      confirm
                      placeholder="Select Time"
                      class="w-50"
                      type="time">
            <template slot="calendar-icon">
              <font-awesome-icon icon="clock"
                                 class="m-0 p-0"
                                 style="font-size: .9rem;"/>
            </template>
          </DatePicker>
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid" />
    </b-row>
  `
})

