

<template>
  <div id="serveModal" class="serve-modal">
    <div class="serve-modal-content">
      <template v-if="showServeCitizenSpinner">
        <div class="q-loader" />
      </template>
      <template v-else>
        <b-alert :show="this.serveModalAlert != ''"
                  style="h-align: center"
                  variant="warning">{{this.serveModalAlert}}</b-alert>
        <div class="modal_header" v-dragged="onDrag">
          <div>
            <h4 style="font-weight:900; color:#6e6e6e">
              {{ simplifiedModal ? 'Exams Time Tracking' : 'Serve Citizen' }}</h4>
          </div>
          <div>
            <button class="btn btn-link"
                    @click="toggleFeedback">Feedback</button>
            <button class="btn btn-link"
                    style="margin-left: 20px"
                    @click="toggleMinimize">{{ minimizeWindow ? "Maximize" : "Minimize" }}</button>
          </div>
        </div>
        <template v-if="!simplifiedModal">
          <b-container id="serve-citizen-modal-top" fluid v-if="!minimizeWindow">
            <b-row no-gutters class="p-2">
              <b-col col cols="4">
                <div><h6>Ticket #: <strong>{{citizen.ticket_number}}</strong></h6></div>
                <div><h6>Channel: <strong>{{channel.channel_name}}</strong></h6></div>
                <div><h6>Created At: <strong>{{formatTime(citizen.start_time)}}</strong></h6></div>
              </b-col>
              <b-col cols="auto" class="ml-3 mr-2">
                <h6>Comments:</h6>
              </b-col>
              <b-col col cols="*" style="text-align: left" class="pr-2">
                <div>
                  <b-textarea id="serve_comment_textarea"
                              v-model="comments"
                              :rows="4"
                              size="sm" />
                </div>
              </b-col>
            </b-row>
          </b-container>
          <b-container id="serve-top-buttons-container" v-if="!minimizeWindow">
            <div>
              <b-button @click="clickServiceBeginService"
                      v-if="reception"
                      :disabled="serviceBegun===true || performingAction"
                      v-bind:class="buttonStyle"
                      style="margin-right:8px; opacity:1"
                      id="serve-citizen-begin-service-button">Begin Service</b-button>
              <b-button @click="clickReturnToQueue"
                      v-if="reception"
                      :disabled="performingAction"
                      class="btn serve-btn"
                      id="serve-citizen-return-to-queue-button">Return to Queue</b-button>
            </div>
            <div>
              <b-button @click="clickCitizenLeft"
                      :disabled="performingAction"
                      class="btn-danger serve-btn"
                      v-if="reception"
                      id="serve-citizen-citizen-left-button">Citizen Left</b-button>
            </div>
          </b-container>
        </template>
        <ServeCitizenTable v-if="!minimizeWindow"/>
        <template v-if="!simplifiedModal && !minimizeWindow">
          <b-container fluid
                   id="serve-light-inner-container"
                   class="pt-3 pb-2"
                    v-if="!minimizeWindow">
        <b-row no-gutters>
          <b-col cols="7" />
          <b-col cols="auto" style="align: right">
            <select id="counter-selection" v-show="reception && !simplifiedModal" class="custom-select" v-model="counter_selection">
              <option v-for="counter in user.office.counters"
                    :value="counter.counter_id"
                    :key="counter.counter_id">
                {{counter.counter_name}}
              </option>
            </select>
            <select id="priority-selection" class="custom-select px-1" v-model="priority_selection" style="margin-right:8px;">
                <option value=1>High Priority</option>
                <option value=2>Default Priority</option>
                <option value=3>Low Priority</option>
            </select>
            <b-button class="btn-primary serve-btn"
                      @click="clickAddService"
                      :disabled="serviceBegun===false || performingAction">Add Next Service</b-button>
          </b-col>
          <b-col cols="2" />
        </b-row>
      </b-container>

          <div v-if="!minimizeWindow">
            <b-container fluid
                         id="serve-citizen-modal-footer">
                    <div style="display:flex; flex-direction:column; margin-left:10px;">
                        <b-form-checkbox v-model="accurate_time_ind"
                                                        v-if="serviceBegun===true"
                                                        value="0"
                                                        style="color:white; margin:0 0 8px;"
                                                        unchecked-value="1">
                                        <span  style="font: 400 16px Myriad-Pro;">Inaccurate Time</span>
                                        </b-form-checkbox>
                        <b-button @click="clickServiceFinish"
                                :disabled="serviceBegun===false || performingAction"
                                class="btn-success serve-btn"
                                id="serve-citizen-finish-button">Finish</b-button>
                    </div>
                  <b-button @click="clickHold"
                            :disabled="serviceBegun===false || performingAction"
                            class="btn-warning serve-btn"
                            id="serve-citizen-place-on-hold-button">Place on Hold</b-button>
            </b-container>
          </div>
        </template>
        <template v-if="simplifiedModal && !minimizeWindow">
          <b-container class="serve-citizen-modal-footer" fluid>

            <b-row no-gutters class="w-100" align-h="end">
              <b-col cols="auto">
                <b-button class="btn-primary serve-btn"
                          v-if="!simplifiedModal || (simplifiedModal && simplifiedTicketStarted)"
                          @click="clickAddService">Add Next Service</b-button>
              </b-col>
            </b-row>
            <b-row no-gutters
                   class="mt-3"
                   align-h="end">
              <b-col cols="auto">
                <b-button @click="clickSimplifiedFinish"
                          style="width: 100px;"
                          class="serve-btn"
                          :variant="simplifiedTicketStarted ? 'warning' : 'success'"
                          id="serve-citizen-finish-button">
                  {{ simplifiedTicketStarted ? 'Finish' : 'Begin'}}</b-button>
                <b-button @click="clickContinue"
                          style="width: 100px;"
                          class="serve-btn ml-2"
                          :variant="simplifiedTicketStarted ? 'success' : 'danger'"
                          id="serve-citizen-finish-button">
                  {{simplifiedModal && !simplifiedTicketStarted ? 'Cancel' : 'Continue'}}</b-button>
              </b-col>
            </b-row>
          </b-container>
        </template>
      </template>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions, mapMutations } from 'vuex'
