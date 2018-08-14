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
    <CallByNumber v-if="officetype==='callbynumber'"></CallByNumber>
    <CallByName v-else-if="officetype==='callbyname' || officetype==='reception'"></CallByName>
    <NonReception v-else-if="officetype==='nonreception'"></NonReception>
    <div v-else>Please stand by</div>
    <BoardSocket></BoardSocket>
  </div>
</template>

<script>
import BoardSocket from './board-socket'
import CallByNumber from './callbynumber'
import CallByName from './callbyname'
import NonReception from './nonreception'
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

  components: { CallByName, CallByNumber, BoardSocket, NonReception },

  data() {
    return {
      officetype: ''
    }
  },

  computed: {
    office_id() {
      let path = window.location.pathname.split('/')
      if (path.length >= 3) {
        return path[2]
      } else {
        return 'notfound'
      }
    },
    url() {
      return `/smartboard/?office_number=${this.office_id}`
    }
  },

  methods: {
    initializeBoard() {
      Axios.get(this.url).then( resp => {
        this.officetype = resp.data.office_type
      })
    }
  }
}
</script>

<style>
  .board-footer-div { display: flex; position: fixed; bottom: 0; left: 0; margins: 0px; height:13%; width: 100%; justify-content: flex-start; align-items: center; font-size:2.2em; }
  .board-video-div { left: 0px; top: 0px; height: 504px; width: 896px; background-color: white; box-shadow: 2px 3px 10px rgba(0, 0, 0, .5); }
  .board-video-div-2 { left: 0px; top: 0px; height: 605px; width: 1075px; background-color: white; box-shadow: 2px 3px
  10px rgba(0, 0, 0, .5); }
  .board-75-video { width: 75%; height: 100%; }
  .main-container { position: fixed; top: 0; left: 0; height:100%; width: 100%; margin: 0px; background:linear-gradient(lemonchiffon,lightskyblue) }
  .top-flex-div { display: flex; height:12%; justify-content: center; align-items: center; width: 100% }
  .flex-title { font-size: 3.6em; color: darkblue;
    text-shadow: -1px 0 steelblue, 0 1px steelblue, 1px 0 steelblue, 0 -1px steelblue }
  .lg-boardtable-head { font-size: 2.3em; text-align: center; height: 30px }
  .sm-boardtable-body { font-size: 1.8em; text-align: center }
  .sm-boardtable-head { font-size: 1.8em; text-align: center }
  .lg-boardtable-body { font-size: 2.5em; text-align: left }
  .flashing-ticket {color: red; font-size: 1em }
  .board-video-div { left: 0px; top: 0px; height: 504px; width: 896px; background-color: white; box-shadow: 2px 3px 10px rgba(0, 0, 0, .5); }
  .board-content-div { background-color: white; box-shadow: 2px 3px 10px rgba(0, 0, 0, .5); }
  .board-table-style { width: 100%; background-color: white; text-align: center; }
  .board-75-video { width: 75%; height: 100%; padding-left: 3%}
  .board-25-table { width: 25%; height: 100%; padding-right: 3%;}
  .testclass {height: 20px;}
  .flex-title-2 { font-size: 2.0em; color: midnightblue}
</style>
