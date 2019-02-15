import Vue from 'vue'
import { mapMutations, mapState } from 'vuex'
import DatePicker from 'vue2-datepicker'

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
                         :name="q.key" />
        </b-form-group>
      </b-col>
      <checkmark :validated="validationObj[q.key].valid"  />
    </b-row>
  `
})

export const SelectOffice = Vue.component('select-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam',],
  components: { checkmark },
  data() {
    return {
      search: '',
      selected: '',
      officeId: '',
      fields: [
        {key: 'office_name', thStyle: 'width: 70%'},
        {key: 'office_id', thStyle: 'width: 30%'}
      ]
    }
  },
  computed: {
    ...mapState(['offices', 'capturedExam']),
    displaySelection() {
      if (this.offices && this.capturedExam && this.capturedExam.office_id) {
        let name = this.offices.find(office => office.office_id == this.capturedExam['office_id']).office_name
        let id = this.capturedExam.office_id
        return `${id} - ${name}`
      }
      return ''
    },
    items() {
      if (!this.search) {
        if (this.selected) {
          return this.selected
        }
        return this.offices
      }
      if (this.selected) {
        return this.selected
      }
      return this.offices
    }
  },
  methods: {
    filter(e) {
      this.search = e
      
    },
    rowClicked(item, index) {
      this.officeId = item.office_id
      this.handleInput({
        target: {
          name: 'office_id',
          value: item.office_id
        }
      })
    },
  },
  template: `
      <b-row no-gutters class="mb-2">
        <b-col cols="11" class="mb-0">
          <label>Search for Office</label><br>
          <b-form-input :value="search"
                        id="input1ref"
                        style="border-radius: 0px; border: 1px solid lightgrey"
                        @input="filter"
                        class="mb-1"
                        placeholder="Start typing to search"/>
            <div style="border: 1px solid lightgrey">
            <b-table :items="items"
                     :fields="fields"
                     :filter="search"
                     :show-empty="true"
                     :small="true"
                     :per-page="3"
                     class="pb-0"
                     :id="q.key"
                     head-variant="light"
                     hover
                     :fixed="true"
                     id="office_select_table"
                     @row-clicked="rowClicked">
              <template slot="office_name" slot-scope="data">
                <div>
                  <span>
                    {{ data.item.office_name }}
                  </span>
                    <div style="display: none">
                    {{
                      (officeId == data.item.office_id) ?
                      (data.item._rowVariant='active') : (data.item._rowVariant='')
                    }}
                  </div>
                </div>
              </template>
            </b-table>
          </div>
        </b-col>
        <checkmark :validated="validationObj[q.key].valid"  />
      </b-row>
 
  
  `
})

export const ExamReceivedQuestion = Vue.component('exam-received-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam',],
  components: { checkmark, DatePicker },
  data() {
    return {
      date: null,
      options: [
        {text: 'Yes', value: true},
        {text: 'No', value: false}
      ]
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
                              :options="options" />
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
  `,
  computed: {
    ...mapState(['captureITAExamTabSetup']),
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
      selectRecdDate(e) {
        this.handleInput({
          target: {
            name: 'exam_received_date',
            value: e
          }
        })
      }
      },
})

export const NotesQuestion = Vue.component('notes-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam'],
  components: { checkmark },
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
  `,
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
  }
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
    ...mapState(['user', 'addITAExamModal']),
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
            {{ addITAExamModal.setup == 'group' ? 'Exam Date' : 'Expiry Date' }}
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label>
          <DatePicker :value="exam[q.key]" lang="en" @input="selectDate"></DatePicker>
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
          </label>
          <DatePicker :value="exam[q.key]"
                      :time-picker-options="{ start: '8:00', step: '00:30', end: '17:00' }"
                      lang="en"
                      @input="selectTime"
                      format="h:mm a"
                      confirm
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
    ...mapState(['addITAExamModal', 'capturedExam', 'nonITAExam' ]),
    dropItems() {
      if (this.addITAExamModal.setup === 'individual' && !this.nonITAExam) {
        return this.examTypes.filter(type => type.exam_type_name.includes('Single'))
      }
      if(this.addITAExamModal.setup === 'individual' && this.nonITAExam) {
        return this.examTypes.filter(type  => type.ita_ind === 0)
      }
      if (this.addITAExamModal.setup === 'group') {
        return this.examTypes.filter(type => type.exam_type_name.includes('Group'))
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
      if (!this.addITAExamModal.step1MenuOpen) {
        return 'dropdown-menu'
      }
      if (this.addITAExamModal.step1MenuOpen) {
        return 'dropdown-menu dropdown-menu-right show py-0 my-0 w-100'
      }
    }
  },
  methods: {
    ...mapMutations(['toggleAddITAExamModal', 'toggleNonITAExamModal']),
    clickInput() {
      if (!this.addITAExamModal.step1MenuOpen) {
        this.toggleAddITAExamModal({step1MenuOpen: true})
        return
      }
      this.toggleAddITAExamModal({step1MenuOpen: false})
    },
  },
  template: `
    <b-row no-gutters>
      <b-col class="dropdown">
      <h5 v-if="addITAExamModal.setup === 'group' ">Add Group Exam</h5>
      <h5 v-else-if="addITAExamModal.setup === 'individual' && !this.nonITAExam ">Add Individual ITA Exam</h5>
      <h5 v-else-if="addITAExamModal.setup === 'individual' && this.nonITAExam ">Add Non-ITA Exam</h5>
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
        </b-form-group>
      
      
      </b-col>
    </b-row>
  `
})
