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
  <div style>
    <b-alert
      :show="showIEWarning"
      style="justify-content: center"
      variant="danger"
      dismissible
      fade
    >
      You are using Internet Explorer, and may have a degraded experience. To increase performance and access all features please use a modern browser, like 
      Chrome or Microsoft Edge
    </b-alert>
    <div class="dash-button-flex-button-container pb-0 mb-3 mx-4">
      <!-- SLOT FOR EACH VIEW'S BUTTON CONTROLS-->
      <div
        style="width: 75px"
        v-show="$route.path !== '/queue' || showTimeTrackingIcon"
      >
        <b-button
          :variant="showIcon.style"
          v-if="showIcon.show"
          v-show="flashIcon"
          class="mr-3"
          @click="clickIcon"
        >
          <font-awesome-icon
            icon="stopwatch"
            style="font-size: 1rem; color: white"
            class="p0"
            id="booking_time_tracking"
          />
        </b-button>
      </div>
      <router-view name="buttons"></router-view>
      <div
        v-if="calendarSetup && this.$route.path === '/booking'"
        style="flex-grow: 8"
        class="q-inline-title"
      >
        {{
          calendarSetup.titleRef.title
            ? calendarSetup.titleRef.title
            : calendarSetup.title
        }}
      </div>
      <div
        v-if="calendarSetup && this.$route.path === '/agenda'"
        style="flex-grow: 8"
        class="q-inline-title"
      >
        {{ calendarSetup.titleRef.title }}
      </div>
      <div />
      <div v-if="showHamburger">
        <b-dropdown
          variant="outline-primary"
          class="pl-0 ml-0 mr-3"
          right
          id="nav-dropdown"
          :popper-opts="dropdownPopperOpts"
        >
          <span slot="button-content">
            <font-awesome-icon icon="bars" style="font-size: 1.18rem" />
          </span>
          <div :style="{ width: 200 + 'px' }" id="nav-dropdown-buttons">
            <b-dropdown-item to="/queue" id="the_q">The Q</b-dropdown-item>
            <b-dropdown-item to="/booking" v-if="showExams" id="room_bookings"
              >Room Booking</b-dropdown-item
            >
            <b-dropdown-item
              to="/appointments"
              v-if="showAppointments"
              id="appointments"
              >Appointments</b-dropdown-item
            >
            <b-dropdown-item to="/exams" v-if="showExams" id="exam_inventory"
              >Exam Inventory</b-dropdown-item
            >
            <b-dropdown-item
              to="/agenda"
              v-if="isGAorCSR && showExams"
              id="office_agenda"
              >Office Agenda</b-dropdown-item
            >
            <b-dropdown-item to="/service-flow"  id="service_flow" v-if="isServiceFLowEnabled"
              >Service Flow</b-dropdown-item
            >
            <span v-if="user.role && (user.role.role_code == 'GA' || user.role.role_code == 'SUPPORT')">
              <b-dropdown-item @click="clickGAScreen">
                <font-awesome-icon
                  v-if="showGAScreenModal"
                  icon="check"
                  class="m-0 p-0"
                  style="
                    padding-left: 0.25em !important;
                    padding-top: 2px !important;
                  "
                />
                <span style="font-weight: 400">Show GA Panel</span>
              </b-dropdown-item>
              <b-dropdown-divider />
            </span>
            <b-dropdown-item v-if='appointmentsEnabled' @click='clickAgendaScreen'>
              <font-awesome-icon
                  v-if="showAgendaScreenModal"
                  icon="check"
                  class="m-0 p-0"
                  style="
                    padding-left: 0.25em !important;
                    padding-top: 2px !important;
                  "
                />
              <span>Show Day Agenda</span>
              <b-dropdown-divider />
            </b-dropdown-item>
            
            <b-dropdown-item v-if="showAdmin" to="/admin"
              >Administration</b-dropdown-item
            >
            <b-dropdown-item v-if="showAdmin" @click="clickRefresh"
              >Refresh</b-dropdown-item
            >
            <b-dropdown-item v-if="showSupport" to="/upload"
              >Upload File</b-dropdown-item
            >
            <b-dropdown-divider v-if="showAdmin" />
            <b-dropdown-item>
              <b-button
                class="btn-primary w-100 m-0"
                v-if="!showServiceModal"
                @click="clickFeedback"
                id="click-feedback-button"
                >Feedback</b-button
              >
            </b-dropdown-item>
          </div>
        </b-dropdown>
      </div>
    </div>
    <!--SLOT FOR EACH VIEW'S MAIN CONTENT-->
    <div style="position: relative; min-height: 400px">
      <router-view />
    </div>
    <AddCitizen />
    <ServeCitizen v-if="showServiceModal" />
  </div>
</template>

<script lang="ts">

import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'

import AddCitizen from '../AddCitizen/add-citizen.vue'
import ServeCitizen from '../ServeCitizen/serve-citizen.vue'
import config from '../../../config'
import configMap from '../../utils/config-helper'

