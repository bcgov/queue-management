<!-- /*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/ -->

<template>
  <div class="main-container">
    <v-row>
      <v-col :cols="((isRightMenuEnabled) && (officetype === 'callbyname' || officetype === 'reception')) ? 10 : 12">
        <div class="top-flex-div">
          <div class="flex-title">{{ date }} {{ time }}</div>
        </div>
        <CallByTicket
          v-if="officetype === 'callbyticket'"
          :smartboardData="{ office_number }"
          :networkStatus="{ networkDown }"
        ></CallByTicket>
        <CallByName
          v-else-if="officetype === 'callbyname' || officetype === 'reception'"
          :smartboardData="{ office_number }"
          :networkStatus="{ networkDown }"
          :office="{office}"
          :isMessageEnabled="{isMessageEnabled}"
        ></CallByName>
        <NonReception
          v-else-if="officetype === 'nocallonsmartboard'"
          :smartboardData="{ office_number }"
          :office="{office}"
          :isMessageEnabled="{isMessageEnabled}"
        ></NonReception>

        <div v-else>Please stand by...</div>
        <BoardSocket :smartboardData="{ office_number }"></BoardSocket>
      </v-col>
      <v-col :cols="isRightMenuEnabled ? 2 : ''"  v-if="((officetype === 'callbyname' || officetype === 'reception') && isRightMenuEnabled)">
        <RightMenu
          v-if="(officetype === 'callbyname' || officetype === 'reception')"
          :smartboardData="{ office_number }"
          :networkStatus="{ networkDown }"
          :isRightMenuEnabled="{isRightMenuEnabled}"
        ></RightMenu>
      </v-col>
    </v-row>
    <div v-if="networkDown == true" id="network-status" class="loading small">
    </div>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Component, Prop, Vue } from 'vue-property-decorator'
import Axios from '@/utils/axios'
import BoardSocket from './board-socket.vue'
import CallByName from './call-by-name.vue'
import CallByTicket from './call-by-ticket.vue'
import NonReception from './non-reception.vue'
import RightMenu from './right-menu.vue'
import axios from 'axios'
import config from '../../../config'

@Component({
  components: {
    CallByName,
    CallByTicket,
    BoardSocket,
    NonReception,
    RightMenu
  }
})
export default class Smartboard extends Vue {
  @Prop({ default: '' })
  private office_number!: string

  private tz: any = this.getParameterByName('tz') || Intl.DateTimeFormat().resolvedOptions().timeZone
  networkStatus: string = ''
  date: string = ''

  // return {
  private officetype: string = ''
  private networkDown: boolean = false
  private options: any = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: this.tz
  }

  private timeOpts: any = {
    hour12: true,
    hour: 'numeric',
    minute: '2-digit',
    timeZone: this.tz
  }

  private time: any = ''
  
  private isMessageEnabled: boolean = false
  private isRightMenuEnabled: boolean = false
  private office: any = {}


  get url () {
    return `/smartboard/?office_number=${this.office_number}`
  }

  initializeBoard () {
    // TO DO
    // this.networkStatus = ''

    this.now()
    Axios.get(this.url).then(resp => {
      this.officetype = resp.data.office_type
    })
  }

  now () {
    const d = new Date()
    this.date = d.toLocaleDateString('en-CA', this.options)
    this.time = d.toLocaleTimeString('en-CA', this.timeOpts)
  }

  getParameterByName (name, url = window.location.href) {
    url = window.location.href
    // eslint-disable-next-line no-useless-escape
    name = name.replace(/[\[\]]/g, '\\$&')
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)')
    var results = regex.exec(url)
    if (!results) return null
    if (!results[2]) return ''
    return decodeURIComponent(results[2].replace(/\+/g, ' '))
  }

  created () {
    this.initializeBoard()
  }

  mounted () {
    this.$root.$on('onDigitalSignageMsgUpdate', () => { this.onDigitalSignageMsgUpdate() })
    setInterval(() => { this.now() }, 1000)

    var fetchNetworkStatus = () => {
      axios
        .get('http://localhost/health')
        .then(response => {
          this.networkDown = !response.data.connected
          this.$forceUpdate()

          setTimeout(fetchNetworkStatus, 1000)
        })
    }
    fetchNetworkStatus()

    this.getOffice()
    window.setInterval(() => {
      this.getOffice()
    }, 350000)
  }

  private onDigitalSignageMsgUpdate () {
    this.getOffice()
  }

  private getOffice () {
    this.isMessageEnabled = false
    this.isRightMenuEnabled = false
    const url = '/smardboard/side-menu/'+this.office_number
    Axios.get(url).then(resp => {
      if (resp.data) {
        this.office = resp.data.office
        if (this.office) {
          if(this.office.digital_signage_message == 1) {
            this.isMessageEnabled = true
          }
          if(this.office.currently_waiting == 1) {
            this.isRightMenuEnabled = true
          }
        }
        }
    })
  }
}
</script>

<style>
.main-container {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  margin: 0px;
  text-align: center;
  /* overflow-y: auto; */
}
.top-flex-div {
  height: 11%;
  text-align: center;
  width: 100%;
}
.bottom-flex-div {
  position: relative;
  top: 2px;
  bottom: 10px;
  left: 0;
  text-align: center;
  height: 12%;
  width: 100%;
}
.flex-title {
  font-size: 7.2rem;
  color: darkblue;
  text-shadow: -1px 0 steelblue, 0 1px steelblue, 1px 0 steelblue,
    0 -1px steelblue;
}
.lg-boardtable-head {
  font-size: 2.3rem;
  text-align: center;
  height: 30px;
}
.sm-boardtable-body {
  font-size: 1.8rem;
  text-align: center;
}
.sm-boardtable-head {
  font-size: 1.8rem;
  text-align: center;
}
.lg-boardtable-body {
  font-size: 2.5rem;
  text-align: left;
}
.flashing-ticket {
  color: red;
  font-size: 1rem;
}
.board-content-div {
  background-color: white;
  box-shadow: 2px 3px 10px rgba(0, 0, 0, 0.5);
  text-align: center;
}
.board-table-style {
  width: 100%;
  background-color: white;
  text-align: center;
}
.board-nameticket-video {
  display: inline-block;
  width: 74%;
}
.board-noticket-video {
  display: inline-block;
  width: 85%;
}
.board-25-table {
  display: inline-block;
  width: 24%;
  max-height: 60vh;
  padding-left: 1%;
  padding-right: 1%;
  vertical-align: top;
}
.flex-title {
    font-size: 4rem;
    color: midnightblue;
    margin-top: -4px;
}
.video-js {
  background-color: white;
}

