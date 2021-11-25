<template>
  <div id="serveModal" class="serve-modal">
    <div class="serve-modal-content">
      <div id="navi">
        <template v-if="showServeCitizenSpinner">
          <div class="q-loader2"></div>
        </template>
      </div>
      <b-alert
        :show="this.alertMessage != ''"
        style="justify-content: center"
        variant="warning"
        >{{ this.alertMessage }}</b-alert
      >
      <div class="modal_header" v-dragged="onDrag">
        <div>
          <h4 style="font-weight: 900; color: #6e6e6e">
            {{ simplifiedModal ? 'TheQ Time Tracking' : 'Serve Citizen' }}
          </h4>
        </div>
        <div>
          <button class="btn btn-link" @click="toggleFeedback">Feedback</button>
          <button
            class="btn btn-link"
            style="margin-left: 20px"
            @click="toggleMinimize"
          >
            {{ minimizeWindow ? 'Maximize' : 'Minimize' }}
          </button>
        </div>
      </div>
      <template v-if="!simplifiedModal">
        <b-container id="serve-citizen-modal-top" fluid v-if="!minimizeWindow">
          <b-row no-gutters class="p-2">
            <b-col col cols="4">
              <div v-if="appointment">
                <strong>{{ citizen.citizen_name }}</strong>
              </div>
              <div>
                <h6>
                  Ticket #:
                  <strong>{{ citizen.ticket_number }}</strong>
                </h6>
              </div>
              <div>
                <h6>
                  Channel:
                  <strong>{{ channel.channel_name }}</strong>
                </h6>
              </div>
              <div>
                <h6>
                  Created At:
                  <strong>{{ formatTime(citizen.start_time) }}</strong>
                </h6>
              </div>
            </b-col>
            <b-col cols="auto" class="ml-3 mr-2">
              <h6>Comments:</h6>
            </b-col>
            <b-col col cols="*" style="text-align: left" class="pr-2">
              <div>
                <b-textarea
                  id="serve_comment_textarea"
                  v-model="comments"
                  :rows="4"
                  :maxlength="1000"
                  size="sm"
                />
              </div>
            </b-col>
          </b-row>
        </b-container>
        <b-container
          id="serve-top-buttons-container"
          :style="{ top: topSpace }"
          :class="
            appointment
              ? 'serve-top-buttons-container-2'
              : 'serve-top-buttons-container'
          "
          v-if="!minimizeWindow"
        >
          <div>
            <b-button
              @click="clickServiceBeginService"
              v-if="reception"
              :disabled="
                serviceBegun === true || performingAction || commentsTooLong
              "
              v-bind:class="buttonStyle"
              style="margin-right: 8px; opacity: 1"
              id="serve-citizen-begin-service-button"
              >Begin Service</b-button
            >
            <b-button
              @click="clickReturnToQueue"
              v-if="reception"
              :disabled="performingAction || commentsTooLong"
              class="btn serve-btn"
              id="serve-citizen-return-to-queue-button"
              >Return to Queue</b-button
            >
             <b-button
              @click="clickUnCheckIn"
              v-if="appointmentsEnabled && appointment"
              :disabled="performingAction || commentsTooLong"
              class="btn serve-btn"
              id="serve-citizen-uncheckin-button"
              style="margin-left: 8px;"
              >Return to Calendar</b-button
            >
          </div>
          <div>
            <b-button
              @click="clickCitizenLeft"
              :disabled="performingAction || commentsTooLong"
              class="btn-danger serve-btn"
              v-if="reception"
              id="serve-citizen-citizen-left-button"
              >Citizen Left</b-button
            >
          </div>
        </b-container>
      </template>
      <ServeCitizenTable v-if="!minimizeWindow" />
      <template v-if="!simplifiedModal && !minimizeWindow">
        <b-container
          fluid
          id="serve-light-inner-container"
          class="pt-3 pb-2"
          v-if="!minimizeWindow"
        >
          <b-row no-gutters>
            <b-col cols="7" />
            <b-col cols="auto" style="text-align: right">
              <select
                id="counter-selection-serve"
                v-show="reception && !simplifiedModal"
                class="custom-select"
                v-model="counter_selection"
              >
                <option
                  v-for="counter in user.office.counters"
                  :value="counter.counter_id"
                  :key="counter.counter_id"
                >
                  {{ counter.counter_name }}
                </option>
              </select>
              <select
                id="priority-selection"
                class="custom-select px-1"
                v-model="priority_selection"
                style="margin-right: 8px"
              >
                <option value="1">High Priority</option>
                <option value="2">Default Priority</option>
                <option value="3">Low Priority</option>
              </select>
              <b-button
                class="btn-primary serve-btn"
                @click="clickAddService"
                :disabled="
                  serviceBegun === false || performingAction || commentsTooLong
                "
                >Add Next Service</b-button
              >
            </b-col>
            <b-col cols="2" />
          </b-row>
        </b-container>

        <div v-if="!minimizeWindow">
          <b-container fluid id="serve-citizen-modal-footer">
            <div
              style="display: flex; flex-direction: column; margin-left: 10px"
            >
              <b-form-checkbox
                v-model="accurate_time_ind"
                v-if="serviceBegun === true"
                value="0"
                style="color: white; margin: 0 0 8px"
                unchecked-value="1"
              >
                <span style="font: 400 16px Myriad-Pro, sans-serif">Inaccurate Time</span>
              </b-form-checkbox>
              <b-button
                @click="clickServiceFinish"
                :disabled="
                  serviceBegun === false || performingAction || commentsTooLong
                "
                class="btn-success serve-btn"
                id="serve-citizen-finish-button"
                >Finish</b-button
              >
            </div>
            <b-button
              @click="clickHold"
              :disabled="
                serviceBegun === false || performingAction || commentsTooLong
              "
              class="btn-warning serve-btn"
              id="serve-citizen-place-on-hold-button"
              >Place on Hold</b-button
            >
          </b-container>
        </div>
      </template>
      <template v-if="simplifiedModal && !minimizeWindow">
        <b-container class="serve-citizen-modal-footer" fluid>
          <b-row no-gutters class="w-100" align-h="end">
            <b-col cols="auto">
              <b-button
                class="btn-primary serve-btn"
                v-if="
                  !simplifiedModal ||
                  (simplifiedModal && simplifiedTicketStarted)
                "
                @click="clickAddService"
                >Add Next Service</b-button
              >
            </b-col>
          </b-row>
          <b-row no-gutters class="mt-3" align-h="end">
            <b-col cols="auto">
              <b-button
                @click="clickSimplifiedFinish"
                style="width: 100px"
                class="serve-btn"
                :variant="simplifiedTicketStarted ? 'warning' : 'success'"
                id="serve-citizen-finish-button"
                >{{ simplifiedTicketStarted ? 'Finish' : 'Begin' }}</b-button
              >
              <b-button
                @click="clickContinue"
                style="width: 100px"
                class="serve-btn ml-2"
                :variant="simplifiedTicketStarted ? 'success' : 'danger'"
                id="serve-citizen-finish-button"
                >{{
                  simplifiedModal && !simplifiedTicketStarted
                    ? 'Cancel'
                    : 'Continue'
                }}</b-button
              >
            </b-col>
          </b-row>
        </b-container>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'
