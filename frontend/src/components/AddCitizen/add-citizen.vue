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
      style="justify-content: center"
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

<script lang="ts">
/* eslint-disable */
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'
import AddCitizenForm from './add-citizen-form.vue'
import Buttons from './form-components/buttons.vue'

@Component({
  components: {
    AddCitizenForm,
    Buttons
  }
})
export default class AddCitizen extends Vue {
  @State('addCitizenModal') private addCitizenModal!: string | undefined
  @State('addModalForm') private addModalForm!: string | undefined
  @State('showAddModal') private showAddModal!: string | undefined
  @State('addModalSetup') private addModalSetup!: string | undefined
  @State('serviceModalForm') private serviceModalForm!: string | undefined
  @State('user') private user!: any
  @State('displayServices') private displayServices!: string | undefined
  @State('citizenButtons') private citizenButtons!: string | undefined
  @State('performingAction') private performingAction!: string | undefined

  @Getter('form_data') private form_data!: any;
  @Getter('reception') private reception!: any;

  @Action('cancelAddCitizensModal') public cancelAddCitizensModal: any
  @Action('clickEditCancel') public clickEditCancel: any
  @Action('resetAddCitizenModal') public resetAddCitizenModal: any
  // @Action('cancelAddCitizensModal') public cancelAddCitizensModal: any

  @Mutation('setDefaultChannel') public setDefaultChannel: any
  @Mutation('toggleAddModal') public toggleAddModal: any
  @Mutation('updateAddModalForm') public updateAddModalForm: any

  private dismissSecs: number = 5;
  private dismissCountDown: number = 0;
  private minimizeWindow: boolean = false;
  private dragged: boolean = false
  private left: number = 0
  private top: number = 0

  Alert () {
    this.dismissCountDown = this.dismissSecs
  }

  get marginStyle () {
    let style = {}
    if (this.citizenButtons) {
      style = { marginRight: '50%' }
    } else {
      style = { marginLeft: '50%' }
    }
    return style
  }

  get simplified () {
    if (this.$route.path !== '/queue') {
      return true
    }
    return false
  }

  get modalTitle () {
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
  }

  get counter_selection () {
    return this.form_data.counter
  }

  set counter_selection (value: string) {
    this.updateAddModalForm({ type: 'counter', value })
  }

  get priority_selection () {
    return this.form_data.priority
  }

  set priority_selection (value) {
    this.updateAddModalForm({ type: 'priority', value })
  }

  get sortedCounters () {
    // eslint-disable-next-line
    var sorted = this.user.office.counters.sort((a: { counter_name: number }, b: { counter_name: number }) => {
      return a.counter_name > b.counter_name
    })
    return sorted
  }

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
  }

  closeAddServiceModal () {
    this.resetAddCitizenModal()
    this.$store.commit('appointmentsModule/toggleApptBookingModal', true)
  }

  countDownChanged (dismissCountDown: number) {
    this.dismissCountDown = dismissCountDown
  }

  onDrag (event: any) {
    const { el, deltaX, deltaY, offsetX, offsetY, clientX, clientY, first, last } = event
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
    const add_modal: any = document.getElementsByClassName('modal-content')[0]
    add_modal.style.transform = 'translate(' + this.left + 'px,' + this.top + 'px)'
  }

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
  }

  toggleMinimize () {
    this.minimizeWindow = !this.minimizeWindow
  }

  mounted () {
    this.$root.$on('showAddMessage', () => {
      this.Alert()
    })
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