@Component({
  components: {
    AddCitizen,
    ServeCitizen
  }
})
export default class Nav extends Vue {
  @State('citizenInvited') private citizenInvited!: any
  @State('showServiceModal') private showServiceModal!: any
  @State('calendarSetup') private calendarSetup!: any
  @State('rescheduling') private rescheduling!: any
  @State('scheduling') private scheduling!: any
  @State('serviceModalForm') private serviceModalForm!: any
  @State('serviceBegun') private serviceBegun!: any
  @State('showGAScreenModal') private showGAScreenModal!: any

  @State('showAgendaScreenModal') private showAgendaScreenModal!: any
  @State('showTimeTrackingIcon') private showTimeTrackingIcon!: any
  @State('showAddModal') private showAddModal!: any
  @State('user') private user!: any

  @Getter('showExams') private showExams!: any;
  @Getter('showAppointments') private showAppointments!: any;

  @Action('clickGAScreen') public clickGAScreen: any
  @Action('clickAgendaScreen') public clickAgendaScreen: any

  
  @Action('clickAddCitizen') public clickAddCitizen: any
  @Action('clickRefresh') public clickRefresh: any

  @Mutation('toggleFeedbackModal') public toggleFeedbackModal: any
  @Mutation('toggleServiceModal') public toggleServiceModal: any
  // to check service for enable
  public isServiceFLowEnabled = configMap.isServiceFLowEnabled()

  private flashIcon: boolean = true
  private showSpacer: boolean = false
  toggleTimeTrackingIcon: any
    dropdownPopperOpts = {
    modifiers: {
      computeStyle: {
        gpuAcceleration: false
      }
    }
  }

  showIEWarning: boolean = config.IS_INTERNET_EXPLORER;

  mounted() {
    // We don't want to re-evaluate this every time appointmentsEnabled is re-evaluated
    this.showIEWarning = this.showIEWarning && this.appointmentsEnabled
  }

  get appointmentsEnabled() : boolean {
    if (this.user && this.user.office) {
      return !!(this.user.office.appointments_enabled_ind)
    }
    return false;
  }

  @Watch('showIcon')
  onShowIconChange (newV: any, oldV: any) {
    if (this.$route.path === '/queue' && newV.show && !oldV.show) {
      this.showSpacer = true
      let k = 4
      const flash = () => {
        this.flashIcon = !this.flashIcon
        k -= 1
        if (k > 0) {
          setTimeout(() => { flash() }, 140)
        }
      }
      flash()
    }
  }

  get showHamburger () {
    if (this.scheduling || this.rescheduling) {
      return false
    }
    if (this.$route.path === '/queue' && this.citizenInvited) {
      return false
    }
    return true
  }

  get showIcon () {
    if (this.$route.path !== '/queue') {
      if (this.serviceModalForm &&
        this.serviceModalForm.citizen_id &&
        !this.showServiceModal &&
        !this.showAddModal) {
        return { show: true, style: 'warning' }
      }
      return { show: true, style: 'primary' }
    }
    return this.showTimeTrackingIcon ? { show: true, style: 'warning' } : { show: false, style: null }
  }

  get isGAorCSR () {
    if (this.user && this.user.role) {
      // eslint-disable-next-line camelcase
      const { role_code } = this.user.role
      // eslint-disable-next-line camelcase
      if (role_code === 'CSR' || role_code === 'GA') {
        return true
      }
    }
    return false
  }

  get agendaPanelStyle () {
    let classStyle = 'gaScreenUnchecked'
    if (this.showAgendaScreenModal) {
      classStyle = 'gaScreenChecked'
    }
    return classStyle
  }

  get gaPanelStyle () {
    let classStyle = 'gaScreenUnchecked'
    if (this.showGAScreenModal) {
      classStyle = 'gaScreenChecked'
    }
    return classStyle
  }

  get showAdmin () {
    const roles = ['GA', 'ANALYTICS', 'HELPDESK', 'SUPPORT']
    if (this.user && this.user.role && this.user.role.role_code) {
      if (roles.indexOf(this.user.role.role_code) > -1) {
        return true
      }
    }
    return false
  }

  get showSupport () {
    if (this.user && this.user.role && this.user.role.role_code) {
      if (this.user.role.role_code == 'SUPPORT') {
        return true
      }
    }
    return false
  }

  // Is this used?
  toggleTrackingIcon (bool: boolean) {
    if (!bool) {
      this.showSpacer = false
    }
    this.toggleTimeTrackingIcon(bool)
  }

  clickFeedback () {
    this.toggleFeedbackModal(true)
  }

  clickIcon () {
    if (this.showIcon) {
      this.toggleServiceModal(true)
      return
    }
    this.clickAddCitizen()
  }
}

</script>

<style scoped>
.no-border {
  border: none !important;
}
.dash-button-flex-button-container {
  display: flex;
  justify-content: space-between;
  width: 97%;
  padding: 10px;
  margin: 10px;
}
.gaScreenChecked {
  padding-left: 0em;
}
.gaScreenUnchecked {
  padding-left: 1.5em;
}
.tracking-icon {
  font-size: 2.75rem;
  border-radius: 5px;
  box-shadow: -4px 4px 4px 0px grey;
  cursor: pointer;
}
</style>
