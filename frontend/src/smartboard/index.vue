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
  <div class="main-container">
    <div class="top-flex-div">
      <div class="flex-title">{{ date }} {{ time }}</div>
    </div>
    <CallByTicket v-if="officetype==='callbyticket'"></CallByTicket>
    <CallByName v-else-if="officetype==='callbyname' || officetype==='reception'"></CallByName>
    <NonReception v-else-if="officetype==='nocallonsmartboard'"></NonReception>
    <div v-else>Please stand by...</div>
    <BoardSocket></BoardSocket>
  </div>
</template>

<script>
import BoardSocket from './board-socket'
import CallByTicket from './call-by-ticket'
import CallByName from './call-by-name'
import NonReception from './non-reception'
import axios from 'axios'

const Axios = axios.create({
  baseURL: process.env.API_URL,
  withCredentials: true,
  headers: {
    'Accept': 'application/json'
  }
})

export default {
  name: 'Smartboard',

  created() {
    this.initializeBoard()
  },

  mounted() {
    setInterval( () => { this.now() }, 3000)
  },

  components: { CallByName, CallByTicket, BoardSocket, NonReception },

  data() {
    let tz = this.getParameterByName("tz")
    if (!tz) {
      tz = Intl.DateTimeFormat().resolvedOptions().timeZone
    }

    return {
      officetype: '',
      options: {
        weekday:'long',
        year:'numeric',
        month:'long',
        day:'numeric',
        timeZone: tz
      },
      timeOpts: {
        hour12: true,
        hour: 'numeric',
        minute: '2-digit',
        timeZone: tz
      },
      time: ''
    }
  },

  computed: {
    office_number() {
      let path = window.location.pathname.split('/')
      if (path.length >= 3) {
        return path[2]
      } else {
        return 'notfound'
      }
    },
    url() {
      return `/smartboard/?office_number=${this.office_number}`
    }
  },

  methods: {
    initializeBoard() {
      this.now()
      Axios.get(this.url).then( resp => {
        this.officetype = resp.data.office_type
      })
    },
    now() {
      let d = new Date()
      this.date = d.toLocaleDateString('en-CA', this.options)
      this.time = d.toLocaleTimeString('en-CA', this.timeOpts)
    },
    getParameterByName(name, url) {
      if (!url) url = window.location.href;

      name = name.replace(/[\[\]]/g, '\\$&');
      var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'), results = regex.exec(url);
      if (!results) return null;
      if (!results[2]) return '';
      return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }
  }
}
</script>

<style>
  .main-container { position: fixed; top: 0; left: 0; height:100%; width: 100%; margin: 0px; }
  .top-flex-div { display: flex; height:11%; justify-content: center; align-items: center; width: 100% }
  .bottom-flex-div { display: flex; height:11%; justify-content: center; align-items: center; width: 100%; padding-top: 2%}
  .flex-title { font-size: 7.2rem; color: darkblue; text-shadow: -1px 0 steelblue, 0 1px steelblue, 1px 0 steelblue, 0 -1px steelblue }
  .lg-boardtable-head { font-size: 2.3rem; text-align: center; height: 30px }
  .sm-boardtable-body { font-size: 1.8rem; text-align: center }
  .sm-boardtable-head { font-size: 1.8rem; text-align: center }
  .lg-boardtable-body { font-size: 2.5rem; text-align: left }
  .flashing-ticket {color: red; font-size: 1rem }
  .board-content-div { background-color: white; box-shadow: 2px 3px 10px rgba(0, 0, 0, .5); }
  .board-table-style { width: 100%; background-color: white; text-align: center; }
  .board-85-video { width: 82%; max-height: 60vh; padding-left: 1%; padding-right: 1%;}
  .board-25-table { width: 25%; max-height: 60vh; padding-left: 1%; padding-right: 1%;}
  .flex-title { font-size: 4.0rem; color: midnightblue }
</style>
