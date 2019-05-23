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
  <div style="">
    <div class="dash-button-flex-button-container pb-0 mb-3">
      <!-- SLOT FOR EACH VIEW'S BUTTON CONTROLS-->
      <div style="width: 75px" v-show="$route.path !=='/queue' || showTimeTrackingIcon">
      <b-button :variant="showIcon.style"
                  v-if="showIcon.show"
                  v-show="flashIcon"
                  class="mr-3"
                  @click="clickIcon">
          <font-awesome-icon icon="stopwatch"
                             style="font-size: 1.0rem;color: white;"
                             class="p0"
                             id="booking_time_tracking"/>
        </b-button>
      </div>
      <router-view name="buttons"></router-view>

      <div v-if="calendarSetup && (this.$route.path === '/booking' || this.$route.path === '/agenda')"
           style="flex-grow: 8"
           class="q-inline-title">{{ calendarSetup.title }}</div>
    <div />
      <div v-if="!scheduling && !rescheduling && !citizenInvited">
        <b-dropdown variant="outline-primary"
                    class="pl-0 ml-0 mr-3"
                    right
                    id="nav-dropdown">
          <template slot="button-content">
            <font-awesome-icon icon="bars"
                               style="font-size: 1.18rem;"/>
          </template>
          <div :style="{width:200+'px'}"
               id="nav-dropdown-buttons">
            <b-dropdown-item to="/queue" id="the_q">The Q</b-dropdown-item>
            <b-dropdown-item to="/booking" v-if="showExams" id="room_bookings">Room Booking</b-dropdown-item>
            <b-dropdown-item to="/appointments" v-if="showAppointments" id="appointments">Appointments</b-dropdown-item>
            <b-dropdown-item to="/exams" v-if="showExams" id="exam_inventory">Exam Inventory</b-dropdown-item>
            <b-dropdown-item to="/agenda" v-if="isGAorCSR && showExams" id="office_agenda">Office Agenda</b-dropdown-item>
            <template  v-if="user.role && user.role.role_code=='GA'">
              <b-dropdown-item @click="clickGAScreen" :class="gaPanelStyle">
                <font-awesome-icon v-if="showGAScreenModal"
                                   icon="check"
                                   class="m-0 p-0"
                                   style="padding-left: .25em !important; padding-top: 2px !important" />
                <span style="font-weight: 400;">Show GA Panel</span>
              </b-dropdown-item>
              <b-dropdown-divider />
            </template>
            <b-dropdown-item v-if="showAdmin" to="/admin">Administration</b-dropdown-item>
            <b-dropdown-item v-if="showAdmin" @click="clickRefresh">Refresh</b-dropdown-item>
            <b-dropdown-divider v-if="showAdmin" />
            <b-dropdown-item>
              <b-button class="btn-primary w-100 m-0"
                        v-if="!showServiceModal"
                        @click="clickFeedback"
                        id="click-feedback-button">Feedback</b-button>
            </b-dropdown-item>
          </div>
        </b-dropdown>
      </div>
    </div>
    <!--SLOT FOR EACH VIEW'S MAIN CONTENT-->
    <div style="position: relative; min-height: 400px;">
      <router-view />
    </div>
    <AddCitizen />
    <ServeCitizen v-if="showServiceModal"/>
  </div>
</template>

<script>
  import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'
  import ServeCitizen from '../serve-citizen/serve-citizen'
  import AddCitizen from '../add-citizen/add-citizen'

  export default {
    name: 'Nav',
    components: { AddCitizen, ServeCitizen },
    data() {
      return {
        flashIcon: true,
        showSpacer: false,
      }
    },
    computed: {
      ...mapGetters([ 'showExams', 'showAppointments', ]),
      ...mapState([
        'citizenInvited',
        'showServiceModal',
        'calendarSetup',
        'rescheduling',
        'scheduling',
        'serviceModalForm',
        'serviceBegun',
        'showGAScreenModal',
        'showServiceModal',
        'showTimeTrackingIcon',
        'showAddModal',
        'user',
      ]),
      showIcon() {
        if (this.$route.path !== '/queue') {
          if ( this.serviceModalForm &&
            this.serviceModalForm.citizen_id &&
            !this.showServiceModal &&
            !this.showAddModal ) {
            return { show: true, style: 'warning' }
          }
          return { show: true, style: 'primary'}
        }
        return this.showTimeTrackingIcon ? {show: true, style: 'warning'} : { show: false, style: null}
      },
      isGAorCSR() {
        if (this.user && this.user.role) {
          let { role_code } = this.user.role
          if (role_code === 'CSR' || role_code === 'GA' ) {
            return true
          }
        }
        return false
      },
      gaPanelStyle() {
        let classStyle = 'gaScreenUnchecked'
        if (this.showGAScreenModal) {
          classStyle = 'gaScreenChecked'
         }
         return classStyle
      },
      showAdmin() {
        let roles = ['GA', 'ANALYTICS', 'HELPDESK', 'SUPPORT']
        if (this.user && this.user.role && this.user.role.role_code) {
          if (roles.indexOf(this.user.role.role_code) > -1) {
            return true
          }
        }
        return false
      },
    },
    watch: {
      showIcon(newV, oldV) {
        if (this.$route.path === '/queue' && newV.show && !oldV.show) {
          this.showSpacer = true
          let k = 4
          let flash = () => {
            this.flashIcon = !this.flashIcon
            k -= 1
            if (k > 0) {
              setTimeout(() => { flash()}, 140 )
            }
          }
          flash()
        }
      }
    },
    methods: {
      ...mapActions(['clickGAScreen', 'clickAddCitizen', 'clickRefresh']),
      ...mapMutations(['toggleFeedbackModal', 'toggleServiceModal', 'toggleTrackingIcon', ]),
      toggleTrackingIcon(bool) {
        if (!bool) {
          this.showSpacer = false
        }
        this.toggleTimeTrackingIcon(bool)
      },
      clickFeedback() {
        this.toggleFeedbackModal(true)
      },
      clickIcon() {
        if (this.showIcon) {
          this.toggleServiceModal(true)
          return
        }
        this.clickAddCitizen()
      }
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
  .add-flex-grow {
    flex-grow: 1;
  }
  .gaScreenChecked {
    padding-left: 0em
  }
  .gaScreenUnchecked {
    padding-left: 1.5em
  }
  .tracking-icon {
    font-size: 2.75rem;
    border-radius: 5px;
    box-shadow: -4px 4px 4px 0px grey;
    cursor: pointer;
  }
</style>
