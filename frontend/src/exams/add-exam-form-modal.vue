<template>
  <b-modal v-model="modal"
           :no-close-on-backdrop="true"
           hide-ok
           hide-header
           hide-cancel
           @hidden="resetModal"
           size="md">
    <template slot="modal-footer">
      <div v-if="step < 4"
           style="width: 100%;
                  display: flex;
                  justify-content: space-between">
        <div>
          <b-button @click="clickCancel">Cancel</b-button>
        </div>
        <div style="display: inline">
          <b-button v-if="step > 1"
                    class="btn-secondary mr-2"
                    @click="clickBack">Back</b-button>
          <b-button v-if="button.nextDisabled"
                    :class="button.nextClass"
                    @click="setWarning">Next</b-button>
          <b-button v-else
                    :class="button.nextClass"
                    @click="clickNext">Next</b-button>
        </div>
      </div>
      <div v-else-if="step == 4"
           style="display: flex;
                  justify-content: space-between;
                  width: 100%">
        <div style="display: inline">
          <b-button class="btn-secondary"
                    @click="clickCancel">Cancel</b-button>
        <b-button class="btn-warning"
                  @click="resetModal">Start Again</b-button>
        </div>
        <div style="display: flex">
          <b-button v-if="errors.length > 0"
                    @click="submitMsg='You have an error on a previous step.  Click on the red tab.'"
                    class="btn-primary disabled">Submit</b-button>
          <b-button v-else
                    class="btn-primary">Submit</b-button>
        </div>
      </div>
    </template>

    <b-nav tabs class="mb-3">
      <b-nav-item v-for="i in tabs"
                  :key="'tab '+i.title"
                  :active="tabs[step-1].title==i.title"
                  @click="clickTab(i.step)">
        <span :style="tabWarning(i)">{{ i.title }}
        <font-awesome-icon v-if="tabValidate(i.step)"
                           icon="check"
                           class="m-0 p-0"
                           style="font-size: .8rem; color: green"/>
        </span>
      </b-nav-item>
    </b-nav>
    <AddExamFormController v-if="step <= 3"  />
    <AddExamFormConfirm v-if="step==4" :submitMsg="submitMsg" />
  </b-modal>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import AddExamFormController from './add-exam-form-controller'
  import AddExamFormConfirm from './add-exam-form-confirm'

  export default {
    name: 'AddExamFormModal',
    components: { AddExamFormController, AddExamFormConfirm },
    data() {
      return {
        submitMsg: ''
      }
    },
    computed: {
      ...mapGetters({
        button: 'addIndividualITAButton',
      }),
      ...mapState({
        exam: state => state.capturedExam,
        examTypes: state => state.examTypes,
        modalVisible: state => state.addIndividualITAExamModalVisibe,
        steps: state => state.addIndividualITAsteps,
        tab: state => state.captureITAExamTabSetup,
      }),
      errors() {
        if (this.tab.errors) {
          return this.tab.errors
        } else {
          this.submitMsg = ''
          return []
        }
      },
      modal: {
        get() {
          return this.modalVisible
        },
        set(e) {
          this.toggleAddIndividualITAExam(e)
        }
      },
      step() {
        if (this.tab && this.tab.step) {
          return this.tab.step
        }
        return 1
      },
      tabs() {
        return this.steps.slice(0, this.tab.highestStep)
      },
      validated() {
        if (this.tab && this.tab.stepsValidated) {
          if (Array.isArray(this.tab.stepsValidated)) {
            return this.tab.stepsValidated
          }
          return [this.tab.stepsValidated]
        }
        return []
      },
    },
    methods: {
      ...mapActions(['postExam']),
      ...mapMutations([
        'resetCaptureForm',
        'resetCaptureTab',
        'toggleAddIndividualITAExam',
        'updateCaptureTab',
      ]),
      tabWarning(i) {
        if (!Array.isArray(this.errors)) return ''
        if (this.errors.length > 0) {
          let list = []
            this.errors.forEach(error=>{
              if (this.steps.some(step=>step.step==error)) {
                list.push(this.steps.find(step=>step.step==error)).questions
              }

            })
          if (list.includes(i)) {
            return {color: 'red'}
          }
          return ''
        }
        return ''
      },
      tabValidate(i) {
        if (this.validated.indexOf(i) === -1) {
          return false
        }
        return true
      },
      clickBack() {
        let step = this.step - 1
        this.updateCaptureTab({step})
      },
      clickCancel() {
        this.toggleAddIndividualITAExam(false)
      },

      clickNext() {
        let step = this.step + 1
        this.updateCaptureTab({step})

        if (step > this.tab.highestStep) {
          this.updateCaptureTab({highestStep: step})
        }
      },

      clickTab(e) {
        this.updateCaptureTab({step: e})
      },

      resetModal() {
        this.resetCaptureForm()
        this.resetCaptureTab()
      },

      setWarning() {
        if (!this.errors.includes(this.step)) {
          let errors = this.errors.concat([this.step])
          this.updateCaptureTab({errors})
        }
      },

    }
  }
</script>

<style>
  .tab-title-font {
    font-size: .8rem
  }
  .buttontabs {
    border-radius: 0 !important;
    border-bottom: 1px solid black;
    border-top: none;
    border-right: none;
    border-left: none;
  }

</style>
