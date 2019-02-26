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

export const InputQuestion = Vue.component('input-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  template: `
    <b-row no-gutters>
      <b-col cols="11">
        <b-form-group>
          <label>{{q.text}}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label>
          <b-form-input :value="exam[q.key]"
                        :name="q.key"
                        :key="q.key"
                        @input.native="handleInput" />
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid"  />
    </b-row>
  `
})

export const SelectQuestion = Vue.component('select-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
  computed: {
    ...mapState(['addExamModal']),
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

export const SelectOffice = Vue.component('select-office', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam',],
  components: { checkmark, OfficeDrop },
  data() {
    return {}
  },
  computed: {
    ...mapGetters(['role_code']),
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
    }
  },
  methods: {
    ...mapMutations(['captureExamDetail', 'toggleIndividualCaptureTabRadio']),
    preSetDate() {
      if (this.addExamModal.setup === 'other') {
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
                              @input="preSetDate"
                              :options="addExamModal.setup === 'other' ? otherOptions : options" />
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

export const DateQuestion = Vue.component('date-question', {
  props: ['error', 'exam', 'handleInput', 'q', 'radioChange','today', 'validationObj'],
  components: { checkmark, DatePicker },
  data() {
    return {
      date: null
    }
  },
  computed: {
    ...mapState(['user', 'addExamModal']),
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
    <b-row no-gutters>
      <b-col cols="11">
        <b-form-group>
          <label>
            {{ addExamModal.setup == 'group' ? 'Exam Date' : 'Expiry Date' }}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label><br>
          <DatePicker :value="exam[q.key]" lang="en" @input="selectDate" class="w-50"></DatePicker>
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid" />
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
    ...mapState(['user']),
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
    <b-row no-gutters>
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
                      class="w-50"
                      type="time"></DatePicker>
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
      if(this.addExamModal.setup === 'other') {
        let exams = this.examTypes.filter(type  => type.ita_ind === 0)
        return exams.sort((a,b) => sorter(a,b))
      }
      if (this.addExamModal.setup === 'group') {
        let exams = this.examTypes.filter(type => type.exam_type_name.includes('Group'))
        return exams.sort((a,b) => sorter(a,b))
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
  },
  template: `
    <b-row no-gutters>
      <b-col class="dropdown">
      <h5 v-if="addExamModal.setup === 'group' ">Add Group Exam</h5>
      <h5 v-if="addExamModal.setup === 'individual' ">Add Individual ITA Exam</h5>
      <h5 v-else-if="addExamModal.setup === 'other' ">Add Non-ITA Exam</h5>
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
                       @click="handleInput"
                       :name="type.exam_type_id"
                       :id="type.exam_type_id"
                       :class="type.class">{{ type.exam_type_name }}</b-dd-item>
          </template>
        </div>
      </b-col>
    </b-row>
  `
})
