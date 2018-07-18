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
  <b-container>
    <b-row align-v="end">
      <b-col cols="9">
        <h1>
          <img src='./assets/bcid.jpg'/>
          Queue Management
        </h1>
        <b-button @click="showModal()">
          show modal
        </b-button>
        <AddCitizen />
        <Socket/>
      </b-col>
      <b-col cols="3">
        <Login></Login>
      </b-col>
    </b-row>
      <Controls v-if="this.$store.state.isLoggedIn"/>
      <SlackMessage v-if="this.$store.state.isLoggedIn"/>
  </b-container>
</template>

<script>
import Controls from './Controls'
import Login from './Login'
import Socket from './Socket'
import SlackMessage from './SlackMessage'
import AddCitizen from './add-citizen/add-citizen'

export default {
  name: 'App',
  components: { Login, Socket, Controls, SlackMessage, AddCitizen },
  methods: {
    showModal() {
      console.log('this part worked')
      this.$store.dispatch('addCitizen')
    }
  }
}

</script>


