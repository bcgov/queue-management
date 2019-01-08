import Vue from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { mapMutations, mapState } from 'vuex'

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

export const ExamReceivedQuestion = Vue.component('exam-received-question', {
  props: ['error', 'q', 'validationObj', 'handleInput', 'exam',],
  components: { checkmark },
  data() {
    return {
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
          <b-input type="date"
                   :value="exam[q.key]"
                   :key="q.key"
                   :name="q.key"
                   @input.native="handleInput" />
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
    ...mapMutations(['captureExamDetail', 'toggleIndividualCaptureTabRadio'])
  }
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
  components: { checkmark },
  template: `
    <b-row no-gutters >
      <b-col cols="6">
        <b-form-group>
          <label>Expiry Date
            <span v-if="error" style="color: red">{{ validationObj[q.key].message }}</span>
          </label>
          <b-form-input :value="exam[q.key]"
                        :name="q.key"
                        type="date"
                        @input.native="handleInput" />
        </b-form-group>
      </b-col>
      <b-col cols="5" />
      <checkmark :validated="validationObj[q.key].valid" />
    </b-row>
  `
})

export const DropdownQuestion = Vue.component('dropdown-question',{
  props: ['question', 'exam_object', 'examTypes', 'handleInput', 'selected', 'message', 'error'],
  components: { checkmark },
  template: `
    <b-row no-gutters>
      <b-col>
        <b-form-group>
          <label>{{ question.text }}
            <span v-if="error" style="color: red">{{ message }}</span>
          </label><br>
          <b-input-group>
            <b-input-group-addon>
              <b-dropdown>
                <template v-for="type in examTypes">
                  <b-dd-header v-if="type.header"
                               :style="{backgroundColor: type.exam_color}"
                               :class="type.class">{{ type.exam_type_name }}</b-dd-header>
                  <b-dd-item v-else :style="{backgroundColor: type.exam_color}"
                             @click="handleInput"
                             :name="type.exam_type_id"
                             :id="type.exam_type_id"
                             :class="type.class">{{ type.exam_type_name }}</b-dd-item>
                </template>
              </b-dropdown>
            </b-input-group-addon>
            <b-input :value="exam_object.exam_type_name"
                     class="w-75"
                     disabled
                     :style="{backgroundColor: exam_object.exam_color}"/>
          </b-input-group>
        </b-form-group>
      </b-col>
    </b-row>
  `
})
