import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Prop, Vue, Watch } from 'vue-property-decorator'
import { mapGetters, mapMutations, mapState } from 'vuex'

import DatePicker from 'vue2-datepicker'
import OfficeDrop from './office-drop.vue'
import moment from 'moment'

// checkmark
@Component({
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
export class checkmark extends Vue {
  @Prop()
  private validated!: any
}

// AddExamCounter
@Component({
  components: {
    checkmark
  },
  computed: {
    ...mapState({
      setup: (state: any) => state.addExamModal.setup,
      candidates: (state: any) => state.addExamModule.candidates
    })

  },
  template: `
  <div>
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
  </div>
`
})
export class AddExamCounter extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  private readonly setup
  private readonly candidates

  @Mutation('captureExamDetail') public captureExamDetail: any
  @Mutation('deleteCapturedExamDetail') public deleteCapturedExamDetail: any

  @Watch('numberOfStudents')
  onNumberOfStudentsChange (newVal: any, oldV: any) {
    if (newVal == this.currentNumber) {
      this.$store.commit('captureExamDetail', { key: 'add_exam_counter', value: 1 })
    } else {
    }
  }

  @Watch('currentNumber')
  onCurrentNumberChange (newVal: any, oldV: any) {
    if (newVal == this.exam.number_of_students) {
      this.$store.commit('captureExamDetail', { key: 'add_exam_counter', value: 1 })
    } else {
    }
  }

  get numberOfStudents () {
    return this.exam.number_of_students
  }

  get currentNumber () {
    if (Array.isArray(this.candidates)) {
      return this.candidates.length
    }
    return 0
  }
}

// DateQuestion
@Component({
  components: {
    checkmark,
    DatePicker
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

export class DateQuestion extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  @Prop()
  private radioChange!: any

  @Prop()
  private today!: any

  private date: any = null

  @State('user') private user!: any
  @State('addExamModal') private addExamModal!: any
  @State('capturedExam') private capturedExam!: any

  selectDate (e) {
    this.handleInput({
      target: {
        name: 'expiry_date',
        value: e
      }
    })
  }

  beforeMount () {
    if (this.exam.ind_or_group === 'group') {
      this.exam.expiry_date = null
    }
  }
}

// DropdownQuestion
@Component({
  components: {
    checkmark
  },
  computed: {
    ...mapState({
      setup: (state: any) => state.addExamModal.setup,
      candidates: (state: any) => state.addExamModule.candidates
    })

  },
  template: `
  <b-row no-gutters>
    <b-row>
      <b-col class="dropdown">
        <h5 v-if="addExamModal.setup === 'group' ">Add Group Exam</h5>
        <h5 v-if="addExamModal.setup === 'individual' ">Add Individual ITA Exam</h5>
        <h5 v-if="addExamModal.setup === 'other' ">Add Non-ITA Exam</h5>
        <h5 v-if="addExamModal.setup === 'pesticide' ">Add Environment Exam</h5>
      </b-col>
      <b-col>
        <label>Exam Type</label><br>
        <div @click="clickInput" id="exam_type_dropdown">
          <b-input read-only
                  autocomplete="off"
                  :value="inputText"
                  placeholder="click here to see options"
                  :style="inputStyle" />
        </div>
      </b-col>
    </b-row
  <b-row>
    <div :class="dropclass"
          style="border: 1px solid grey"
          @click="clickInput">
      <template v-for="type in dropItems">
        <b-dd-header v-if="type.header"
                      :style="{backgroundColor: type.exam_color, listStyleType: 'none'}"
                      :class="type.class">{{ type.exam_type_name }}</b-dd-header>
        <b-dd-item v-else :style="{backgroundColor: type.exam_color, listStyleType: 'none'}"
                    @click="preHandleInput(type.exam_type_id)"
                    :name="type.exam_type_id"
                    autocomplete="off"
                    :id="type.exam_type_id"
                    :class="type.class">{{ type.exam_type_name }}</b-dd-item>
      </template>
    </div>
    </b-row>
  </b-row>
`
})
export class DropdownQuestion extends Vue {
  @Prop()
  private question!: any

  @Prop()
  private exam!: any

  @Prop()
  private exam_object!: any

  @Prop()
  private examTypes!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private selected!: any

  @Prop()
  private message!: any

  @Prop()
  private error!: any

  private clicked: any = false

  @State('addExamModal') private addExamModal!: any
  @State('capturedExam') private capturedExam!: any
  @State('nonITAExam') private nonITAExam!: any

  @Mutation('setAddExamModalSetting') public setAddExamModalSetting: any

  get dropItems () {
    const sorter = (a, b) => {
      const typeA = a.exam_type_name
      const typeB = b.exam_type_name
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
        (type.group_exam_ind === 1 && type.exam_type_name != 'Group Environment Exam')
      )
      return exams.sort((a, b) => sorter(a, b))
    }
    if (this.addExamModal.setup === 'pesticide') {
      const exams = this.examTypes.filter(type =>
        type.pesticide_exam_ind === 1 &&
        type.group_exam_ind === 0)
      return exams.sort((a, b) => sorter(a, b))
    }
  }

  get inputText () {
    if (this.exam_object && this.exam_object.exam_type_name) {
      return this.exam_object.exam_type_name
    }
    return ''
  }

  get inputStyle () {
    if (this.exam_object && this.exam_object.exam_type_name) {
      return { backgroundColor: `${this.exam_object.exam_color}` }
    }
    return ''
  }

  get dropclass () {
    if (!this.addExamModal.step1MenuOpen) {
      return 'dropdown-menu'
    }
    if (this.addExamModal.step1MenuOpen) {
      return 'dropdownmenu dropdown-menu-right show py-0 my-0 w-100'
    }
  }

  clickInput () {
    if (!this.addExamModal.step1MenuOpen) {
      this.setAddExamModalSetting({ step1MenuOpen: true })
      return
    }
    this.setAddExamModalSetting({ step1MenuOpen: false })
  }

  preHandleInput (id) {
    this.handleInput({
      target: {
        name: 'exam_type_id',
        value: id
      }
    })
  }
}

// ExamReceivedQuestion
@Component({
  components: {
    checkmark,
    DatePicker
    // moment
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
export class ExamReceivedQuestion extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  public date: any = null
  public options: any = [
    { text: 'Yes', value: true },
    { text: 'No', value: false }
  ]

  public otherOptions: any = [
    { text: 'No', value: true },
    { text: 'Yes', value: false }
  ]

  @State('addExamModal') private addExamModal!: any
  @State('captureITAExamTabSetup') private captureITAExamTabSetup!: any

  @Mutation('captureExamDetail') public captureExamDetail: any
  @Mutation('toggleIndividualCaptureTabRadio') public toggleIndividualCaptureTabRadio: any

  get showRadio () {
    return this.captureITAExamTabSetup.showRadio
  }

  set showRadio (e) {
    this.captureExamDetail({ key: 'exam_received_date', value: null })
    this.toggleIndividualCaptureTabRadio(e)
  }

  get modalSetup () {
    if (this.addExamModal && this.addExamModal.setup) {
      return this.addExamModal.setup
    }
    return ''
  }

  unsetDate (e) {
    if (!e && this.modalSetup === 'individual') {
      this.handleInput({
        target: {
          name: 'exam_received_date',
          value: null
        }
      })
    }
  }

  preSetDate () {
    if (this.modalSetup === 'other' || this.modalSetup === 'pesticide') {
      this.handleInput({
        target: {
          name: 'exam_received_date',
          value: moment()
        }
      })
    }
  }

  selectRecdDate (e) {
    this.handleInput({
      target: {
        name: 'exam_received_date',
        value: e
      }
    })
  }
}

// InputQuestion

@Component({
  components: {
    checkmark
  },
  computed: {
    ...mapState({
      setup: (state: any) => state.addExamModal.setup
    })

  },
  template: `
  <div v-if="q.key === 'exam_name' && setup === 'challenger'">
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
  </div>
  <div v-else>
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
  </div>
`
})
export class InputQuestion extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  preHandleInput (e) {
    this.handleInput(e)
  }
}

// InputQuestion2

@Component({
  components: {
    checkmark
  },
  computed: {
    ...mapState({
      setup: (state: any) => state.addExamModal.setup
    })
  },
  template: `
    <div>
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
    </div>
  `
})

export class InputQuestion2 extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  public options: any = [
    { text: 'No', value: false },
    { text: 'Yes', value: true }
  ]

  get capture_names () {
    return this.exam.capture_names
  }

  set capture_names (value) {
    this.$store.commit('captureExamDetail', { key: 'capture_names', value })
  }

  preHandleInput (e) {
    this.handleInput(e)
  }
}

// LocationInput

@Component({
  components: {
    checkmark
  },
  computed: {
    ...mapState({
      examTypes: (state: any) => state.examTypes,
      setup: (state: any) => state.addExamModal.setup,
      capturedExam: (state: any) => state.capturedExam,
      booking: (state: any) => state.addExamModule.booking,
      user: (state: any) => state.user
    })

  },
  template: `
    <div>
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
      </div>
  `
})

export class LocationInput extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  @Mutation('toggleScheduling') public toggleScheduling: any
  @Mutation('setAddExamModalSetting') public setAddExamModalSetting: any
  @Mutation('setSelectedExam') public setSelectedExam: any

  private readonly examTypes
  private readonly setup
  private readonly capturedExam
  private readonly booking
  private readonly user

  get showBooking () {
    if (this.booking && Object.keys(this.booking).length > 1) {
      return 'some specifics when possible'
    }
    return 'Not Scheduled'
  }

  get isOffsite () {
    if (this.capturedExam && this.capturedExam.on_or_off) {
      if (this.capturedExam.on_or_off === 'on') {
        return false
      }
      return true
    }
  }

  get invigilator () {
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
  }

  get bookingDetails () {
    if (this.exam.exam_time) {
      const date = moment(this.exam.exam_time).format('ddd MMM Do, YYYY')
      const time = moment(this.exam.exam_time).format('h:mm a')
      const room = this.exam.offsite_location.title
      return `${date} @ ${time} in ${room}`
    }
    return 'Not Yet Scheduled'
  }

  launchSchedule () {
    const { exam_type_id } = this.examTypes.find(t => t.exam_type_name === 'Monthly Session Exam')
    const exam: any = {
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
}

// NotesQuestion
@Component({
  components: {
    checkmark
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
export class NotesQuestion extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  @State('captureITAExamTabSetup') private captureITAExamTabSetup!: any

  @Mutation('updateCaptureTab') public updateCaptureTab: any

  get notes () {
    return this.captureITAExamTabSetup.notes
  }

  handleClick () {
    this.updateCaptureTab({ notes: true })
  }
}

// OffsiteSelect
@Component({
  components: {
    checkmark
  },
  computed: {
    ...mapState({
      setup: (state: any) => state.addExamModal.setup,
      candidates: (state: any) => state.addExamModule.candidates
    }),
    ...mapState({
      booking: (state: any) => state.addExamModal.booking
    })
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
export class OffsiteSelect extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  private readonly booking!: any
  @State('addExamModal') private addExamModal!: any
  @State('capturedExam') private capturedExam!: any
  @State('user') private user!: any

  @Mutation('captureExamDetail') public captureExamDetail: any

  preHandleInput (e) {
    this.handleInput(e)
  }
}

// SelectQuestion

@Component({
  components: {
    checkmark
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
export class SelectQuestion extends Vue {

  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  @State('addExamModal') private addExamModal!: any
  @State('capturedExam') private capturedExam!: any

  @Watch('ind_or_group')
  onInd_or_groupChange (newVal: any, oldVal: any) {
    if (this.addExamModal.setup === 'pesticide' && newVal === 'group') {
      this.$store.commit('captureExamDetail', { key: 'capture_names', value: false })
    }
  }

  get ind_or_group () {
    if (this.capturedExam.ind_or_group) {
      return this.capturedExam.ind_or_group
    }
    return null
  }
}

// SelectOffice

@Component({
  components: {
    checkmark,
    OfficeDrop
  },

  template: `
      <b-row no-gutters class="mb-2">
        <OfficeDrop columnW="9" :office_number="office_number" :setOffice="setOffice" :msg="message" :error="Error" />
        <checkmark :validated="validationObj[q.key].valid"  />
      </b-row>
  `
})
export class SelectOffice extends Vue {
  @State('offices') private offices!: any
  @State('user') private user!: any
  @State('addExamModal') private addExamModal!: any

  @Getter('role_code') private role_code!: any;

  @Mutation('setAddExamModalSetting') public setAddExamModalSetting: any
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  get office_number () {
    return this.addExamModal.office_number
  }

  get Error () {
    if (this.error && this.validationObj.office_id.message) {
      return true
    }
    return false
  }

  get message () {
    if (this.error && this.validationObj.office_id.message) {
      return this.validationObj.office_id.message
    }
    return '(Start typing to search or enter Office #)'
  }

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
}

// TimeQuestion
@Component({
  components: {
    checkmark,
    DatePicker
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
export class TimeQuestion extends Vue {
  @Prop()
  private error!: any

  @Prop()
  private q!: any

  @Prop()
  private validationObj!: any

  @Prop()
  private handleInput!: any

  @Prop()
  private exam!: any

  @Prop()
  private radioChange!: any

  @Prop()
  private today!: any

  private date: any = ''

  @State('user') private user!: any
  @State('addExamModal') private addExamModal!: any
  @State('capturedExam') private capturedExam!: any

  selectTime (e) {
    this.handleInput({
      target: {
        name: 'exam_time',
        value: e
      }
    })
  }
}
