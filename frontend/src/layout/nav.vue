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
  <div style="position: relative">
    <div class="dash-button-flex-button-container pb-0 mb-3">
      <!-- SLOT FOR EACH VIEW'S BUTTON CONTROLS-->
      <router-view name="buttons"/>
      <div v-if="calendarSetup"
           style="flex-grow: 8"
           class="q-inline-title">{{ calendarSetup.title }}</div>
    <div />
      <div v-if="navigationVisible">
        <b-dropdown variant="outline-primary"
                    class="pl-0 ml-0 mr-3"
                    boundary="viewport"
                    id="nav-dropdown">
          <template slot="button-content">
            <font-awesome-icon icon="bars"
                               style="font-size: 1.18rem;"/>
          </template>
          <div :style="{width:200+'px'}">
            <b-dropdown-item to="/queue">The Q</b-dropdown-item>
            <b-dropdown-item to="/booking" v-if="showExams">Room Booking</b-dropdown-item>
            <b-dropdown-item v-if="showExams" to="/exams">Exam Admin</b-dropdown-item>
            <b-dropdown-item to="/agenda" v-if="isGAorCSR && showExams">Office Agenda</b-dropdown-item>
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
            <b-dropdown-divider v-if="showAdmin" />
            <b-dropdown-item>
              <b-button class="btn-primary w-100 m-0"
                        v-if="!showServiceModal"
                        @click="clickFeedback"
                        id="click-feedback-button">Feedback</b-button></b-dropdown-item>
            </b-dropdown-item>
          </div>
        </b-dropdown>
      </div>
    </div>
    <!--SLOT FOR EACH VIEW'S MAIN CONTENT-->
    <div style="position: relative">
      <router-view />
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'
  import SchedulingIndicator from '../booking/scheduling-indicator'

  export default {
    name: 'Nav',
    components: { SchedulingIndicator },
    computed: {
      ...mapGetters(['showExams']),
      ...mapState([
        'navigationVisible',
        'showServiceModal',
        'showGAScreenModal',
        'user',
        'calendarSetup',
      ]),
      isGAorCSR() {
        if (this.user && this.user.role) {
          if (this.user.role.role_code === 'CSR' || this.user.role.role_code === 'GA') {
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
    methods: {
      ...mapActions(['clickGAScreen']),
      ...mapMutations(['toggleFeedbackModal']),
      clickFeedback() {
        this.toggleFeedbackModal(true)
      },
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
</style>
