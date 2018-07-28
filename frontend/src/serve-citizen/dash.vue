/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/



<template>
  <div>
    <b-alert :show="dismissCountDown"
             dismissible
             style="h-align: center"
             variant="warning"
             @dismissed="dismissCountDown=0"
             @dismiss-count-down="countDownChanged">
      {{this.$store.state.alertMessage}}
    </b-alert>
    
    <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start" class="modal-header">
      <div>
        <b-button class="m-1" 
                  @click="invite"
                  :disabled="inviteButtonDisabled"
                  >
          Invite
        </b-button>
        <b-button class="m-1" 
                  @click="clickServeNow" 
                  :disabled="serveButtonDisabled"
                  >
          Serve Now
        </b-button>
      </div>
      <div>
        <b-button class="m-1" 
                  @click="addCitizen"
                  :disabled="addCitizenDisabled"
                  >Add Citizen</b-button>
        <b-button class="m-1" v-if="f" :disabled="backOfficeDisabled">Back Office</b-button>
      </div>
      <div>
        <Login />
      </div>
    </div>
  <b-container fluid>
    
    <b-row>
      <b-col>
        <ServeCitizen v-if="isLoggedIn"/>
        <AddCitizen v-if="isLoggedIn"/>
      </b-col>
    </b-row>
      
    <b-row no-gutters v-if="isLoggedIn">
      <b-col>
        Citizens Waiting: {{ queueLength }}
      </b-col>
    </b-row>
    
    <b-row no-gutters v-if="isLoggedIn">
      <DashTable />
    </b-row>
    
    <b-row no-gutters>
      <b-col>
        <Socket v-show="f" />
      </b-col>
      <b-col/>
      <b-col/>
    </b-row>
    
    <b-row no-gutters v-if="isLoggedIn">
      <b-col> 
        Citizens on Hold: {{on_hold.length   }}
      </b-col>
    </b-row>
    
    <b-row v-if="isLoggedIn">
      <b-col>
        <DashHoldTable />
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<script>
import { mapState, mapGetters, mapActions, mapMutations } from 'vuex'
import Login from './../Login'
import AddCitizen from './../add-citizen/add-citizen'
import Socket from './../Socket'
import DashTable from './dash-table'
import DashHoldTable from './dash-hold-table'
import ServeCitizen from './serve-citizen'

  export default {
    name: 'Dash',
    
    components: { 
      AddCitizen,  
      Login,
      Socket,
      DashTable,
      DashHoldTable,
      ServeCitizen
    },
    
    mounted() {
      this.$root.$on('showMessage', () => {
        this.showAlert()
      })
    },
    
    data() {
      return {
        enbleServe: true,
        t: true,
        f: false,
        dismissSecs: 5,
        citizencount: this.queueLength
      }
    },
    
    computed: {
      ...mapState([
        'isLoggedIn', 
        'inviteButtonDisabled',
        'serveButtonDisabled',
        'addCitizenDisabled',
        'backOfficeDisabled',
        'dismissCountDown'
      ]),
      ...mapGetters(['filtered_citizens', 'on_hold']),
      
      queueLength() {
        return this.filtered_citizens.length
      }
    }, 
    
    methods: {
      ...mapMutations(['setAlert']),
      ...mapActions([
        'clickInvite', 
        'addCitizen', 
        'clickServiceModalClose',
        'clickCitizenLeft',
        'clickServeNow'
      ]),      
      
      invite() {
        if (this.queueLength === 0) {
          this.setAlert('The are currently no citizens to invite.')
        } else {
          this.clickInvite()
        }
      },
      
      toggleModal() {
        this.toggleServeNow(true)
      },
      
      countDownChanged(dismissCountDown) {
        this.$store.commit('dismissCountDown', dismissCountDown)
      }
    }
  }
</script>

<style>
  .modal-main div {
    background-color: blue;
  }
</style>