import ServeCitizenTable from './serve-citizen-table'

export default {
  name: 'ServeCitizen',
  components: {
    ServeCitizenTable
  },
  mounted() {
    setInterval( () => { this.flashButton() }, 800)
    this.toggleTimeTrackingIcon(false)
  },
  data() {
    return {
      buttonStyle: 'btn-primary serve-btn',
      selected: '',
      f: false,
      t: true,
      checked: null,
      showCitizenWarning: false,
      minimizeWindow: false
    }
  },
  updated() {
    if (!this.citizen && this.citizen.ticket_number === "") {
      this.$store.commit('toggleServeCitizenSpinner', true)
      console.log("Screen All Citizens")
      this.screenAllCitizens(this.$route).then(() => {
        this.$store.commit('toggleServeCitizenSpinner', false)
      })
    }
    setTimeout( () => {
      if (!this.citizen && this.citizen.ticket_number === "") {
        this.setServeModalAlert("An error occurred loading citizen, please try refreshing the page.")
      }
    }, 1000)
  },
  computed: {
    ...mapState([
      'performingAction',
      'showServiceModal',
      'showServeCitizenSpinner',
      'serviceBegun',
      'serviceModalForm',
      'serveModalAlert',
      'user'
    ]),
    ...mapGetters({
      invited_citizen: 'invited_citizen',
      active_service: 'active_service',
      invited_service_reqs: 'invited_service_reqs',
      reception: 'reception',
    }),
    simplifiedModal() {
      if (this.$route.path !== '/queue') {
        return true
      }
      return false
    },
    simplifiedTicketStarted() {
      if (this.$route.path !== '/queue') {
        if (this.serviceModalForm.citizen_id) {
          return true
        }
      }
      return false
    },
    citizen() {
      if (!this.invited_citizen) {
        return {ticket_number: ''}
      }
      return this.invited_citizen
    },
    comments: {
      get() {
        return this.serviceModalForm.citizen_comments
      },
      set(value) {
        this.editServiceModalForm({
          type: 'citizen_comments',
          value
        })
      }
    },
    accurate_time_ind: {
      get() {
        return this.serviceModalForm.accurate_time_ind
      },
      set(value) {
        this.editServiceModalForm({
          type: 'accurate_time_ind',
          value
        })
      }
    },
    channel() {
      if (!this.active_service) {
        return {channel_name: '', channel_id: ''}
      }
      return this.active_service.channel
    },
    priority_selection: {
      get() { return this.serviceModalForm.priority },
      set(value) {
        this.editServiceModalForm({type:'priority',value})
      }
    },
    counter_selection: {
      get() { return this.serviceModalForm.counter },
      set(value) {
        this.editServiceModalForm({ type: "counter", value })
      }
    },
  },

  methods: {
    ...mapActions([
      'clickAddCitizen',
      'clickAddService',
      'clickCitizenLeft',
      'clickHold',
      'clickReturnToQueue',
      'clickServiceBeginService',
      'clickServiceFinish',
      'screenAllCitizens',
      'setServeModalAlert',
    ]),
    ...mapMutations([
      'editServiceModalForm',
      'toggleFeedbackModal',
      'toggleServiceModal',
      'toggleExamsTrackingIP',
      'toggleTimeTrackingIcon',///
    ]),
    formatTime(data) {
      let date = new Date(data)
      return date.toLocaleTimeString()
    },
    clickSimplifiedFinish() {
      if (this.simplifiedTicketStarted) {
        this.toggleExamsTrackingIP(false)
        this.clickServiceFinish()
        return
      }
      this.toggleExamsTrackingIP(true)
      this.toggleServiceModal(false)
      this.clickAddCitizen()
    },
    clickContinue() {
      this.toggleExamsTrackingIP(true)
      this.toggleServiceModal(false)
    },
    toggleFeedback() {
      this.toggleFeedbackModal(true)
    },
    toggleMinimize() {
      if (this.$route.path === '/queue' && !this.serviceBegun) {
        this.minimizeWindow = !this.minimizeWindow
        return
      }
      this.toggleServiceModal(false)
      this.toggleTimeTrackingIcon(true)
    },
    flashButton() {
      if (this.serviceBegun === false) {
        this.buttonStyle == 'btn-primary serve-btn' ?
          this.buttonStyle = 'btn-highlighted' : this.buttonStyle = 'btn-primary serve-btn'
      }
      if (this.serviceBegun === true) {
        this.buttonStyle = 'btn-primary serve-btn'
      }
    },
    closeWindow() {
      this.$store.dispatch('clickServiceModalClose')
    },
    onDrag({ el, deltaX, deltaY, offsetX, offsetY, clientX, clientY, first, last }) {
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

      var serve_modal = document.getElementsByClassName('serve-modal-content')[0]
      serve_modal.style.transform = "translate("+this.left+"px,"+this.top+"px)"
    }
  }
}

</script>

<style scoped>
.serve-modal {
  position: fixed;
  z-index: 1040;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
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
 background-color: #F0F0F0;
 color: #6e6e6e;
 padding-bottom: 20px;
}
#serve-top-buttons-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    position: absolute;
    top: 178px;
    z-index: 99;
    width: 100%;
    max-width: 100%;
}
#serve-light-inner-container{
    background: #504E4F;
    display: flex;
    flex-direction: row-reverse;
}
.serve-citizen-modal-footer {
  background: #504E4F;
  padding-top: 30px;
  padding-bottom: 25px;
}
#serve-citizen-modal-footer {
    background: #504E4F;
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
</style>
