import Vue from 'vue'
import { mapGetters, mapMutations, mapState } from 'vuex'
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

export const AddExamCounter = Vue.component('add-exam-counter', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState({
      setup: state => state.addExamModal.setup,
      candidates: state => state.addExamModule.candidates
    }),
    numberOfStudents () {
      return this.exam.number_of_students
    },
    currentNumber () {
      if (Array.isArray(this.candidates)) {
        return this.candidates.length
      }
      return 0
    }
  },
  methods: {
    ...mapMutations(['captureExamDetail', 'deleteCapturedExamDetail'])
  },
  watch: {
    numberOfStudents (newVal) {
      if (newVal == this.currentNumber) {
        this.$store.commit('captureExamDetail', { key: 'add_exam_counter', value: 1 })
      } else {
        // this.$store.commit('deleteCapturedExamDetail', 'add_exam_counter')
      }
    },
    currentNumber (newVal) {
      if (newVal == this.exam.number_of_students) {
        this.$store.commit('captureExamDetail', { key: 'add_exam_counter', value: 1 })
      } else {
        // this.$store.commit('deleteCapturedExamDetail', 'add_exam_counter')
      }
    }
  },
  template: `
    <fragment>
      <b-row no-gutters class="mx-2">
        <b-col cols="2">
          <b-form-group>
            <label class="m-0">Total</label>
            <b-input class="my-0 w-50" disabled size="sm" :value="currentNumber" />
          </b-form-group>
        </b-col>

      </b-row>
      <b-row no-gutters v-if="error && !validationObj['add_exam_counter'].valid">
        <b-col cols="11" class="mt-1">
          <span style="color: red">Number of selected exams does not equal the number of candidates</span>
        </b-col>
      </b-row>
    </fragment>
  `
})

