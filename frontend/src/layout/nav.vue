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
  <div class="nav-container">
    <div class="dash-button-flex-button-container pb-0 mb-3">

      <!-- SLOT FOR EACH VIEW'S BUTTON CONTROLS-->
      <router-view name="buttons"/>

      <div v-if="navigationVisible">
        <b-dropdown variant="outline-primary"
                    class="pl-0 ml-0 mr-3"
                    id="nav-dropdown">
          <template slot="button-content">
            <font-awesome-icon icon="bars"
                               style="font-size: 1.18rem;"/>
          </template>
          <div :style="{width:200+'px'}">
            <b-dropdown-item to="/queue">The Q</b-dropdown-item>
            <b-dropdown-item to="/exams">Manage Exams</b-dropdown-item>
            <template  v-if="user.role && user.role.role_code=='GA'">
              <b-dropdown-item @click="clickGAScreen">
                <b-check :checked="showGAScreenModal"><span style="font-weight: 400;">Show GA Panel</span></b-check>
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
    <div style="width: 98%; margin-right: 15px;">
      <router-view />
    </div>

  </div>
</template>

<script>
  import { mapState, mapActions, mapMutations } from 'vuex'
  export default {
    name: 'Nav',
    computed: {
      ...mapState([
        'navigationVisible',
        'showServiceModal',
        'showGAScreenModal',
        'user'
      ]),
      showAdmin() {
        let roles = ['GA', 'ANALYTICS', 'HELPDESK', 'SUPPORT']
        if (this.user && this.user.role && this.user.role.role_code) {
          if (roles.indexOf(this.user.role.role_code) > -1) {
            return true
          }
        }
        return false
      }
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
    display: inline-flex;
    justify-content: space-between;
    width: 97%;
    padding: 10px;
    margin: 10px;
  }
  .add-flex-grow {
    flex-grow: 1;
  }
  .nav-container {
    display: inline;
  }
</style>