import ServeCitizenTable from './serve-citizen-table.vue'

@Component({
  components: {
    ServeCitizenTable
  }
})
export default class ServeCitizen extends Vue {
  @State('performingAction') private performingAction!: any
  @State('showServiceModal') private showServiceModal!: any
  @State('showServeCitizenSpinner') private showServeCitizenSpinner!: any
  @State('serviceBegun') private serviceBegun!: any
  @State('serviceModalForm') private serviceModalForm!: any
  @State('serveModalAlert') private serveModalAlert!: any
  @State('user') private user!: any

  @Getter('invited_citizen') private invited_citizen!: any;
  @Getter('active_service') private active_service!: any;
  @Getter('invited_service_reqs') private invited_service_reqs!: any;
  @Getter('reception') private reception!: any;

  @Action('clickAddCitizen') public clickAddCitizen: any
  @Action('clickAddService') public clickAddService: any
  @Action('clickCitizenLeft') public clickCitizenLeft: any
  @Action('clickHold') public clickHold: any
  @Action('clickReturnToQueue') public clickReturnToQueue: any
  @Action('clickServiceBeginService') public clickServiceBeginService: any
  @Action('clickServiceFinish') public clickServiceFinish: any
  @Action('clickUnCheckIn') public clickUnCheckIn: any
  @Action('screenAllCitizens') public screenAllCitizens: any
  @Action('setServeModalAlert') public setServeModalAlert: any