export const DateQuestion = Vue.component('date-question', {
  props: ['error', 'exam', 'handleInput', 'q', 'radioChange', 'today', 'validationObj'],
  components: { checkmark, DatePicker },
  data () {
    return {
      date: null
    }
  },
  computed: {
    ...mapState(['user', 'addExamModal', 'capturedExam'])
  },
  beforeMount () {
    if (this.exam.ind_or_group === 'group') {
      this.exam.expiry_date = null
    }
  },
  methods: {
    selectDate (e) {
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
            {{ addExamModal.setup == 'group' || addExamModal.setup == 'challenger' || addExamModal.setup == 'pesticide' ? 'Exam Date' : 'Expiry Date' }}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label><br>
          <DatePicker :value="exam[q.key]"
                      lang="en"
                      @input="selectDate"
                      class="w-50"
                      ></DatePicker>
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid" />
    </b-row>
  `
})

export const DropdownQuestion = Vue.component('dropdown-question', {
  props: ['question', 'exam', 'exam_object', 'examTypes', 'handleInput', 'selected', 'message', 'error'],
  components: { checkmark },
  data () {
    return {
      clicked: false
    }
  },
  computed: {
    ...mapState(['addExamModal', 'capturedExam', 'nonITAExam']),
    dropItems () {
      const sorter = (a, b) => {
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
        const exams = this.examTypes.filter(type =>
          type.ita_ind === 1 &&
          type.group_exam_ind === 0 &&
          !type.exam_type_name.includes('Monthly'))
        return exams.sort((a, b) => sorter(a, b))
      }
      if (this.addExamModal.setup === 'other') {
        const exams = this.examTypes.filter(type =>
          type.ita_ind === 0 &&
          type.group_exam_ind === 0 &&
          type.pesticide_exam_ind === 0 &&
          !type.exam_type_name.includes('Monthly')
        )
        return exams.sort((a, b) => sorter(a, b))
      }
      if (this.addExamModal.setup === 'group') {
        const exams = this.examTypes.filter(type =>
          (type.group_exam_ind === 1 && type.exam_type_name != 'Group Pesticide Exam' && type.exam_type_name != 'Pesticide Group Exam')
        )
        return exams.sort((a, b) => sorter(a, b))
      }
      if (this.addExamModal.setup === 'pesticide') {
        const exams = this.examTypes.filter(type =>
          type.pesticide_exam_ind === 1 &&
          type.group_exam_ind === 0)
        return exams.sort((a, b) => sorter(a, b))
      }
    },
    inputText () {
      if (this.exam_object && this.exam_object.exam_type_name) {
        return this.exam_object.exam_type_name
      }
      return ''
    },
    inputStyle () {
      if (this.exam_object && this.exam_object.exam_type_name) {
        return { backgroundColor: `${this.exam_object.exam_color}` }
      }
      return ''
    },
    dropclass () {
      if (!this.addExamModal.step1MenuOpen) {
        return 'dropdown-menu'
      }
      if (this.addExamModal.step1MenuOpen) {
        return 'dropdown-menu dropdown-menu-right show py-0 my-0 w-100'
      }
    }
  },
  methods: {
    ...mapMutations(['setAddExamModalSetting']),
    clickInput () {
      if (!this.addExamModal.step1MenuOpen) {
        this.setAddExamModalSetting({ step1MenuOpen: true })
        return
      }
      this.setAddExamModalSetting({ step1MenuOpen: false })
    },
    preHandleInput (id) {
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
      <h5 v-if="addExamModal.setup === 'pesticide' ">Add Environment Exam</h5>
      <label>Exam Type</label><br>
        <div @click="clickInput" id="exam_type_dropdown">
          <b-input read-only
                   autocomplete="off"
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
                       autocomplete="off"
                       :id="type.exam_type_id"
                       :class="type.class">{{ type.exam_type_name }}</b-dd-item>
          </template>
        </div>
      </b-col>
    </b-row>
  `
})

export const ExamReceivedQuestion = Vue.component('exam-received-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark, DatePicker, moment },
  data () {
    return {
      date: null,
      options: [
        { text: 'Yes', value: true },
        { text: 'No', value: false }
      ],
      otherOptions: [
        { text: 'No', value: true },
        { text: 'Yes', value: false }
      ]
    }
  },
  computed: {
    ...mapState(['addExamModal', 'captureITAExamTabSetup']),
    showRadio: {
      get () {
        return this.captureITAExamTabSetup.showRadio
      },
      set (e) {
        this.captureExamDetail({ key: 'exam_received_date', value: null })
        this.toggleIndividualCaptureTabRadio(e)
      }
    },
    modalSetup () {
      if (this.addExamModal && this.addExamModal.setup) {
        return this.addExamModal.setup
      }
      return ''
    }
  },
  methods: {
    ...mapMutations(['captureExamDetail', 'toggleIndividualCaptureTabRadio']),
    unsetDate (e) {
      if (!e && this.modalSetup === 'individual') {
        this.handleInput({
          target: {
            name: 'exam_received_date',
            value: null
          }
        })
      }
    },
    preSetDate () {
      if (this.modalSetup === 'other' || this.modalSetup === 'pesticide') {
        this.handleInput({
          target: {
            name: 'exam_received_date',
            value: moment()
          }
        })
      }
    },
    selectRecdDate (e) {
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
                              @change="unsetDate"
                              autocomplete="off"
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
    ...mapState({ setup: state => state.addExamModal.setup })
  },
  methods: {
    preHandleInput (e) {
      this.handleInput(e)
    }
  },
  template: `
    <fragment v-if="q.key === 'exam_name' && setup === 'challenger'">
      <b-row no-gutters>
        <b-col cols="11"><h5>Adding a Monthly Session Exam</h5></b-col>
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
                          :id="q.key"
                          autocomplete="off"
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
                          :id="q.key"
                          autocomplete="off"
                          @input.native="preHandleInput" />
          </b-form-group>
        </b-col>
        <checkmark v-if="setup !=='challenger' " :validated="validationObj[q.key].valid"  />
      </b-row>
    </fragment>
  `
})

export const InputQuestion2 = Vue.component('input-question-2', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  data () {
    return {
      options: [
        { text: 'No', value: false },
        { text: 'Yes', value: true }
      ]
    }
  },
  computed: {
    ...mapState({
      setup: state => state.addExamModal.setup
    }),
    capture_names: {
      get () {
        return this.exam.capture_names
      },
      set (value) {
        this.$store.commit('captureExamDetail', { key: 'capture_names', value })
      }
    }
  },
  methods: {
    preHandleInput (e) {
      this.handleInput(e)
    }
  },
  template: `
    <fragment>
      <b-row no-gutters>
        <b-col cols="3">
          <label>{{q.text}}
              <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label>
        </b-col>
        <b-col cols="9" />
      </b-row>
      <b-row no-gutters class="mb-1">
        <b-col cols="1"><b-form-input :value="exam[q.key]"
                          :name="q.key"
                          :key="q.key"
                          size="sm"
                          class="w-50"
                          :id="q.key"
                          autocomplete="off"
                          @input.native="preHandleInput" />
        </b-col>

        <checkmark :validated="validationObj[q.key].valid" />
      </b-row>
    </fragment>
  `
})

export const LocationInput = Vue.component('location-input-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState({
      examTypes: 'examTypes',
      setup: state => state.addExamModal.setup,
      capturedExam: state => state.capturedExam,
      booking: state => state.addExamModule.booking,
      user: state => state.user
    }),
    showBooking () {
      if (this.booking && Object.keys(booking).length > 1) {
        return 'some specifics when possible'
      }
      return 'Not Scheduled'
    },
    isOffsite () {
      if (this.capturedExam && this.capturedExam.on_or_off) {
        if (this.capturedExam.on_or_off === 'on') {
          return false
        }
        return true
      }
    },
    invigilator () {
      if (this.exam.invigilator) {
        if (this.exam.invigilator === 'sbc') {
          return {
            show: true,
            text: 'SBC Employee'
          }
        }
        if (this.exam.invigilator.invigilator_id) {
          return {
            show: true,
            text: this.exam.invigilator.invigilator_name
          }
        }
      }
      return {
        show: false
      }
    },
    bookingDetails () {
      if (this.exam.exam_time) {
        const date = moment(this.exam.exam_time).format('ddd MMM Do, YYYY')
        const time = moment(this.exam.exam_time).format('h:mm a')
        const room = this.exam.offsite_location.title
        return `${date} @ ${time} in ${room}`
      }
      return 'Not Yet Scheduled'
    }
  },
  methods: {
    ...mapMutations(['toggleScheduling', 'setAddExamModalSetting', 'setSelectedExam']),
    launchSchedule () {
      const { exam_type_id } = this.examTypes.find(t => t.exam_type_name === 'Monthly Session Exam')
      const exam = {
        exam_name: this.exam.exam_name,
        examinee_name: 'Monthly Session',
        exam_method: 'tbd',
        office_id: this.user.office_id,
        exam_type: {
          exam_type_name: 'Monthly Session Exam',
          exam_type_id,
          number_of_hours: 4
        },
        number_of_students: 1
      }
      this.toggleScheduling(true)
      exam.referrer = 'scheduling'
      this.setSelectedExam(exam)
      this.$router.push('/booking')
      this.setAddExamModalSetting(false)
    }
  },
  template: `
    <fragment>
      <template v-if="capturedExam.on_or_off === 'off' || setup === 'pesticide' || setup === 'group' ">
        <b-row no-gutters>
          <b-col cols="11">
            <b-form-group>
              <label>
                {{q.text}}<span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
              </label>
              <b-form-input :value="exam[q.key]"
                            :name="q.key"
                            autocomplete="off"
                            :key="q.key"
                            :id="q.key"
                            @input.native="handleInput" />
            </b-form-group>
          </b-col>
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
          <b-col cols="12">
            <b-form-group>
              <label>Scheduled For
                <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
              </label>
              <b-form-input :value="bookingDetails"
                            disabled />
            </b-form-group>
          </b-col>

        </b-row>
        <b-row no-gutters v-if="invigilator.show">
          <b-col cols="12">
            <b-form-group>
              <label>Invigilator
              </label>
              <b-form-input :value="invigilator.text"
                            autocomplete="off"
                            disabled />
            </b-form-group>
          </b-col>
        </b-row>
      </template>
      </fragment>
  `
})

