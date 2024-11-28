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
    <div id="navi">
      <template v-if="showInviteCitizenSpinner">
        <div class="q-loader2"></div>
      </template>
      <b-button
        class="btn-primary mr-1"
        @click="invite"
        :disabled="
          citizenInvited ||
          showTimeTrackingIcon ||
          performingAction ||
          showAdmin
        "
        v-if="reception"
        id="invite-citizen-button"
        >Invite</b-button
      >
      <b-button
        v-bind:class="serveNowStyle"
        @click="clickServeNow"
        :disabled="citizenInvited === false"
        id="serve-citizen-button"
        >Serve Now</b-button
      >
    </div>
    <div>
      <b-button-group>
        <b-button
          class="btn-primary ml-2"
          @click="addCitizen"
          :disabled="
            citizenInvited ||
            showTimeTrackingIcon ||
            performingAction ||
            showAdmin
          "
          id="add-citizen-button"
          >Add Citizen</b-button
        >
        <b-dropdown
          v-if="user.office.quick_list.length > 0"
          :variant="
            citizenInvited === true || performingAction || showAdmin
              ? ''
              : 'primary'
          "
          :disabled="
            citizenInvited ||
            showTimeTrackingIcon ||
            performingAction ||
            showAdmin
          "
          right
        >
          <b-dropdown-item
            v-for="item in user.office.quick_list"
            :data-id="item.service_id"
            :key="item.service_id"
            @click="quickServeCitizen"
            >{{ item.service_name }}</b-dropdown-item
          >
        </b-dropdown>
      </b-button-group>

      <b-button-group>
        <b-button
          class="btn-primary ml-2"
          @click="clickBackOffice"
          :disabled="
            citizenInvited ||
            showTimeTrackingIcon ||
            performingAction ||
            showAdmin
          "
          id="add-citizen-button"
          >Back Office</b-button
        >
        <b-dropdown
          v-if="user.office.back_office_list.length > 0"
          :variant="
            citizenInvited === true || performingAction || showAdmin
              ? ''
              : 'primary'
          "
          :disabled="
            citizenInvited ||
            showTimeTrackingIcon ||
            performingAction ||
            showAdmin
          "
          right
        >
          <b-dropdown-item
            v-for="item in user.office.back_office_list"
            :data-id="item.service_id"
            :key="item.service_id"
            @click="quickBackOffice"
            >{{ item.service_name }}</b-dropdown-item
          >
        </b-dropdown>
      </b-button-group>
    </div>
    <div />
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class DashButtons extends Vue {
  @State('isLoggedIn') private isLoggedIn!: any
  @State('showAddModal') private showAddModal!: any
  @State('citizenInvited') private citizenInvited!: any
  @State('performingAction') private performingAction!: any
  @State('showAdmin') private showAdmin!: any
  @State('showGAScreenModal') private showGAScreenModal!: any
  @State('showServiceModal') private showServiceModal!: any
  @State('showTimeTrackingIcon') private showTimeTrackingIcon!: any
  @State('serveNowStyle') private serveNowStyle!: any
  @State('user') private user!: any
  @State('showInviteCitizenSpinner') private showInviteCitizenSpinner!: any

  @Getter('reception') private reception!: any;
  @Getter('citizens_queue') private citizens_queue!: any;

  @Action('clickInvite') public clickInvite: any
  @Action('clickAddCitizen') public clickAddCitizen: any
  @Action('clickAdmin') public clickAdmin: any
  @Action('clickGAScreen') public clickGAScreen: any
  @Action('clickServeNow') public clickServeNow: any
  @Action('clickBackOffice') public clickBackOffice: any
  @Action('clickQuickServe') public clickQuickServe: any
  @Action('clickQuickBackOffice') public clickQuickBackOffice: any

  @Mutation('setMainAlert') public setMainAlert: any
  @Mutation('toggleFeedbackModal') public toggleFeedbackModal: any
  @Mutation('setAddModalSelectedItem') public setAddModalSelectedItem: any

  get queueLength () {
    return this.citizens_queue.length
  }

  private addCitizen () {
    this.clickAddCitizen()
  }

  private quickServeCitizen (e: any) {
    const service_id = e.target.dataset.id
    const service_name = e.target.innerText.trim()

    //  If CSR is on reception, and a reception office, bring up add citizen form with defaults.
    if (this.user.receptionist_ind && this.user.office.sb.sb_type !== 'nocallonsmartboard') {
      this.clickAddCitizen()
      this.$store.commit('updateAddModalForm', { type: 'service', value: service_id })
      this.$store.commit('updateAddModalForm', { type: 'search', value: service_name })
      //  If CSR NOT on reception or NOT a reception office just serve the citizen.
    } else {
      this.setAddModalSelectedItem(service_name)
      this.$store.commit('updateAddModalForm', { type: 'service', value: service_id })
      this.clickQuickServe()
    }
  }

  private quickBackOffice (e: any) {
    const service_id = e.target.dataset.id
    const service_name = e.target.innerText.trim()

    if (this.user.receptionist_ind && this.user.office.sb.sb_type !== 'nocallonsmartboard') {
      this.clickBackOffice()
      this.$store.commit('updateAddModalForm', { type: 'service', value: service_id })
      this.$store.commit('updateAddModalForm', { type: 'search', value: service_name })
    } else {
      this.setAddModalSelectedItem(service_name)
      this.$store.commit('updateAddModalForm', { type: 'service', value: service_id })
      this.clickQuickBackOffice()
    }
  }

  private invite () {
    if (this.queueLength === 0) {
      this.setMainAlert('The are currently no citizens to invite.')
    } else {
      this.clickInvite()
    }
  }

  private clickFeedback () {
    this.toggleFeedbackModal(true)
  }
}

</script>

<style scoped>
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
#navi {
  position: relative;
  z-index: 1000;
}
.q-loader2 {
  position: absolute;
  text-align: center;
  margin: 50px auto auto 50px;
  width: 50px;
  height: 50px;
  border: 10px solid LightGrey;
  opacity: 0.9;
  border-radius: 50%;
  border-top-color: DodgerBlue;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
  z-index: 1500;
}
#dash-flex-button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 100% !important;
  z-index: 1;
}
.btn-highlighted {
  color: black;
  border: 1px solid darkgoldenrod;
  background-color: gold;
}
</style>