  @Mutation('editServiceModalForm') public editServiceModalForm: any
  @Mutation('toggleFeedbackModal') public toggleFeedbackModal: any
  @Mutation('toggleServiceModal') public toggleServiceModal: any
  @Mutation('toggleExamsTrackingIP') public toggleExamsTrackingIP: any
  @Mutation('toggleTimeTrackingIcon') public toggleTimeTrackingIcon: any

  private buttonStyle: string = 'btn-primary serve-btn'
  private selected: string = ''
  private f: boolean = false
  private t: boolean = true
  private checked: any = null
  private showCitizenWarning: boolean = false
  private minimizeWindow: boolean = false
  private dragged: boolean = false
  private left: number = 0
  private top: number = 0

  get appointment () {
    if (this.serviceModalForm &&
      this.serviceModalForm.citizen_comments &&
      this.serviceModalForm.citizen_comments.includes('|||')) {
      return true
    }
    return false
  }

  get appointmentsEnabled () {
    if (this.user && this.user.office) {
      return this.user.office.appointments_enabled_ind
    }
    return false
  }

  get alertMessage () {
    const serveMessageBlank = this.serveModalAlert === ''
    const commentsMessageBlank = this.commentsAlert === ''
    if (serveMessageBlank && commentsMessageBlank) {
      return ''
    }
    if (serveMessageBlank && !commentsMessageBlank) {
      return this.commentsAlert
    }
    if ((!serveMessageBlank) && commentsMessageBlank) {
      return this.serveModalAlert
    }
    return this.serveModalAlert + '  ' + this.commentsAlert
  }

  get topSpace () {
    let top = this.appointment ? 210 : 178
    if (this.alertMessage != '') {
      top = top + 60
    }
    return top.toString() + 'px'
  }

  get simplifiedModal () {
    if (this.$route.path !== '/queue') {
      return true
    }
    return false
  }

  get simplifiedTicketStarted () {
    if (this.$route.path !== '/queue') {
      if (this.serviceModalForm.citizen_id) {
        return true
      }
    }
    return false
  }

  get citizen () {
    if (!this.invited_citizen) {
      return { ticket_number: '' }
    }
    return this.invited_citizen
  }

  get commentsTooLong () {
    if ((this.serviceModalForm) && (this.serviceModalForm.citizen_comments)) { return this.serviceModalForm.citizen_comments.length > 1000 } else { return false }
  }

  get commentsAlert () {
    return this.commentsTooLong ? 'You have entered more than the 1,000 characters allowed for comments.' : ''
  }

  get comments () {
    if (this.appointment) {
      return this.serviceModalForm.citizen_comments.split('|||')[1].valueOf()
    }
    return this.serviceModalForm.citizen_comments
  }

  set comments (value) {
    if (this.appointment) {
      const time = this.serviceModalForm.citizen_comments.split('|||')[0]
      const prependedValue = `${time}|||${value}`
      this.editServiceModalForm({
        type: 'citizen_comments',
        value: prependedValue
      })
    } else {
      this.editServiceModalForm({
        type: 'citizen_comments',
        value
      })
    }
  }

  get accurate_time_ind () {
    return this.serviceModalForm.accurate_time_ind
  }

  set accurate_time_ind (value) {
    this.editServiceModalForm({
      type: 'accurate_time_ind',
      value
    })
  }

  get channel () {
    if (!this.active_service) {
      return { channel_name: '', channel_id: '' }
    }
    return this.active_service.channel
  }

  get priority_selection () {
    return this.serviceModalForm.priority
  }

  set priority_selection (value) {
    this.editServiceModalForm({ type: 'priority', value })
  }

  get counter_selection () { return this.serviceModalForm.counter }
  set counter_selection (value) {
    this.editServiceModalForm({ type: 'counter', value })
  }

  // methods
  private formatTime (data: any) {
    const date = new Date(data)
    return date.toLocaleTimeString()
  }

