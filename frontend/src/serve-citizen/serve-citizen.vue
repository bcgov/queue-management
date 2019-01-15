

<template>
  <div id="serveModal" class="serve-modal">
    <div class="serve-modal-content">
      <b-alert :show="this.serveModalAlert != ''"
                style="h-align: center"
                variant="warning">{{this.serveModalAlert}}</b-alert>
      <div class="modal_header" v-dragged="onDrag">
        <div>
          <h4 style="font-weight:900; color:#6e6e6e">Serve Citizen</h4>
        </div>
        <div>
          <button
                    class="btn btn-link"
                    @click="toggleFeedback">Feedback</button>
          <button
                    class="btn btn-link"
                    style="margin-left: 20px"
                    @click="toggleMinimize">{{ minimizeWindow ? "Maximize" : "Minimize" }}</button>
        </div>
      </div>
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
      <ServeCitizenTable v-if="!minimizeWindow"/>
      <b-container fluid
                   id="serve-light-inner-container"
                   class="pt-3 pb-2"
                    v-if="!minimizeWindow">
        <b-row no-gutters>
          <b-col cols="7" />
          <b-col cols="auto" style="align: right">
            <b-form-checkbox v-model="quick" value="1" unchecked-value="0" v-if="reception"
                            class="quick-checkbox" style="color:white;margin-right: 8px;">
                <span style="font: 400 16px Myriad-Pro;">Quick Txn</span>
                <span class="quick-span" v-if="quick"></span> <!-- For puppeteer testing to see if quick is selected -->
            </b-form-checkbox>
            <select id="priority-selection" class="custom-select" v-model="priority_selection" style="margin-right:8px;">
                <option value=1>High Priority</option>
                <option value=2>Default Priority</option>
                <option value=3>Low Priority</option>
            </select>
            <b-button class="btn-primary serve-btn"
                      @click="clickAddService"
                      :disabled="serviceBegun===false || performingAction"
                      >Add Next Service</b-button>
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
      console.log("Screen All Citizens")
      this.screenAllCitizens()
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
      'serviceBegun',
      'serviceModalForm',
      'serveModalAlert'
    ]),
    ...mapGetters(['invited_citizen', 'active_service', 'invited_service_reqs', 'reception']),
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
    quick: {
      get() { return this.serviceModalForm.quick },
      set(value) {
        this.editServiceModalForm({type:'quick',value})
      }
    },
    priority_selection: {
      get() { return this.serviceModalForm.priority },
      set(value) {
        this.editServiceModalForm({type:'priority',value})
      }
    }
  },

  methods: {
    ...mapActions([
      'clickCitizenLeft',
      'clickServiceBeginService',
      'clickServiceFinish',
      'clickReturnToQueue',
      'clickHold',
      'clickAddService',
      'screenAllCitizens',
      'setServeModalAlert'
    ]),
    ...mapMutations(['editServiceModalForm', 'toggleFeedbackModal']),
    formatTime(data) {
      let date = new Date(data)
      return date.toLocaleTimeString()
    },
    toggleFeedback() {
      this.toggleFeedbackModal(true)
    },
    toggleMinimize() {
      this.minimizeWindow = !this.minimizeWindow
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
#priority-selection {
    display: inline-block;
    width: 135px;
    padding-right: 0;
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
