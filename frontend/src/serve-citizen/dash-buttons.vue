<!--
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
  -->

<template>
  <div id="dash-flex-button-container">
    <div>
      <b-button class="btn-primary mr-1"
                @click="invite"
                :disabled="citizenInvited===true || performingAction || showAdmin"
                v-if="reception"
                id="invite-citizen-button">Invite</b-button>
      <b-button v-bind:class="serveNowStyle"
                @click="clickServeNow"
                :disabled="citizenInvited===false"
                id="serve-citizen-button">Serve Now</b-button>
    </div>
    <div>
      <b-button class="btn-primary mr-1"
                @click="addCitizen"
                :disabled="citizenInvited===true || performingAction || showAdmin"
                id="add-citizen-button">Add Citizen</b-button>
      <b-button class="btn-primary"
                @click="clickBackOffice"
                :disabled="citizenInvited===true || performingAction || showAdmin"
                id="add-citizen-button">Back Office</b-button>
    </div>
    <div />
  </div>
</template>

<script>
  import { mapState, mapMutations, mapGetters, mapActions } from 'vuex'
  export default {
    name: "DashButtons",
    computed: {
      ...mapGetters([
        'reception',
        'citizens_queue'
      ]),
      ...mapState([
        'isLoggedIn',
        'showAddModal',
        'citizenInvited',
        'performingAction',
        'showAdmin',
        'showGAScreenModal',
        'showServiceModal',
        'serveNowStyle',
        'user',
      ]),
      queueLength() {
        return this.citizens_queue.length
      },
    },
    methods: {
      ...mapMutations([
        'setMainAlert',
        'toggleFeedbackModal',
      ]),
      ...mapActions([
        'clickInvite',
        'clickAddCitizen',
        'clickAdmin',
        'clickGAScreen',
        'clickServeNow',
        'clickBackOffice'
      ]),
      addCitizen() {
        this.clickAddCitizen()
      },
      invite() {
        if (this.queueLength === 0) {
          this.setMainAlert('The are currently no citizens to invite.')
        } else {
          this.clickInvite()
        }
      },
      clickFeedback() {
        this.toggleFeedbackModal(true)
      },
    }
  }
</script>

<style scoped>
  #dash-flex-button-container {
    display: flex;
    justify-content: space-between;
    width: 100%;
    height: 100% !important;
  }
  .btn-highlighted {
    color: black;
    border: 1px solid darkgoldenrod;
    background-color: gold;
  }
</style>