  private clickSimplifiedFinish () {
    if (this.simplifiedTicketStarted) {
      this.toggleExamsTrackingIP(false)
      this.clickServiceFinish()
      return
    }
    this.toggleExamsTrackingIP(true)
    this.toggleServiceModal(false)
    this.clickAddCitizen()
  }

  private clickContinue () {
    this.toggleExamsTrackingIP(true)
    this.toggleServiceModal(false)
  }

  private toggleFeedback () {
    this.toggleFeedbackModal(true)
  }

  private toggleMinimize () {
    if (this.$route.path === '/queue' && !this.serviceBegun) {
      this.minimizeWindow = !this.minimizeWindow
      return
    }
    this.toggleExamsTrackingIP(true)
    this.toggleServiceModal(false)
    this.toggleTimeTrackingIcon(true)
  }

  private flashButton () {
    if (this.serviceBegun === false) {
      this.buttonStyle == 'btn-primary serve-btn'
        ? this.buttonStyle = 'btn-highlighted' : this.buttonStyle = 'btn-primary serve-btn'
    }
    if (this.serviceBegun === true) {
      this.buttonStyle = 'btn-primary serve-btn'
    }
  }

  private closeWindow () {
    this.$store.dispatch('clickServiceModalClose')
  }

  private onDrag (event: any) {
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

    const serve_modal: any = document.getElementsByClassName('serve-modal-content')[0]
    serve_modal.style.transform = 'translate(' + this.left + 'px,' + this.top + 'px)'
  }

  updated () {
    if (!this.citizen && this.citizen.ticket_number === '') {
      this.$store.commit('toggleServeCitizenSpinner', true)
      this.screenAllCitizens(this.$route).then(() => {
        this.$store.commit('toggleServeCitizenSpinner', false)
      })
    }
    setTimeout(() => {
      if (!this.citizen && this.citizen.ticket_number === '') {
        this.setServeModalAlert('An error occurred loading citizen, please try refreshing the page.')
      }
    }, 1000)
  }

  mounted () {
    setInterval(() => { this.flashButton() }, 800)
    this.toggleTimeTrackingIcon(false)
  }
}

</script>

<style scoped>
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
#navi {
  position: relative;
}
.q-loader2 {
  position: absolute;
  z-index: 1100;
  text-align: center;
  margin: 250px auto auto 450px;
  width: 50px;
  height: 50px;
  border: 10px solid LightGrey;
  opacity: 0.9;
  border-radius: 50%;
  border-top-color: DodgerBlue;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}
.serve-modal {
  position: fixed;
  z-index: 1040;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.4);
  transition: display 1s;
}
.modal_header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 20px 20px 4px;
  cursor: grab;
}
.serve-modal-content {
  background-color: #fefefe;
  margin-right: auto;
  margin-left: auto;
  margin-top: 1%;
  width: 80%;
  max-width: 900px;
  position: relative;
}
#serve-citizen-modal-top {
  background-color: #f0f0f0;
  color: #6e6e6e;
  padding-bottom: 20px;
}
.serve-top-buttons-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  position: absolute;
  top: 178px;
  z-index: 99;
  width: 100%;
  max-width: 100%;
}
.serve-top-buttons-container-2 {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  position: absolute;
  top: 210px;
  z-index: 99;
  width: 100%;
  max-width: 100%;
}
#serve-light-inner-container {
  background: #504e4f;
  display: flex;
  flex-direction: row-reverse;
}
.serve-citizen-modal-footer {
  background: #504e4f;
  padding-top: 30px;
  padding-bottom: 25px;
}
#serve-citizen-modal-footer {
  background: #504e4f;
  display: flex;
  flex-direction: row-reverse;
  align-items: flex-end;
  padding-top: 30px;
  padding-bottom: 25px;
}
#serve-citizen-modal-footer .btn {
  width: 140px;
}
.btn-highlighted {
  color: black;
  border: 1px solid darkgoldenrod;
  background-color: gold;
}
strong {
  font-size: 1.35rem;
}
.custom-select {
  line-height: 25px;
}
#serve-citizen-return-to-queue-button {
  background: white;
  color: black;
  border: 1px solid #cecece;
}
#serve-citizen-return-to-queue-button:hover {
  background: #e8e8e8;
}

button:disabled {
  cursor: not-allowed !important;
}
</style>
