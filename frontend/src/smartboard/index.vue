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
    <CallByTicket v-if="officetype==='callbyticket'"
                  :smartboardData="{office_number}" :networkStatus="{networkDown}"></CallByTicket>
    <CallByName v-else-if="officetype==='callbyname' || officetype==='reception'"
                :smartboardData="{office_number}" :networkStatus="{networkDown}"></CallByName>
    <NonReception v-else-if="officetype==='nocallonsmartboard'"
                :smartboardData="{office_number}"></NonReception>

    <div v-else>Please stand by...</div>
    <BoardSocket :smartboardData="{office_number}"></BoardSocket>

    <div v-if="networkDown==true" id="network-status" class="loading small"><div></div><div></div><div></div><div></div><div></div></div>
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
    setInterval( () => { this.now() }, 1000)

    var fetchNetworkStatus = () => {
      axios
        .get('http://localhost/health')
        .then(response => {
          this.networkDown = !response.data.connected;
          this.$forceUpdate()

          setTimeout(fetchNetworkStatus, 1000);
        })
    }
    fetchNetworkStatus()
  },

  props: ['office_number'],

  components: { CallByName, CallByTicket, BoardSocket, NonReception },

  data() {
    console.log("==> In Index.vue: data")
    let tz = this.getParameterByName("tz")
    console.log("    --> initial tz")
    console.log(tz)
    if (!tz) {
      tz = Intl.DateTimeFormat().resolvedOptions().timeZone
      console.log("    --> updated tz")
      console.log(tz)
    }

    return {
      officetype: '',
      networkDown: false,
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
    url() {
      console.log("==> In index.vue: computed")
      console.log("    --> return: " + `/smartboard/?office_number=${this.office_number}`)
      return `/smartboard/?office_number=${this.office_number}`
    }
  },

  methods: {
    initializeBoard() {
      this.networkStatus = ""

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
      console.log("==> In index.vue: getParameterByName")
      console.log("    --> name:          " + name)
      console.log("    --> url:           " + url)
      url = window.location.href;
      console.log("    --> updated url:   " + url)
      name = name.replace(/[\[\]]/g, '\\$&');
      console.log("    --> updated name:  " + name)
      var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'), results = regex.exec(url);
      console.log("    --> results")
      console.log(results)
      if (!results) return null;
      if (!results[2]) return '';
      console.log("    --> decodeURIComponent")
      console.log(decodeURIComponent(results[2].replace(/\+/g, ' ')))
      return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }
  }
}
</script>

<style>
  .main-container { position: fixed; top: 0; left: 0; height:100%; width: 100%; margin: 0px; text-align: center; }
  .top-flex-div { height:11%; text-align: center; width: 100% }
  .bottom-flex-div { position: relative; top: 2px; bottom: 10px; left: 0; text-align: center; height:12%; width: 100%;}
  .flex-title { font-size: 7.2rem; color: darkblue; text-shadow: -1px 0 steelblue, 0 1px steelblue, 1px 0 steelblue, 0 -1px steelblue }
  .lg-boardtable-head { font-size: 2.3rem; text-align: center; height: 30px }
  .sm-boardtable-body { font-size: 1.8rem; text-align: center }
  .sm-boardtable-head { font-size: 1.8rem; text-align: center }
  .lg-boardtable-body { font-size: 2.5rem; text-align: left }
  .flashing-ticket {color: red; font-size: 1rem }
  .board-content-div { background-color: white; box-shadow: 2px 3px 10px rgba(0, 0, 0, .5); text-align: center; }
  .board-table-style { width: 100%; background-color: white; text-align: center; }
  .board-85-video { display: inline-block; width: 74%; padding-left: 1%; padding-right: 1%; margin: 8px auto 0 auto; }
  .board-25-table { display: inline-block; width: 24%; max-height: 60vh; padding-left: 1%; padding-right: 1%; vertical-align: top; }
  .flex-title { font-size: 4.0rem; color: midnightblue; margin-top: -4px; }
  .video-js { background-color: white; }

  #network-status {
    position: absolute;
    right: 8px;
    bottom: 8px;
  }

  .loading {
    display: inline-block;
    width: 50px;
    height: 50px;
    border: 7px solid rgba(7,54,116,.3);
    border-radius: 50%;
    margin: 14px;
  }

  .loading.small {
    border: none;
    width: 18px;
    height: 18px;
  }

  .loading div {
    box-sizing: border-box;
    display: block;
    position: absolute;
    border: 7px solid rgb(7,54,116);
    border-radius: 50%;
    border-color: rgb(7,54,116) transparent transparent transparent;
    width: 64px;
    height: 64px;
    
    -webkit-animation: spin 1s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  }

  .loading.small div {
    width: 32px;
    height: 32px;
  }

  .loading div:nth-child(1) {
      -webkit-animation-delay: -0.23s;
  }
  .loading div:nth-child(2) {
      -webkit-animation-delay: -0.2s;
  }
  .loading div:nth-child(3) {
      -webkit-animation-delay: -0.15s;
  }
  .loading div:nth-child(4) {
      -webkit-animation-delay: -0.08s;
  }

  @-webkit-keyframes spin {
    0% { -webkit-transform: rotate(0deg); }
    100% { -webkit-transform: rotate(360deg); }
  }

</style>