export const NotesQuestion = Vue.component('notes-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState(['captureITAExamTabSetup']),
    notes () {
      return this.captureITAExamTabSetup.notes
    }
  },
  methods: {
    ...mapMutations(['updateCaptureTab']),
    handleClick () {
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
                    size="sm"
                    id="notes">Display Notes Field?</b-button>
        </b-form-group>
        <b-form-group v-if="notes">
          <label>Notes (Optional)</label><br>
          <b-textarea :value="exam[q.key]"
                      @input.native="handleInput"
                      :rows="3"
                      autocomplete="off"
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
      booking: state => state.addExamModule.booking
    })
  },
  methods: {
    ...mapMutations(['captureExamDetail']),
    preHandleInput (e) {
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
                         autocomplete="off"
                         @change.native="preHandleInput"
                         :class="addExamModal.setup === 'group' ? 'w-50 mr-1' : 'mr-1' "
                         :name="q.key" />
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid" />
    </b-row>
  `
})

export const SelectQuestion = Vue.component('select-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState({
      addExamModal: state => state.addExamModal,
      capturedExam: 'capturedExam'
    }),
    ind_or_group () {
      if (this.capturedExam.ind_or_group) {
        return this.capturedExam.ind_or_group
      }
      return null
    }
  },
  watch: {
    ind_or_group (newVal, oldVal) {
      if (this.addExamModal.setup === 'pesticide' && newVal === 'group') {
        this.$store.commit('captureExamDetail', { key: 'capture_names', value: false })
      }
    }
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
                         autocomplete="off"
                         @change.native="handleInput"
                         :class="addExamModal.setup === 'group' ? 'w-50' : '' "
                         :name="q.key" />
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid"  />
    </b-row>
  `
})

