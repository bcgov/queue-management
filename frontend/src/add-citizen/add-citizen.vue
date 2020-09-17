<template>
  <b-modal
    :visible="showAddModal"
    v-if="showAddModal"
    :size="simplified ? 'lg' : 'lg'"
    hide-header
    hide-footer
    no-close-on-backdrop
    no-close-on-esc
    body-class="q-modal-body"
    class="m-0 p-0"
    @shown="setupForm()"
  >
    <div class="modal_header div-top-cont" v-dragged="onDrag">
      <div>
        <h4>{{modalTitle}}</h4>
      </div>
      <div>
        <button
          class="btn btn-link"
          style="margin-left: 20px"
          @click="toggleMinimize"
        >{{ minimizeWindow ? "Maximize" : "Minimize" }}</button>
      </div>
    </div>
    <b-alert
      :show="dismissCountDown"
      style="h-align: center"
      variant="danger"
      @dismissed="dismissCountDown=0"
      @dismiss-count-down="countDownChanged"
    >{{this.$store.state.alertMessage}}</b-alert>
    <div v-if="!minimizeWindow">
      <div v-if="!this.addModalForm.citizen && !this.addModalForm.setup === 'add_mode'">
        <div class="q-loader2" />
      </div>
      <div v-else>
        <AddCitizenForm />
        <b-container class="add-buttons add_citizen_padding">
          <div
            v-bind:class="{'button-row-reversed' : citizenButtons, 'button-row' : !citizenButtons }"
            style="padding-bottom:6px;"
          >
            <select
              v-show="reception && !simplified"
              id="counter-selection-add"
              class="custom-select"
              v-model="counter_selection"
            >
              <option
                v-for="counter in sortedCounters"
                :value="counter.counter_id"
                :key="counter.counter_id"
              >{{counter.counter_name}}</option>
            </select>
            <div id="select-wrapper">
              <select
                id="priority-selection"
                v-if="!simplified"
                class="custom-select"
                v-model="priority_selection"
              >
                <option value="1">High Priority</option>
                <option value="2">Default Priority</option>
                <option value="3">Low Priority</option>
              </select>
            </div>
            <!--  Cancel button goes here. -->
            <b-button
              @click="cancelAction"
              :disabled="performingAction"
              class="btn-danger"
              v-bind:style="marginStyle"
              id="add-citizen-cancel"
            >Cancel</b-button>
          </div>
          <div class="button-row">
            <Buttons />
          </div>
        </b-container>
      </div>
    </div>
  </b-modal>
</template>

<script>
/* eslint-disable */
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'
import Buttons from './form-components/buttons'
import AddCitizenForm from './add-citizen-form'

export default {
  name: 'AddCitizen',
  components: {
    AddCitizenForm,
    Buttons
  },
  mounted () {
    this.$root.$on('showAddMessage', () => {
      this.Alert()
    })
  },
  data () {
    return {
      dismissSecs: 5,
      dismissCountDown: 0,
      minimizeWindow: false
    }
  },
  computed: {
    ...mapState({
      addCitizenModal: 'addCitizenModal',
      addModalForm: 'addModalForm',
      showAddModal: 'showAddModal',
      addModalSetup: 'addModalSetup',
      serviceModalForm: 'serviceModalForm',
      user: 'user',
      displayServices: 'displayServices',
      citizenButtons: 'citizenButtons',
      performingAction: 'performingAction'
    }),
    ...mapGetters(['form_data', 'reception']),
    marginStyle () {
      let style = ''
      if (this.citizenButtons) {
        style = { marginRight: '50%' }
      } else {
        style = { marginLeft: '50%' }
      }
      return style
    },
    simplified () {
      if (this.$route.path !== '/queue') {
        return true
      }
      return false
    },
    modalTitle () {
      if (this.addModalSetup === 'edit_mode') {
        return 'Edit Service'
      }
      if (this.$route.path === '/appointments') {
        return 'Add a Service'
      }
      if (this.simplified) {
        return 'Begin Tracking'
      }
      if (this.displayServices === 'BackOffice') {
        return 'Back Office'
      }
      return 'Add Citizen'
    },

    counter_selection: {
      get () {
        return this.form_data.counter
      },
      set (value) {
        this.updateAddModalForm({ type: 'counter', value })
      }
    },
    priority_selection: {
      get () {
        return this.form_data.priority
      },
      set (value) {
        this.updateAddModalForm({ type: 'priority', value })
      }
    },
    sortedCounters () {
      var sorted = this.user.office.counters.sort((a, b) => {
        return a.counter_name > b.counter_name
      })
      return sorted
    }
  },
  methods: {
    ...mapActions(['cancelAddCitizensModal', 'cancelAddCitizensModal',
      'clickEditCancel', 'resetAddCitizenModal']),
    ...mapMutations(['setDefaultChannel', 'toggleAddModal', 'updateAddModalForm']),
    Alert () {
      this.dismissCountDown = this.dismissSecs
    },
    cancelAction () {
      if (this.$route.path == '/exams') {
        this.cancelAddCitizensModal()
      } else if (this.$route.path == '/appointments') {
        this.closeAddServiceModal()
      } else if ((this.addModalSetup == 'reception') || (this.addModalSetup == 'non_reception')) {
        this.cancelAddCitizensModal()
      } else if (this.addModalSetup == 'add_mode') {
        this.clickEditCancel()
      } else if (this.addModalSetup == 'edit_mode') {
        this.clickEditCancel()
      } else {
        this.cancelAddCitizensModal()
      }
    },
    closeAddServiceModal () {
      this.resetAddCitizenModal()
      this.$store.commit('appointmentsModule/toggleApptBookingModal', true)
    },
    countDownChanged (dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    onDrag ({ el, deltaX, deltaY, offsetX, offsetY, clientX, clientY, first, last }) {
      if (first) {
        this.dragged = true
        return
      }
      if (last) {
        this.dragged = false
        return
      }
      this.left = (this.left || 0) + deltaX
      this.top = (this.top || 0) + deltaY
      var add_modal = document.getElementsByClassName('modal-content')[0]
      add_modal.style.transform = 'translate(' + this.left + 'px,' + this.top + 'px)'
    },
    setupForm () {
      const setup = this.addModalSetup
      if (this.simplified) {
        this.$root.$emit('focusfilter')
        return
      }
      if (setup === 'add_mode' || setup === 'edit_mode') {
        this.$root.$emit('focusfilter')
      } else {
        if (!this.reception) {
          this.$root.$emit('focusfilter')
        } else if (this.reception) {
          this.$root.$emit('focuscomments')
        }
      }
    },
    toggleMinimize () {
      this.minimizeWindow = !this.minimizeWindow
    }
  }
}
</script>

<style>
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.q-loader2 {
  position: absolute;
  text-align: center;
  margin: 50px auto auto 300px;
  width: 50px;
  height: 50px;
  border: 10px solid LightGrey;
  opacity: 0.9;
  border-radius: 50%;
  border-top-color: DodgerBlue;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}
.modal_header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 10px 20px 1px;
  cursor: grab;
}

.add-buttons {
  background: #504e4f;
  padding: 5px 15px 20px;
}

.div-top-cont {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.button-row-reversed {
  background: #504e4f;
  display: flex;
  flex-direction: row-reverse;
}
.button-row {
  background: #504e4f;
  display: flex;
}
</style>
