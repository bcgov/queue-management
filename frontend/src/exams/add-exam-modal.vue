<template>
  <b-modal v-model="modalVisible"
           :no-close-on-backdrop="true"
           hide-ok
           hide-header
           hide-cancel
           @shown="initialize"
           @hidden="resetModal"
           size="md">
    <template slot="modal-footer">
      <template v-if="unSubmitted">
        <div v-if="step < lastStep"
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
        <div v-else-if="step == lastStep"
             style="display: flex;
                    justify-content: space-between;
                    width: 100%">
          <div style="display: inline">
            <b-button class="btn-secondary"
                      @click="clickCancel">Cancel</b-button>
          <b-button class="btn-warning"
                    @click="logAnother">Start Again</b-button>
          </div>
          <div style="display: flex">
            <b-button v-if="errors.length > 0"
                      @click="submitMsg='You have an error on a previous step.  Click on the red tab.'"
                      class="btn-primary disabled">Submit</b-button>
            <b-button v-else
                      class="btn-primary"
                      @click="submit">Submit</b-button>
          </div>
        </div>
      </template>
      <template v-if="!unSubmitted">
        <div style="display: flex; justify-content: flex-start">
          <b-button class="btn-secondary"
                    @click="clickCancel">Close</b-button>
        </div>
      </template>
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
    <template v-if="unSubmitted">
      <AddExamFormController v-if="step <= (lastStep - 1)"  />
      <AddExamFormConfirm v-if="step==lastStep" :submitMsg="submitMsg" />
    </template>
    <template v-if="!unSubmitted">
      <div v-if="status==='unknown' "
           class="loader" style="margin-top: auto"></div>
      <div v-if="status==='success'">
        <b-container>
          <b-row align-v="center"
                 align-h="center"
                 align-content="center">
            <b-col>
              <p><h5>Success.  Exam Details Added.</h5></p>
              <p><b-button @click="logAnother" class="btn-primary">Log Another Exam</b-button></p>
            </b-col>
          </b-row>
        </b-container>
      </div>
      <div v-if="status==='failed'">
        <b-container>
          <b-row align-v="center"
                 align-h="center"
                 align-content="center">
            <b-col>
              <p class="message-text">Something Went Wrong</p>
              <p><b-button @click="tryAgain">Try Again</b-button></p>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </template>
  </b-modal>
</template>

