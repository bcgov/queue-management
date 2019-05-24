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
                :disabled="citizenInvited || showTimeTrackingIcon || performingAction || showAdmin"
                v-if="reception"
                id="invite-citizen-button">Invite</b-button>
      <b-button v-bind:class="serveNowStyle"
                @click="clickServeNow"
                :disabled="citizenInvited===false"
                id="serve-citizen-button">Serve Now</b-button>
    </div>
    <div>
      <b-button-group>
        <b-button class="btn-primary"
                  @click="addCitizen"
                  :disabled="citizenInvited || showTimeTrackingIcon || performingAction || showAdmin"
                  id="add-citizen-button">Add Citizen</b-button>
        <b-dropdown v-if="user.office.quick_list.length > 0"
          :variant="citizenInvited===true || performingAction || showAdmin ? '' : 'primary'"
          :disabled="citizenInvited || showTimeTrackingIcon || performingAction || showAdmin" right>
            <b-dropdown-item v-for="item in user.office.quick_list"
                    :data-id="item.service_id"
                    :key="item.service_id"
                    @click="quickServeCitizen">
              {{item.service_name}}
            </b-dropdown-item>
        </b-dropdown>
      </b-button-group>

      <b-button-group>
        <b-button class="btn-primary"
                  @click="clickBackOffice"
                  :disabled="citizenInvited || showTimeTrackingIcon || performingAction || showAdmin"
                  id="add-citizen-button">Back Office</b-button>
        <b-dropdown v-if="user.office.back_office_list.length > 0"
          :variant="citizenInvited===true || performingAction || showAdmin ? '' : 'primary'"
          :disabled="citizenInvited || showTimeTrackingIcon || performingAction || showAdmin" right>
            <b-dropdown-item v-for="item in user.office.back_office_list"
                    :data-id="item.service_id"
                    :key="item.service_id"
                    @click="quickBackOffice">
              {{item.service_name}}
            </b-dropdown-item>
        </b-dropdown>
      </b-button-group>
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
        'showTimeTrackingIcon',
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
        'setAddModalSelectedItem'
      ]),
      ...mapActions([
        'clickInvite',
        'clickAddCitizen',
        'clickAdmin',
        'clickGAScreen',
        'clickServeNow',
        'clickBackOffice',
        'clickQuickServe',
        'clickQuickBackOffice',
      ]),
      addCitizen() {
        this.clickAddCitizen()
      },
      quickServeCitizen(e) {
        let service_id = e.target.dataset.id
        let service_name = e.target.innerText

        if(this.user.receptionist_ind && this.user.office.sb.sb_type !== "nocallonsmartboard"){
          this.clickAddCitizen()
          this.$store.commit('updateAddModalForm', {type:'service',value:service_id})
          this.$store.commit('updateAddModalForm', {type:'search',value:service_name})
        } else {
          this.setAddModalSelectedItem(service_name)
          this.$store.commit('updateAddModalForm', {type:'service',value:service_id})
          this.clickQuickServe()
        }
      },
      quickBackOffice(e) {
        let service_id = e.target.dataset.id
        let service_name = e.target.innerText

        if(this.user.receptionist_ind && this.user.office.sb.sb_type !== "nocallonsmartboard"){
          this.clickBackOffice()
          this.$store.commit('updateAddModalForm', {type:'service',value:service_id})
          this.$store.commit('updateAddModalForm', {type:'search',value:service_name})
        } else {
          this.setAddModalSelectedItem(service_name)
          this.$store.commit('updateAddModalForm', {type:'service',value:service_id})
          this.clickQuickBackOffice()
        }
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
