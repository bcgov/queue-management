<template>
  <b-form id="capture-ind-ita-form">
    <div v-for="q in questions" :key="q.key">
      <DropdownQuestion v-if="q.kind==='dropdown'"
                        :question="q"
                        :exam="exam"
                        :exam_object="exam_object"
                        :examTypes="examTypes"
                        :message="validationObj[q.key].message"
                        :error="error"
                        :handleInput="handleInput" />
      <InputQuestion v-if="q.kind==='input'"
                     :error="error"
                     :q="q"
                     :validationObj="validationObj"
                     :handleInput="handleInput"
                     :exam="exam" />
      <SelectQuestion v-if="q.kind==='select'"
                      :error="error"
                      :q="q"
                      :validationObj="validationObj"
                      :handleInput="handleInput"
                      :exam="exam" />
      <SelectOffice v-if="q.kind==='office'"
                      :error="error"
                      :q="q"
                      :validationObj="validationObj"
                      :handleInput="handleInput"
                      :exam="exam" />
      <ExamReceivedQuestion v-if="q.kind==='exam_received'"
                            :error="error"
                            :q="q"
                            :validationObj="validationObj"
                            :handleInput="handleInput"
                            :exam="exam" />
      <DateQuestion v-if="q.kind==='date'"
                    :error="error"
                    :q="q"
                    :validationObj="validationObj"
                    :handleInput="handleInput"
                    :exam="exam" />
      <TimeQuestion v-if="q.kind==='time'"
                    :error="error"
                    :q="q"
                    :validationObj="validationObj"
                    :handleInput="handleInput"
                    :exam="exam" />
      <NotesQuestion v-if="q.kind==='notes'"
                     :error="error"
                     :q="q"
                     :validationObj="validationObj"
                     :handleInput="handleInput"
                     :exam="exam" />
    </div>
  </b-form>
</template>

<script>
  import { mapState, mapMutations, mapGetters, mapActions } from 'vuex'
  import {
    checkmark,
    DateQuestion,
    TimeQuestion,
    DropdownQuestion,
    ExamReceivedQuestion,
    InputQuestion,
    NotesQuestion,
    SelectQuestion,
    SelectOffice
  } from './add-exam-form-components.js'
  import moment from 'moment'

  export default {
    name: "AddExamFormController",
    components: {
      checkmark,
      DateQuestion,
      DropdownQuestion,
      ExamReceivedQuestion,
      InputQuestion,
      TimeQuestion,
      NotesQuestion,
      SelectQuestion,
      SelectOffice
    },
    mounted() {
      this.getExamTypes()
      this.getOffices()
    },
    data() {
      return {
        notes: false,
        selectOptions: [
          {text: 'online', value: 'online'},
          {text: 'paper', value: 'paper'}
        ],
      }
    },
    computed: {
      ...mapGetters(['exam_object']),
      ...mapState({
        exam: state => state.capturedExam,
        addITAExamModal: state => state.addITAExamModal,
        addGroupITASteps: state => state.addGroupITASteps,
        addIndITASteps: state => state.addIndITASteps,
        tab: state => state.captureITAExamTabSetup,
        examTypes: state => state.examTypes,
        user: state => state.user,
      }),
      error() {
        if (this.errors.includes(this.step)) {
          return true
        } else {
          return false
        }
      },
      errors() {
        if (this.tab && this.tab.errors) {
          return this.tab.errors
        }
        return []
      },
      examTypes() {
        if (this.$store.state.examTypes) {
          return this.$store.state.examTypes
        }
        return {
          exam_type_id: '',
          exam_type_colour: '',
          exam_type_name: ''
        }
      },
      questions() {
        return this.steps.find(q => q.step == this.step).questions
      },
      step() {
        if (this.tab && this.tab.step) {
          return this.tab.step
        }
        return 1
      },
      steps() {
        if (this.addITAExamModal.setup === "group") {
          return this.addGroupITASteps
        } else {
          return this.addIndITASteps
        }
      },
      stepErrors() {
        let keys = Object.keys(this.validationObj)
        let checklist = keys.map(key => this.validationObj[key].valid)
        if (checklist.includes(false)) {
          return true
        } else {
          return false
        }
      },
      validationObj() {
        let valid = {}
        let messages = {}
        let validateAnswer = question => {
          let key = question.key
          let answer = this.exam[key]
          if (key === 'notes') {
            valid[key] = true
            messages[key] = ''
            return
          }
          if (answer) {
            if (question.minLength > 0) {
              if (answer.length >= question.minLength) {
                if (question.digit) {
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
            if (question.minLength === 0) {
              if (question.digit) {
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
          } else {
            valid[key] = false
            messages[key] = 'Required Field'
            return
          }
        }
        this.questions.forEach(question => {
          validateAnswer(question)
        })
        let output = {}
        let validKeys = Object.keys(valid)
        validKeys.forEach(key => {
          (output[key] = {
            message: messages[key],
            valid: valid[key],
          })
        })
        return output
      },
    },
    methods: {
      ...mapMutations([
        'captureExamDetail',
        'updateCaptureTab'
      ]),
      ...mapActions(['getExamTypes', 'getOffices']),
      handleInput(e) {
        let payload = {
          key: e.target.name,
          value: e.target.value,
        }
        if (this.step === 1) {
          payload.key = 'exam_type_id'
          payload.value = e.target.id
        }
        this.captureExamDetail(payload)
        this.validate()
      },
      removeError() {
        if (this.error) {
          let i = this.errors.indexOf(this.step)
          let errors = this.errors
          errors.splice(i, 1)
          this.updateCaptureTab({errors})
        }
      },
      setError() {
        if (!this.error) {
          let errors = this.errors.concat([this.step])
          this.updateCaptureTab({errors})
        }
      },
      validate() {
        if (!this.stepErrors) {
          this.removeError()
          if (this.tab.stepsValidated.indexOf(this.step)===-1) {
            let validated = this.tab.stepsValidated
            let stepsValidated = validated.concat([this.step])
            this.updateCaptureTab({stepsValidated})
          }
        } else if (this.stepErrors) {
          if (!this.error) {
            if (this.tab.highestStep > this.step) {
              this.setError()
            }
          }
          if (this.tab.stepsValidated.indexOf(this.step) != -1) {
            let stepsValidated = Object.assign([], this.tab.stepsValidated)
            stepsValidated.splice(this.tab.stepsValidated.indexOf(this.step), 1)
            this.updateCaptureTab({stepsValidated})
          }
        }
      }
    }
  }
</script>

<style scoped>
  .confirm-item {
    font-size:1rem;
    font-weight: 500
  }
  .confirm-header {
    font-size:.8rem;
    font-weight:600
  }
  .red {
    color: red;
  }
</style>
