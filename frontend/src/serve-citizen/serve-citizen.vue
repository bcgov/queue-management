

<template>
    <b-modal id="serve_citizen_modal"
             :visible="showServiceModal"
             size="lg"
             hide-header
             hide-footer
             no-close-on-backdrop
             no-close-on-esc
             @show="resetChecked()"
             class="m-0 p-0 serve-table">

     <div style="display: flex; flex-direction: row; justify-content: space-between" class="modal_header">
       <div><h5>Serve Citizen</h5></div>
       <div><b-button-close size="lg" @click="closeWindow" /></div>
     </div>

      <b-container id="serve-outer-container"
                   fluid>
        <b-row no-gutters class="p-2">
          <b-col cols="6">
            <div>Ticket #: <strong>{{citizen.ticket_number}}</strong></div>
            <div>Channels: <strong>{{channel.channel_name}}</strong></div>
            <div class="pt-3">
              <b-button @click="clickServiceBeginService"
                        :disabled="serviceBegun===true"
                        class="btn-primary serve-btn"
                        id="serve-citizen-begin-service-button">Begin Service</b-button>
              <b-button @click="clickReturnToQueue"
                        :disabled="serviceBegun===true"
                        class="btn-primary serve-btn"
                        id="serve-citizen-return-to-queue-button">Return to Queue</b-button>
              <b-button @click="clickCitizenLeft"
                        class="btn-danger serve-btn"
                        id="serve-citizen-citizen-left-button">Citizen Left</b-button>
            </div>
          </b-col>
          <b-col cols="6" style="text-align: left" class="pr-2">
            <div>
              <label>Comments</label>
            </div>
            <div>
              <b-textarea id="serve_comment_textarea"
                          v-model="comments"
                          :rows="4"
                          size="sm"/>
            </div>
          </b-col>
        </b-row>
      </b-container>
      <ServeCitizenTable/>

      <b-container fluid
                   id="serve-light-inner-container"
                   class="pt-3 mt-3 mb-4">
        <b-row no-gutters>
          <b-col cols="7"/>

          <b-col cols="auto" style="align: right">
            <b-button class="w-100 btn-primary serve-btn" @click="clickAddService" :disabled="serviceBegun===false">
              Add Next Service
            </b-button>
          </b-col>
          <b-col cols="2"/>
        </b-row>
      </b-container>

      <b-container fluid
                   id="add-citizen-modal-footer"
                   class="pt-3 mt-5">
        <b-row no-gutters align-h="center">
          <b-col cols="2" />
          <b-col cols="3">
            <b-button @click="clickHold"
                      :disabled="serviceBegun===false"
                      class="w-100 btn-primary serve-btn"
                      id="serve-citizen-place-on-hold-button">Place on Hold</b-button>
          </b-col>
          <b-col cols="2" />
          <b-col cols="3">
            <b-button @click="serviceFinish"
                      :disabled="serviceBegun===false"
                      class="w-100 btn-primary serve-btn"
                      id="serve-citizen-finish-button">
                        Finish
                    </b-button>
            <div v-if="serviceBegun===true" class="px-3 pt-1">
              <b-form-checkbox v-model="checked"
                               value="yes"
                               unchecked-value="no"
                               >
                <span style="font-size: 17px;">Innacurate Time</span>
              </b-form-checkbox>
            </div>
          </b-col>
          <b-col cols="2" />
        </b-row>
        <b-row no-gutters>
          <b-col cols="11"/>
          <b-col cols="1" class="mb-2 pt-3"><b-button size="sm" id="serve-citizen-footer-button" v-if="f">Feedback</b-button></b-col>
        </b-row>
      </b-container>
  </b-modal>
</template>

<script>
import { mapState, mapGetters, mapActions, mapMutations } from 'vuex'
import ServeCitizenTable from './serve-citizen-table'

export default {
  name: 'ServeCitizen',
  components: {
    ServeCitizenTable
  },
  data() {
    return {
      selected: '',
      f: false,
      t: true,
      checked: null
    }
  },
  computed: {
    ...mapState([
      'showServiceModal',
      'serviceBegun',
      'serviceModalForm'
    ]),

    ...mapGetters(['invited_citizen', 'active_service', 'invited_service_reqs']),

    citizen() {
      console.log(this.invited_citizen)
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

    channel() {
      if (!this.active_service) {
        return {channel_name: '', channel_id: ''}
      }
      return this.active_service.channel
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
      'putInaccurateIndicator'
    ]),
    ...mapMutations(['editServiceModalForm']),

    serviceFinish() {
      if (this.checked === 'yes') {
        this.putInaccurateIndicator().then(() => {
          this.clickServiceFinish()
        })
      } else {
        this.clickServiceFinish()
      }
    },

    resetChecked() {
      this.checked = 'no'
    },

    closeWindow() {
      this.$store.dispatch('clickServiceModalClose')
    }
  }
}

</script>
<style>

#serve_citizen_modal > div > div {
  width: 1200px !important;
  left: -200px;
  v-align: top;
}

#serve-outer-container {
  border: 1px solid grey;
  border-radius: 5px 5px 0px 0px;
  background-color: WhiteSmoke;
}

#add-citizen-modal-footer {
  border: 1px solid grey;
  border-radius: 0px 0px 9px 9px;
  background-color: WhiteSmoke;
}
.disabled {
  background-color: #8e9399 !important;
  color: Gainsboro !important;
}
.disabled:hover {
  background-color: #8e9399 !important;
}

</style>
