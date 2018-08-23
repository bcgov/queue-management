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
             @dismiss-count-down="countDownChanged"
             >
      {{this.$store.state.alertMessage}}
    </b-alert>

    <b-container fluid>
      <b-row>
        <b-col style="padding-top: 10px" cols="8">
          <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start">
            <div>
              <b-button class="m-1 btn-primary"
                        @click="invite"
                        :disabled="citizenInvited===true"
                        v-if="reception"
                        id="invite-citizen-button">Invite</b-button>
              <b-button v-bind:class="serveNowStyle"
                        @click="clickServeNow"
                        :disabled="citizenInvited===false"
                        id="serve-citizen-button">Serve Now</b-button>
            </div>
            <div>
              <b-button class="m-1 btn-primary"
                        @click="clickAddCitizen""
                        :disabled="citizenInvited===true"
                        id="add-citizen-button">Add Citizen</b-button>
              <b-button class="m-1 btn-primary"
                        @click="clickAddCitizen""
                        :disabled="citizenInvited===true"
                        id="add-citizen-button">Back Office</b-button>
            </div>
          </div>
        </b-col>
        <b-col />
      </b-row>
    </b-container>
    <b-container fluid v-if="isLoggedIn">
      <b-row>
        <b-col>
          <ServeCitizen v-if="showServiceModal" />
          <AddCitizen />
        </b-col>
      </b-row>
    <template v-if="reception">
      <b-row no-gutters class="mt-1" >
        <b-col class="font-900-rem" id="citizen-wait-count">
          Citizens Waiting: {{ queueLength }}
        </b-col>
      </b-row>


      <b-row no-gutters>
        <b-col class="dash-table-col m-0 p-0" v-bind:style="{height: queueHeight}" xl="12">
          <DashTable />
        </b-col>
      </b-row>
      <b-row no-gutters class="m-0 p-0">
        <b-col class="m-0 p-0">
          <b-button class="m-0 p-0" variant="link" @click="clickExpandContract">
            <font-awesome-icon class="m-0 p-0"
                               v-bind:icon="computeIcon"
                               style="font-size: 2rem; padding: 0px;"
                               >
            </font-awesome-icon>
          </b-button>
        </b-col>
      </b-row>
      <b-row no-gutters class="m-0 p-0">
        <b-col class="font-900-rem m-0 p-0">
          Citizens on Hold: {{on_hold_queue.length}}
        </b-col>
      </b-row>

      <b-row no-gutters class="m-0 p-0">
        <b-col class="dash-table-col m-0 p-0" xl="12" v-bind:style="{height: holdHeight}">
          <DashHoldTable />
        </b-col>
      </b-row>
    </template>
      <template v-else-if="!reception">
        <b-row no-gutters class="m-0 p-0">
          <b-col class="font-900-rem m-0 p-0">
            Citizens on Hold: {{on_hold_queue.length}}
          </b-col>
        </b-row>

        <b-row no-gutters class="m-0 p-0">
          <b-col class="dash-table-col m-0 p-0" xl="12" style="max-height: 600px; min-height: 200px;">
            <DashHoldTable />
          </b-col>
        </b-row>
        </template>
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
        citizencount: this.queueLength,
        y: 300,
        ymax: 300,
        interval: null,
        point: 'down'
      }
    },

    computed: {
      ...mapState([
        'isLoggedIn',
        'citizenInvited',
        'dismissCountDown',
        'showServiceModal',
        'serveNowStyle'
      ]),
      ...mapGetters(['citizens_queue', 'on_hold_queue', 'reception']),

      computeIcon() {
        if (this.point === 'up') return 'caret-up'
        if (this.point === 'down') return 'caret-down'
      },
      queueLength() {
        return this.citizens_queue.length
      },
      holdHeight() {
        return `${(600 - this.y)}px`
      },
      queueHeight() {
        return `${this.y}px`
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
      },
      clickExpandContract() {
        if (this.y === 300) {
          this.ymax = 450
          this.interval = setInterval( () => { this.makeBigger() }, 15)
          return
        }
        if (this.y === 450) {
          this.ymax = 300
          this.interval = setInterval( () => { this.makeSmaller() }, 15)
          return
        }
      },
      makeBigger() {
        let sizeUp = () => {
          this.y += 5
        }
        if (this.y >= this.ymax) {
          clearInterval(this.interval)
          this.y = 450
          this.point = 'up'
          return
        }
        sizeUp()
      },
      makeSmaller() {
        let sizeDown = () => {
          this.y -= 5
        }
        if (this.y < this.ymax) {
          clearInterval(this.interval)
          this.y = 300
          this.point = 'down'
          return
        }
        sizeDown()
      }
    }
  }
</script>

<style>
  .dash-table-col {
    overflow-y: scroll; overflow: scroll; border: 1px solid;
  }
  .font-900-rem {
    font-size: .9rem;
  }
  .modal-main div {
    background-color: blue;
  }
  .btn-highlighted {
    background-color: #FEDF01 !important;
    color: black !important;
    border: 1px solid white;
  }
  #queue-col-top {
    display: flex; width: 100%; justify-content: space-between;
  }
</style>
