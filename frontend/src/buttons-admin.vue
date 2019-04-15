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
  <b-form autocomplete="off">
    <template v-if="user.role && user.role.role_code==='SUPPORT' ">
      <div style="display: inline-flex;">
        <span style="font-size: 1.4rem; font-weight: 600; margin-right: 1em"> Editing: </span>
        <b-form-select :options="options" @input="handleInput" :value="option" />
      </div>
    </template>
    <template v-else-if="user.role && user.role.role_code==='GA' ">
      <div style="display: inline-flex;">
        <span style="font-size: 1.4rem; font-weight: 600; margin-right: 1em"> Editing: </span>
        <b-form-select :options="optionsGA" @input="handleInput" :value="option" />
      </div>
    </template>
    <template v-else>
      <span style="font-size: 1.4rem; font-weight: 600"> Editing: {{this.name}}</span>
    </template>
  </b-form>
</template>

<script>
  import {  mapActions, mapState } from 'vuex'

  export default {
    name: "ButtonsAdmin",
    data() {
      return {
        option: 'csr',
        options: [
          {value: 'csr', text: 'CSRs'},
          {value: 'office', text: 'ServiceBC Offices'},
          {value: 'channel', text: 'Delivery Channels'},
          {value: 'role', text: 'User roles'},
          {value: 'service', text: 'Provided Services'},
          {value: 'smartboard', text: 'Smartboard Content'},
          {value: 'invigilator', text: 'Invigilators'},
          {value: 'room', text: 'Rooms'},
          {value: 'examtype', text: 'Exam Types'}
        ],
        optionsGA: [
          {value: 'csr', text: 'CSRs'},
          {value: 'invigilator', text: 'Invigilators'},
          {value: 'room', text: 'Rooms'}
        ]
      }
    },
    computed: {
      ...mapState(['user']),
      name() {
        if (this.user && this.user.role && (this.user.role.role_code === 'GA' || this.user.role.role_code === 'HELPDESK')) {
          this.changeAdminView('csr')
          return 'CSRs'
        }
        if (this.user && this.user.role && this.user.role.role_code === 'ANALYTICS') {
          this.changeAdminView('service')
          return 'Services Provided'
        }
      }
    },
    methods: {
      ...mapActions(['changeAdminView']),
      handleInput(e) {
        this.view = e
        this.changeAdminView(e)
      }
    }
  }
</script>

<style scoped>
</style>
