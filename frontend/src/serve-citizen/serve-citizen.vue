

<template>
  <div id="serveModal" class="serve-modal">
    <div class="serve-modal-content">
     <div style="display: flex; flex-direction: row; justify-content: space-between" class="modal_header">
       <div><h5>Serve Citizen</h5></div>
       <div><b-button-close size="lg" @click="closeWindow" /></div>
     </div>

      <b-container class="pb-3" id="serve-citizen-modal-top" fluid>
       <b-row no-gutters class="p-2">
         <b-col col cols="4">
           <div><h6>Ticket #: <strong>{{citizen.ticket_number}}</strong></h6></div>
           <div><h6>Channel: <strong>{{channel.channel_name}}</strong></h6></div>

         </b-col>
         <b-col cols="auto" class="ml-3 mr-2">
           <h6>Comments</h6>
         </b-col>
         <b-col col cols="*" style="text-align: left" class="pr-2">
           <div>
             <b-textarea id="serve_comment_textarea"
                         v-model="comments"
                         :rows="4"
                         size="sm"
                         />
           </div>
         </b-col>
       </b-row>
       <b-row>
         <b-col>
           <div class="pt-3" style="display: flex; flex-direction: row; justify-content: space-between;">
             <div>
             <b-button @click="clickServiceBeginService"
                       :disabled="serviceBegun===true"
                       v-bind:class="buttonStyle"
                       id="serve-citizen-begin-service-button">Begin Service</b-button>
             <b-button @click="clickReturnToQueue"
                       :disabled="serviceBegun===true"
                       class="btn-primary serve-btn"
                       id="serve-citizen-return-to-queue-button">Return to Queue</b-button>
             </div>
             <div>
             <b-button @click="clickCitizenLeft"
                       class="btn-danger serve-btn"
                       id="serve-citizen-citizen-left-button">Citizen Left</b-button>
             </div>
           </div>
         </b-col>
       </b-row>
     </b-container>
     <ServeCitizenTable/>

     <b-container fluid
                  id="serve-light-inner-container"
                  class="pt-3 pb-3">
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

     <div>
     <b-container fluid
                  id="serve-citizen-modal-footer"
                  class="pt-3">
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
               <span style="font-size: 17px;">Inaccurate Time</span>
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
    }
  }
}

</script>

<style scoped>
  .serve-modal {
    position: fixed; 
    z-index: 1; 
    left: 0;
    top: 0;
    width: 100%; 
    height: 100%; 
    overflow: auto; 
    background-color: rgb(0,0,0); 
    background-color: rgba(0,0,0,0.4); 
    transition: display 1s;
}

.serve-modal-content {
    background-color: #fefefe;
    margin-right: auto; 
    margin-left: auto;
    margin-top: 1%;
    border-radius: 5px;
    padding: 20px;
    border: 1px solid #888;
    width: 80%; 
    
}

#serve-citizen-modal-top {
  border: 1px solid grey;
  background-color: WhiteSmoke;
}

  .btn-highlighted {
    background-color: orange !important;
    color: white !important;
    border: 1px solid orangered;
  }

#serve-citizen-modal-footer {
  border: 1px solid grey;
  background-color: WhiteSmoke;
}
strong {
  color: blue;
  font-size: 21px;
}
</style>
