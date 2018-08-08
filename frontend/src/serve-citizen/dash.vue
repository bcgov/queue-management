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

    <b-container fluid>
      <b-row>
        <b-col style="padding-top: 10px">
          <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start">
            <div>
              <b-button class="m-1 btn-primary"
                        @click="invite"
                        :disabled="citizenInvited===true"
                        id="invite-citizen-button">Invite</b-button>
              <b-button class="m-1 btn-primary"
                        @click="clickServeNow"
                        :disabled="citizenInvited===false"
                        id="serve-citizen-button">Serve Now</b-button>
            </div>
            <div>
              <b-button class="m-1 btn-primary"
                        @click="clickAddCitizen""
                        :disabled="citizenInvited===true"
                        id="add-citizen-button">Add Citizen</b-button>
              <b-button class="m-1" v-if="f" :disabled="citizenInvited===true">Back Office</b-button>
            </div>
          </div>
        </b-col>
        <b-col />
      </b-row>
    </b-container>
    <b-container fluid v-if="isLoggedIn">
      <b-row>
        <b-col>
          <ServeCitizen />
          <AddCitizen />
        </b-col>
      </b-row>

      <b-row no-gutters class="mt-2">
        <b-col class="m-2" id="citizen-wait-count">
          Citizens Waiting: {{ queueLength }}
        </b-col>
      </b-row>

      <b-row no-gutters>
        <b-col style="height: 250px; overflow-y: scroll; overflow: scroll; margin-bottom: 1em; border: 1px solid;" xl="12">
          <DashTable />
        </b-col>
      </b-row>

      <b-row no-gutters>
        <b-col>
          Citizens on Hold: {{on_hold_queue.length}}
        </b-col>
      </b-row>

      <b-row no-gutters>
        <b-col style="height: 250px; overflow-y: scroll; overflow: scroll; border: 1px solid;" xl="12">
          <DashHoldTable />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions, mapMutations } from 'vuex'
import AddCitizen from './../add-citizen/add-citizen'
import DashTable from './dash-table'
import DashHoldTable from './dash-hold-table'
import ServeCitizen from './serve-citizen'

  export default {
    name: 'Dash',

    components: {
      AddCitizen,
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
        'citizenInvited',
        'dismissCountDown'
      ]),
      ...mapGetters(['citizens_queue', 'on_hold_queue']),

      queueLength() {
        return this.citizens_queue.length
      }
    },

    methods: {
      ...mapMutations(['setMainAlert']),
      ...mapActions([
        'clickInvite',
        'clickAddCitizen',
        'clickServiceModalClose',
        'clickCitizenLeft',
        'clickServeNow',
        'clickBackOffice'
      ]),

      invite() {
        if (this.queueLength === 0) {
          this.setMainAlert('The are currently no citizens to invite.')
        } else {
          this.clickInvite()
        }
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