<script>
  import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
  import AddExamFormController from './add-exam-form-controller'
  import AddExamFormConfirm from './add-exam-form-confirm'
  import moment from 'moment'

  export default {
    name: 'AddExamModal',
    components: { AddExamFormController, AddExamFormConfirm },
    mounted() {
      this.captureExamDetail({key: 'exam_received_date', value: null})
    },
    data() {
      return ({
        submitMsg: '',
        unSubmitted: true,
        status: 'unknown',
      })
    },
    computed: {
      ...mapGetters({
        steps: 'add_modal_steps',
        button: 'add_exam_modal_navigation_buttons',
      }),
      ...mapState({
        exam: 'capturedExam',
        examTypes: 'examTypes',
        addExamModal: 'addExamModal',
        tab: 'captureITAExamTabSetup',
        user: 'user',
        module: 'addExamModule',
        addGroupSteps: state => state.addExamModule.addGroupSteps,
        addChallengerSteps: state => state.addExamModule.addChallengerSteps,
        addIndividualSteps: state => state.addExamModule.addIndividualSteps,
        addOtherSteps: state => state.addExamModule.addOtherSteps,
        addPesticideSteps: state => state.addExamModule.addPesticideSteps,
        capturtedAddModal: state => state.addExamModule.addExamModal,
      }),
      lastStep() {
        if (this.addExamModal.setup === 'challenger') {
          return 3
        }
        return 4
      },
      errors() {
        if (this.tab.errors) {
          return this.tab.errors
        } else {
          this.submitMsg = ''
          return []
        }
      },
      modalVisible: {
        get() {
          return this.addExamModal.visible
        },
        set(e) {
          this.toggleAddExamModal(e)
        }
      },
      step() {
        if (this.tab && this.tab.step) {
          return this.tab.step
        }
        return 1
      },
      tabs() {
        if (this.steps && Array.isArray(this.steps)) {
          return this.steps.slice(0, this.tab.highestStep)
        }
      },
    },
    methods: {
      ...mapActions(['clickAddExamSubmit', 'getExams', 'wipeAll']),
      ...mapMutations(['captureExamDetail', 'resetCaptureForm', 'resetCaptureTab', 'toggleAddExamModal', 'updateCaptureTab', ]),
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
        if (this.validated().indexOf(i) === -1) {
          return false
        }
        return true
      },
      logAnother() {
        this.wipeAll()
        this.resetModal()
        this.initialize()
      },
      clickBack() {
        let step = this.step - 1
        this.updateCaptureTab({step})
      },
      clickCancel() {
        this.resetModal()
        this.wipeAll()
        this.toggleAddExamModal({visible: false, setup: null, step1MenuOpen: false})
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
      initialize() {
        this.captureExamDetail({key:'notes', value: ''})
        this.captureExamDetail({key: 'exam_method', value: 'paper'})
        this.unSubmitted = true
        this.submitMsg = ''
        this.status = 'unknown'
        let { setup } = this.addExamModal
        if (setup === 'challenger') {
          if (this.module.booking && this.module.booking.start) {
            this.captureExamDetail({ key: 'offsite_location', value: this.module.booking.resource})
            this.captureExamDetail({ key: 'exam_time', value: this.module.booking.start})
            this.captureExamDetail({ key: 'expiry_date', value: this.module.booking.start})
            setTimeout( () => { this.$root.$emit('validateform') }, 300)
          }
          if (this.module.addExamModal &&
              Object.keys(this.module.addExamModal).length > 0) {
            return
          }
          this.captureExamDetail({ key: 'on_or_off', value: 'off'})
        }
        if (setup == 'individual') {
          let d = new Date()
          let today = moment(d).format('YYYY-MM-DD')
          this.captureExamDetail({ key: 'exam_received_date', value: today })
          let value = moment().add(90, 'd')
          this.captureExamDetail({ key: 'expiry_date', value })
        }
        if (setup === 'group') {
          let { office_id, office_number } = this.user.office
          office_id = parseInt(office_id)
          office_number = parseInt(office_number)
          this.captureExamDetail({key: 'office_id', value: office_id })
          this.toggleAddExamModal({ office_number })
        }
        if (setup === 'other') {
          let value = moment().add(60, 'd')
          this.captureExamDetail({ key: 'expiry_date', value })
        }
        if (setup === 'pesticide') {
          let value = moment().add(60, 'd')
          this.captureExamDetail({ key: 'expiry_date', value })
        }

      },
      tryAgain() {
        this.unSubmitted = true
        this.status = 'unknown'
      },
      submit() {
        let { setup } = this.addExamModal
        this.unSubmitted = false
        this.submitMsg = ''
        if (setup === 'group') {
          this.clickAddExamSubmit(setup).then( resp => {
            this.status = resp
            this.getExams()
          }).catch( error => {
            this.status = error
            this.getExams()
          })
        }
        if (setup === 'challenger') {
          this.clickAddExamSubmit(setup).then( resp => {
            this.status = resp
            this.getExams()
          }).catch( error => {
            this.status = error
            this.getExams()
          })
        }
        if (setup === 'individual' || setup === 'other' || setup === 'pesticide') {
          this.clickAddExamSubmit('individual').then( resp => {
            this.status = resp
            this.getExams()
          }).catch( error => {
            this.status = error
            this.getExams()
          })
        }
      },
      resetModal() {
        if (this.addExamModal.setup !== 'challenger') {
          this.resetCaptureForm()
          this.resetCaptureTab()
          return
        }
        if (this.capturtedAddModal && Object.keys(this.capturtedAddModal).length > 0) {
          return
        }
        this.resetCaptureForm()
        this.resetCaptureTab()
      },
      setWarning() {
        if (!this.errors.includes(this.step)) {
          let errors = this.errors.concat([this.step])
          this.updateCaptureTab({errors})
        }
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
    }
  }
</script>

<style>
  .message-text {
    font-size: .9rem; font-weight: 500
  }
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
  .loader {
    position: relative;
    text-align: center;
    margin: 15px auto 35px auto;
    z-index: 9999;
    display: block;
    width: 80px;
    height: 80px;
    border: 10px solid rgba(0, 0, 0, .3);
    border-radius: 50%;
    border-top-color: #000;
    animation: spin 1s ease-in-out infinite;
    -webkit-animation: spin 1s ease-in-out infinite;
  }
  @keyframes spin {
    to {
      -webkit-transform: rotate(360deg);
    }
  }

  @-webkit-keyframes spin {
    to {
      -webkit-transform: rotate(360deg);
    }
  }

</style>