export const SelectOffice = Vue.component('select-office', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark, OfficeDrop },
  data () {
    return {}
  },
  computed: {
    ...mapGetters(['role_code']),
    ...mapState(['offices', 'user', 'addExamModal']),
    office_number () {
      return this.addExamModal.office_number
    },
    Error () {
      if (this.error && this.validationObj.office_id.message) {
        return true
      }
      return false
    },
    message () {
      if (this.error && this.validationObj.office_id.message) {
        return this.validationObj.office_id.message
      }
      return '(Start typing to search or enter Office #)'
    }
  },
  methods: {
    ...mapMutations(['setAddExamModalSetting']),
    setOffice (office_number) {
      office_number = parseInt(office_number)
      this.setAddExamModalSetting({ office_number })
      if (this.offices && this.offices.length > 0) {
        const office = this.offices.find(office => office.office_number == office_number) || null
        if (office) {
          const { office_id } = office
          this.handleInput({
            target: {
              name: 'office_id',
              value: office_id
            }
          })
          this.$nextTick(function () { this.$root.$emit('validateform') })
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
  props: ['error', 'exam', 'handleInput', 'q', 'radioChange', 'today', 'validationObj'],
  components: { checkmark, DatePicker },
  data () {
    return {
      date: ''
    }
  },
  computed: {
    ...mapState(['user', 'capturedExam', 'addExamModal'])
  },
  methods: {
    selectTime (e) {
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
                      autocomplete="off"
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
