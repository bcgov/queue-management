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
  <div id="dashmaincontainer" class="dashmaincontainer" key="dashmaincontainer">
    <b-alert :show="dismissCountDown"
             dismissible
             style="h-align: center"
             variant="warning"
             @dismissed="dismissCountDown=0"
             @dismiss-count-down="countDownChanged">{{this.$store.state.alertMessage}}</b-alert>
    <div v-bind:style="{width:'100%', height:`${buttonH}px`}" v-if="isLoggedIn">
      <AddCitizen />
      <ServeCitizen v-if="showServiceModal"/>
      <div id="dash-flex-button-container">
        <div>
          <b-button class="btn-primary"
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
          <b-button class="btn-primary"
                    @click="clickAddCitizen"
                    :disabled="citizenInvited===true"
                    id="add-citizen-button">Add Citizen</b-button>
          <b-button class="btn-primary"
                    @click="clickAddCitizen"
                    :disabled="citizenInvited===true"
                    id="add-citizen-button">Back Office</b-button>
        </div>
        <div>
          <b-button class="btn-primary"
                    @click="clickFeedback"
                    id="click-feedback-button">Feedback</b-button>
        </div>
      </div>
    </div>
    <template v-if="reception && isLoggedIn">
      <div v-bind:style="{width:'100%', height: `${qLengthH}px`}" class="font-900-rem">
        Citizens Waiting: {{ queueLength }}
      </div>
      <div class="dash-table-holder" v-bind:style="{width:'100%', height:`${dashH}px`}">
        <DashTable />
      </div>
      <div v-bind:style="{width:'100%', height:`${qLengthH}px`}">
        <div style="display: flex; width: 100%; justify-content: space-between;">
          <div class="font-900-rem">Citizens on Hold: {{on_hold_queue.length}}</div>
          <b-button variant="link" v-dragged="onDrag" class="m-0 p-0">
            <font-awesome-icon icon="sort"
                              class="m-0 p-0"
                              style="font-size: 1.5rem;" />
          </b-button>
        </div>
      </div>
      <div class="dash-table-holder" v-bind:style="{width:'100%',height:`${holdH}px`}">
        <DashHoldTable />
      </div>
    </template>
    <template v-else-if="!reception && isLoggedIn">
      <div class="font-900-rem">Citizens on Hold: {{on_hold_queue.length}}</div>
      <div class="dash-table-holder" v-bind:style="{width:'100%',minHeight:'200px',maxHeight:`${this.availH}px`}">
        <DashHoldTable></DashHoldTable>
      </div>
    </template>
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
      let totalH = dashmaincontainer.clientHeight
      let availH = totalH-(2 * this.qLengthH)-this.buttonH-16
      this.availH = availH
    },

    data() {
      return {
        availH: '',
        buttonH: 45,
        qLengthH: 28,
        isDragged: false,
        offset: 0,
        t: true,
        f: false,
        last: 0,
        dismissSecs: 5,
        citizencount: this.queueLength,
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
      queueLength() {
        return this.citizens_queue.length
      },
      holdHeight() {
        return `${(600 - this.y)}px`
      },
      queueHeight() {
        return `${this.y}px`
      },
      dashH() {
        if (!this.isDragged) return this.availH / 2;
        if (this.isDragged) return this.availH + this.offset;
      },
      holdH() {
        if (!this.isDragged) return this.availH / 2;
        if (this.isDragged) return this.availH - this.dashH;
      }
    },

    methods: {
      ...mapMutations(['setMainAlert', 'toggleFeedbackModal']),
      ...mapActions([
        'clickInvite',
        'clickAddCitizen',
        'clickServiceModalClose',
        'clickCitizenLeft',
        'clickServeNow',
        'clickBackOffice'
      ]),
      onDrag({ deltaY, first, last }) {
        this.isDragged = true
        if (first) {
          this.offset = -this.availH / 2 + this.last
          return
        }
        if(!first && !last) {
          this.offset += deltaY
          this.last = (this.availH / 2) + this.offset
        }
      },
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

      clickFeedback() {
        this.toggleFeedbackModal(true)
      }
    }
  }
</script>

<style scoped>
  .dashmaincontainer {
    height: 85%; width: 100%; display: block; position: absolute; top: 75px;
    padding-left: 1%; padding-right: 1%; padding-top: 8px; padding-bottom: 8px;
  }
  #dash-flex-button-container {
    display: flex; justify-content: space-between; height: 100% !important;
  }
  .dash-table-holder {
    overflow-y: scroll; overflow: scroll; border: 1px solid dimgrey;
  }
  .font-900-rem {
    font-size: .9rem;
  }
  .modal-main div {
    background-color: blue;
  }
</style>
