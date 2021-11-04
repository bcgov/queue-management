<template>
  <b-form id="capture-ind-ita-form" autocomplete="off">
    <div v-for="q in questions" :key="q.key">
      <AddExamCounter
        v-if="q.kind === 'add_exam_counter'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <DropdownQuestion
        v-if="q.kind === 'dropdown'"
        :question="q"
        :exam="exam"
        :exam_object="exam_object"
        :examTypes="examTypes"
        :message="validationObj[q.key].message"
        :error="error"
        :handleInput="handleInput"
      />
      <InputQuestion
        v-if="q.kind === 'input'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <InputQuestion2
        v-if="
          q.kind === 'number_of_students' && addExamModal.setup === 'pesticide'
        "
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <LocationInput
        v-if="q.kind === 'locationInput'"
        v-show="addExamModal.setup != 'other' || q.key != 'event_id'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <OffsiteSelect
        v-if="q.kind === 'offsiteSelect'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <SelectQuestion
        v-if="q.kind === 'select'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <GroupPesticideModal
        v-if="q.kind === 'group_exam_types'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <PesticideFees
        v-if="q.kind === 'pesticideFees'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <SelectOffice
        v-if="q.kind === 'office'"
        v-show="is_ita2_designate || is_pesticide_designate"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <ExamReceivedQuestion
        v-if="q.kind === 'exam_received'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
      <DateQuestion
        v-if="q.kind === 'date'"
        :error="error"
        v-show="addExamModal.setup !== 'challenger' || exam.on_or_off === 'off'"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
        :id="q.key"
      />
      <TimeQuestion
        v-if="q.kind === 'time'"
        v-show="addExamModal.setup !== 'challenger' || exam.on_or_off === 'off'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
        :id="q.key"
      />
      <NotesQuestion
        v-if="q.kind === 'notes'"
        :error="error"
        :q="q"
        :validationObj="validationObj"
        :handleInput="handleInput"
        :exam="exam"
      />
    </div>
  </b-form>
</template>

<script lang="ts">

import { Action, Getter, Mutation } from 'vuex-class'
import {
  AddExamCounter,
  DateQuestion,
  DropdownQuestion,
  ExamReceivedQuestion,
  InputQuestion,
  InputQuestion2,
  LocationInput,
  NotesQuestion,
  OffsiteSelect,
  SelectOffice,
  SelectQuestion,
  TimeQuestion,
  checkmark
} from './add-exam-form-components'

import { Component, Vue, Watch } from 'vue-property-decorator'

import GroupPesticideModal from './form-components/group-pesticide-modal.vue'
import PesticideFees from './form-components/pesticide-fees.vue'

import { mapState } from 'vuex'

@Component({
  components: {
    PesticideFees,
    AddExamCounter,
    checkmark,
    DateQuestion,
    DropdownQuestion,
    ExamReceivedQuestion,
    GroupPesticideModal,
    InputQuestion,
    LocationInput,
    InputQuestion2,
    NotesQuestion,
    OffsiteSelect,
    SelectOffice,
    SelectQuestion,
    TimeQuestion
  },
  computed: {

    ...mapState({
      exam: (state: any) => state.capturedExam,
      event_ids: (state: any) => state.event_ids,
      event_id_warning: (state: any) => state.event_id_warning,
      addExamModal: (state: any) => state.addExamModal,
      addGroupSteps: (state: any) => state.addExamModule.addGroupSteps,
      addChallengerSteps: (state: any) => state.addExamModule.addChallengerSteps,
      addIndividualSteps: (state: any) => state.addExamModule.addIndividualSteps,
      addOtherSteps: (state: any) => state.addExamModule.addOtherSteps,
      tab: (state: any) => state.captureITAExamTabSetup,
      // JSTOTS -changed variable name
      examTypesState: (state: any) => state.examTypes,
      user: (state: any) => state.user
    })
  }
})
export default class AddExamFormController extends Vue {
  @Getter('add_modal_steps') private steps!: any;
  @Getter('exam_object') private exam_object!: any;
  @Getter('role_code') private role_code!: any;
  @Getter('is_pesticide_designate') private is_pesticide_designate!: any;
  @Getter('is_ita2_designate') private is_ita2_designate!: any;
  @Getter('addPesticideSteps') private addPesticideSteps!: any;

  @Action('getExamTypes') public getExamTypes: any
  @Action('getExamEventIDs') public getExamEventIDs: any
  @Action('getOffices') public getOffices: any

  @Mutation('captureExamDetail') public captureExamDetail: any
  @Mutation('updateCaptureTab') public updateCaptureTab: any
  @Mutation('setEventWarning') public setEventWarning: any

  @Watch('step')
  onstepChange (newV: any, oldV: any) {
    this.$nextTick(function () {
      this.validate()
    })
  }

  @Watch('validationObj')
  onValidationObjChange () {
    // calling validate() with every change in validationObj() is untested with any workflow except 'pesticide',
    // and other workflows don't seem to require this additional step, so limiting this call to fire only when
    this.validate()
    this.$nextTick(function () {
      this.validate()
    })
  }

  private readonly exam!: any
  private readonly event_ids!: any
  private readonly event_id_warning!: any
  private readonly addExamModal!: any
  private readonly addGroupSteps!: any
  private readonly addChallengerSteps!: any
  private readonly addIndividualSteps!: any
  private readonly addOtherSteps!: any
  private readonly tab!: any
  // JSTOTS -changed variable name
  private readonly examTypesState!: any
  private readonly user!: any

  public notes: any = false
  public selectOptions: any = [
    { text: 'online', value: 'online' },
    { text: 'paper', value: 'paper' }
  ]

  event_form_validation: boolean = false

