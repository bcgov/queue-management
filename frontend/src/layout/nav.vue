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
    <div class="dash-button-flex-button-container pb-0 mb-0">

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
            <!--
            <b-dropdown-item to="/exams">Manage Exams</b-dropdown-item>
            <b-dropdown-item to="/cal">Room Booking</b-dropdown-item>
            <b-dropdown-item>Reporting</b-dropdown-item>
            <b-dropdown-item>GA Panel</b-dropdown-item>
            <b-dropdown-item>Admin Console</b-dropdown-item>
            <b-dropdown-item>My Settings</b-dropdown-item>
            <b-dropdown-item>
              <b-button block class="btn-primary">
                Feedback
              </b-button>
            </b-dropdown-item>-->
          </div>
        </b-dropdown>
      </div>
    </div>

    <!--SLOT FOR EACH VIEW'S MAIN CONTENT-->
    <router-view />

  </div>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: 'Nav',
    computed: {
      ...mapState([
        'navigationVisible',
      ]),
    },
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
