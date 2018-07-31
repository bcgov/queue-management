

<template>
    <b-modal id="serve_citizen_modal"
             :visible="this.$store.state.showServiceModal"
             size="lg"
             hide-header
             hide-footer
             no-close-on-backdrop
             no-close-on-esc
             class="m-0 p-0">

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
                        :disabled="serveBeginServiceDisabled"
                        class="btn-primary">Begin Service</b-button>
              <b-button @click="clickReturnToQueue"
                        :disabled="serveReturnQueueDisabled"
                        class="btn-primary">Return to Queue</b-button>
              <b-button @click="clickCitizenLeft"
                        class="btn-danger">Citizen Left</b-button>
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
          <b-col cols="2"/>
          <b-col cols="3"><b-form-select v-model="selected"
                                         :options="options"
                                         v-if="f" />
          </b-col>
          <b-col cols="2"/>
          <b-col cols="3" style="align: right">
            <b-button v-if="f" class="w-75">Add Next Service</b-button>
          </b-col>
          <b-col cols="2"/>
        </b-row>
      </b-container>

      <b-container fluid
                   id="add-citizen-modal-footer"
                   class="pt-3 mt-5">
        <b-row no-gutters>
          <b-col cols="2" />
          <b-col cols="3">
            <b-button @click="clickHold"
                      :disabled="finishDisabled"
                      class="w-75 btn-primary">Place on Hold</b-button>
          </b-col>
          <b-col cols="2" />
          <b-col cols="3">
            <b-button @click="clickFinishService"
                      :disabled="finishDisabled"
                      class="w-75 btn-primary" >Finish</b-button>
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
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
import ServeCitizenTable from './serve-citizen-table'

export default {
  name: 'ServeCitizen',
  components: {
    ServeCitizenTable
  },
  data() {
    return {
      selected: '',
      f: false
    }
  },
  computed: {
    ...mapState([
      'showServiceModal',
      'invitedCitizen',
      'serveBeginServiceDisabled',
      'serveCitizenLeftDisabled',
      'serveReturnQueueDisabled',
      'finishDisabled'
    ]),

    citizen() {
    return this.invitedCitizen
  },

    comments: {
      get() { return this.citizen.citizen_comments },
      set(value) {
        this.$store.commit('editInvitedCitizen',{type:'citizen_comments',value})
      }},
      options() {
        let { service_reqs } = this.citizen

        if (service_reqs.length === 1 || !service_reqs) {
          return [{text:'no other services', value: null}]
        } else if (service_reqs.length > 1) {
          let array_options = service_reqs.map(req =>
          ({text:req.service.service_name, value:req.service.service_name})
        )
        return array_options
        }
      },

    channel() {
      if (this.citizen) {
        return this.citizen.service_reqs[0].channel
      } else {
        return ''
      }
    }},

  methods: {
    ...mapActions([
      'clickCitizenLeft',
      'postBeginService',
      'editServiceButton',
      'clickServiceBeginService',
      'clickServiceModalClose',
      'clickFinishService',
      'clickReturnToQueue',
      'clickHold'
    ]),
    ...mapMutations(
      {
        toggleService: 'toggleServiceModal',
        editServices: 'editServicesFromServe',
        toggleAdd: 'toggleAddCitizen'
      }
    ),

    closeWindow() {
      this.$store.dispatch('clickServiceModalClose')
    },
    beginService(item, index) {
      this.postBeginService()
      this.toggleService(false)
    },
    clickEdit() {
      this.editServices()
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

#serve-citizen-footer-button {
  color: dimgrey;
  background-color: WhiteSmoke;
  border: .75px solid lightgrey;
  font-size: 17px;
}
</style>