#network-status {
  position: absolute;
  right: 8px;
  bottom: 8px;
}

.loading {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 7px solid rgba(7, 54, 116, 0.3);
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
  border: 7px solid rgb(7, 54, 116);
  border-radius: 50%;
  border-color: rgb(7, 54, 116) transparent transparent transparent;
  width: 64px;
  height: 64px;

  -webkit-animation: spin 1s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.loading.small div {
  width: 32px;
  height: 32px;
}

/* .flex-title-waiting {
  color: midnightblue;
  margin-top: 16px;
  margin-left: -41px;
  font-size: 2.3rem;
} */

.margin-left-container{
  margin-top: 16px;
  margin-left: -176px;
}

.text-font-sz {
  font-size: 1rem;
}

.flex-title-upcomming{
  color: midnightblue;
  margin-top: 16px;
  margin-left: -176px;
  font-size: 1.48rem;
}
.flex-title-waiting{
  color: midnightblue;
  margin-top: 16px;
  margin-left: -176px;
  font-size:2.3rem;
}

.marquee-container {
    background-color: rgb(25, 25, 112);
    margin-top: -119px;
    height: 70px;
    margin-left: 178px;
    margin-right: -183px;
    /* margin-left: -73px;
    margin-right: 66px; */
}

.marquee-ds {
  /* position: absolute; */
  /* left: 50px;
  width: calc(100% - 100px); */
  /* left: 183px;
  width: calc(100% - 219px); */
  height: 70px;
  background-color: rgb(25, 25, 112);
  /* padding: 5px; */
  text-align: center;
}

.marquee-text {
  color: white;
  font-size: 2.8rem;
}

.container-height-menu-half {
  height: 400px !important;
}
.container-height-menu-full {
  height: 900px !important;
}
.container-height-menu-half-bottom{
  height: 50% !important;
}

.margin-push-left {
  margin-left: -60% !important;
}

.marquee-msg-container-full {
    margin-top: 121px;
    padding-left: 33px;
    padding-right: 394px;
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
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}
</style>