  get error () {
    if (this.errors.includes(this.step)) {
      return true
    }
    return false
  }

  get ind_or_group () {
    if (this.exam) {
      return this.exam.ind_or_group
    }
    return null
  }

  get errors () {
    if (this.tab && this.tab.errors) {
      return this.tab.errors
    }
    return []
  }

  get examTypes () {
    if (this.$store.state.examTypes) {
      return this.$store.state.examTypes
    }
    return {
      exam_type_id: '',
      exam_type_colour: '',
      exam_type_name: ''
    }
  }

  get questions () {
    if (this.steps && this.steps.length > 0) {
      return this.steps.find(q => q.step == this.step).questions
    }
    return []
  }

  get step () {
    if (this.tab && this.tab.step) {
      return this.tab.step
    }
    return 1
  }

  get stepErrors () {
    const keys = Object.keys(this.validationObj)
    const checklist = keys.map(key => this.validationObj[key].valid)
    if (checklist.includes(false)) {
      return true
    } else {
      return false
    }
  }

  get validationObj () {
    const valid: any = {}
    const messages: any = {}
    const validateAnswer = (question) => {
      const key = question.key
      let answer = this.exam[key]
      if (key === 'notes') {
        valid[key] = true
        messages[key] = ''
        return
      }
      // TODO Turn this on for event ID checks only on group exams. Add && group_exam_indicator to the if block
      // below as well
      if (key === 'event_id' && answer && answer.length >= 4) {
        if (this.event_id_warning) {
          valid.event_id = true
          messages.event_id = 'Event ID already in Use'
          // Should handle next button bug
          this.tab.stepsValidated = [1, 2]
          this.setError()
          return
        }
        if ((document.activeElement as any).id === 'event_id') {
          this.getExamEventIDs(answer)
        }
        if (this.event_ids === false) {
          valid.event_id = true
          messages.event_id = ''
          // Should handle next button bug
          this.tab.stepsValidated = [1, 2]
          return
        }
        valid.event_id = false
        messages.event_id = 'Event ID already in Use'
        // Should handle next button bug
        this.tab.stepsValidated = [1]
        return
      }
      if (key === 'exam_name' && answer && answer.length > 50) {
        valid.exam_name = false
        messages.exam_name = 'Maximum Field Length Exceeded'
        return
      }
      if (key === 'office_id' && answer == null) {
        valid[key] = false
        messages[key] = 'Invalid Office'
        return
      }
      if (answer) {
        answer = answer.toString()
        if (question.minLength > 0) {
          if (answer.length >= question.minLength) {
            if (question.digit) {
              answer = parseInt(answer)
              if (!isNaN(answer)) {
                valid[key] = true
                messages[key] = ''
                return
              }
              if (isNaN(answer)) {
                valid[key] = false
                messages[key] = 'Response must be a NUMBER'
                return
              }
            }
            if (!question.digit) {
              valid[key] = true
              messages[key] = ''
              return
            }
          }
          if (answer.length < question.minLength) {
            valid[key] = false
            messages[key] = 'Response is too short'
            return
          }
        }
        if (question.minLength == 0) {
          if (question.digit) {
            answer = parseInt(answer)
            if (!isNaN(answer)) {
              valid[key] = true
              messages[key] = ''
              return
            }
            if (isNaN(answer)) {
              valid[key] = false
              messages[key] = 'Response must be a NUMBER'
              return
            }
          }
          if (!question.digit) {
            valid[key] = true
            messages[key] = ''
            return
          }
        }
        valid[key] = false
        messages[key] = 'Required Field'
        return
      }
      if (question.minLength == 0 && !question.digit) {
        valid[key] = true
        messages[key] = ''
        return
      }
      valid[key] = false
      messages[key] = 'Required Field'
    }
    this.questions.forEach(question => {
      validateAnswer(question)
    })
    const output = {}
    const validKeys = Object.keys(valid)
    validKeys.forEach(key => {
      (output[key] = {
        message: messages[key],
        valid: valid[key]
      })
    })
    return output
  }

  handleInput (e) {
    const payload = {
      key: e.target.name,
      value: e.target.value
    }
    this.captureExamDetail(payload)
    this.$nextTick(function () {
      this.validate()
    })
  }

  removeError () {
    if (this.error) {
      const i = this.errors.indexOf(this.step)
      const errors = this.errors
      errors.splice(i, 1)
      this.updateCaptureTab({ errors })
    }
  }

  setError () {
    if (!this.error) {
      const errors = this.errors.concat([this.step])
      this.updateCaptureTab({ errors })
    }
  }

  validate () {
    if (!this.stepErrors) {
      this.removeError()
      if (this.tab.stepsValidated.indexOf(this.step) === -1) {
        const validated = this.tab.stepsValidated
        const stepsValidated = validated.concat([this.step])
        this.updateCaptureTab({ stepsValidated })
      }
    } else if (this.stepErrors) {
      if (!this.error) {
        if (this.tab.highestStep > this.step) {
          this.setError()
        }
      }
      if (this.tab.stepsValidated.indexOf(this.step) != -1) {
        const stepsValidated = Object.assign([], this.tab.stepsValidated)
        stepsValidated.splice(this.tab.stepsValidated.indexOf(this.step), 1)
        this.updateCaptureTab({ stepsValidated })
      }
    }
  }

  mounted () {
    this.event_form_validation = false
    this.getExamTypes()
    this.getOffices()
    this.$root.$on('validateform', () => {
      this.validate()
    })
  }
}
</script>

<style scoped>
.confirm-item {
  font-size: 1rem;
  font-weight: 500;
}
.confirm-header {
  font-size: 0.8rem;
  font-weight: 600;
}
.red {
  color: red;
}
</style>
