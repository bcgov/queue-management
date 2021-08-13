<!-- /*Copyright 2015 Province of British Columbia

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
  <div v-if="isRightMenuEnabled">
    <div v-if="(!networkStatus.networkDown && (citizenInQ))" class="bottom-flex-div">
      <div class="flex-title-waiting">Currently waiting: {{ waiting }}</div>
    </div>
    <div class="marqueeup">
      <b-container :class="waitingClass">
          <div>
            <b-row  v-for="(each, index) in citizenInQ" :key="each.start_time">
              <b-col>
                <!-- for booked app -->
                <b-button 
                  v-if="each.flag=='booked_app'"
                  variant="success"
                  size="lg"
                  >
                  <font-awesome-icon
                    icon="calendar-alt"
                  />
                </b-button>
                <p  v-if="(each.flag=='booked_app')"><strong>Appointment</strong></p>
                <!-- jus for walkin -->
                <b-button 
                  v-if="((each.flag=='walkin_app')  && (isNew(each)))"
                  variant="info"
                  size="lg"
                  >
                  <font-awesome-icon
                    animation="cylon"
                    icon="walking"
                    pulse 
                  />
                </b-button>
                <p v-if="((each.flag=='walkin_app') && (isNew(each)))"><strong>Walk In</strong></p>
                <!-- walk in   -->
                <b-button 
                  v-if="((each.flag=='walkin_app') && !(isNew(each)))"
                  variant="info"
                  size="lg"
                  >
                  <font-awesome-icon
                    animation="cylon"
                    icon="walking"
                  />
                </b-button>
                <p v-if="((each.flag=='walkin_app') && !(isNew(each)))"><strong>Walk In</strong></p>
              </b-col>
              <b-col>
                <b-card bg-variant="success" text-variant="white"  v-if="each.flag=='booked_app'">
                  <b-card-text
                    class="text-font-sz"
                    align="center"
                    justify="center">
                    {{index+1}}
                  </b-card-text>
                </b-card>
                <b-card bg-variant="info" text-variant="white" v-else>
                  <b-card-text
                    class="text-font-sz"
                    align="center"
                    justify="center">
                    {{index+1}}
                  </b-card-text>
                </b-card>
              </b-col>
            </b-row>
        </div>
      </b-container>
      </div>
      <div v-if="(!networkStatus.networkDown && (bookedNotcheckIn.length > 0))" class="bottom-flex-div">
        <div class="flex-title-upcomming"> Upcoming Appointments:</div>
      </div>
      <div class="marqueeup">
      <b-container class="container-height-menu-half-bottom">
        <div>
          <b-row v-for="each in bookedNotcheckIn" :key="each.start_time">
            <b-col>
              <b-button 
                variant="secondary"
                size="lg"
                >
                <font-awesome-icon
                  icon="calendar-alt"
                />
              </b-button>
              <p><strong>Appointment</strong></p>
            </b-col>
            <b-col>
              <b-card bg-variant="dark" text-variant="white">
                <b-card-text class="text-font-sz">
                  <strong>{{getAppTime(each)}}</strong>
                </b-card-text>
              </b-card>
            </b-col>
          </b-row>
      </div>
      </b-container>
    </div>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Component, Prop, Vue } from 'vue-property-decorator'

// import axios from 'axios'
import Axios from '@/utils/axios'
import Video from './video.vue'
import config from '../../../config'

@Component({
  components: {
    Video
  }
})
export default class RightMenu extends Vue {
  @Prop({ default: '' })
  private smartboardData!: any

  @Prop({ default: '' }) office_number!: string

  @Prop({ default: '' })
  private networkStatus!: string

  @Prop({ default: false })
  private isRightMenuEnabled!: boolean

  private citizens: any = ''
  private officeType: string = ''
  private maxVideoHeight: string | number = ''
  private citizenInQ: any = []
  private bookedNotcheckIn: any = []

  get url () {
    return `/smartboard/?office_number=${this.smartboardData.office_number}`
  }

  get waiting () {
    if (this.citizens && this.citizens.length > 0) {
      return this.citizens.filter(c => c.active_period.ps.ps_name === 'Waiting').length
    }
    return 0
  }

  get waitingClass () {
    if ((this.citizenInQ.length > 0) && (this.bookedNotcheckIn.length > 0)) {
      return 'container-height-menu-half'
    } else if ((this.citizenInQ.length > 0) && (this.bookedNotcheckIn.length == 0)) {
      return 'container-height-menu-full'
    } else {
      return 'container-height-menu-half'
    }
  }

  initializeBoard () {
    Axios.get(this.url).then(resp => {
      this.officeType = resp.data.office_type
      this.citizens = resp.data.citizens
      // TODO check can't see  this.office_id Declared . so commented
      // this.$root.$emit('boardConnect', this.office_id)
      // so change to below line to get office id
      this.$root.$emit('boardConnect', { office_id: this.smartboardData && this.smartboardData.office_number })
    })
  }

  updateBoard (ticketId) {
    Axios.get(this.url).then(resp => {
      this.citizens = resp.data.citizens
    })
    this.getAllData()
  }

  getAllData () {
    this.getCurrentlyWaiting()
    this.getUpcomming()
  }

  getCurrentlyWaiting () {
    const url = '/smardboard/Q-details/waiting/'+this.smartboardData.office_number
    Axios.get(url).then(resp => {
      if (resp.data) {
        this.citizenInQ = resp.data.citizen_in_q
        this.citizenInQ = this.citizenInQ.filter(c => c.service_name !== 'Back Office')
      }
    })
  }

  getUpcomming () {
    const url = '/smardboard/Q-details/upcoming/'+this.smartboardData.office_number
    Axios.get(url).then(resp => {
      if (resp.data) {
        this.bookedNotcheckIn = resp.data.booked_not_checkin
      }
    })
  }

  // TODO check event param
  // event
  handleResize () {
    this.maxVideoHeight = document.documentElement.clientHeight * 0.8
  }

  mounted () {
    this.$root.$on('addToBoard', (data) => { this.updateBoard(data) })
    this.initializeBoard()
    this.handleResize()
    window.addEventListener('resize', this.handleResize)
    window.setInterval(() => {
      this.getUpcomming()
    }, 60000)
  }

  created () {
    this.getAllData()
  }

  private getAppTime (Q) {
    if (Q.start_time) {
      return new Date(Q.start_time).toLocaleTimeString().replace(/:\d{2}\s/,' ');
    }
    return Q.start_time
  }

  private isNew (Q) {
    if (Q.created_at) {
      var t1 = new Date(Q.created_at);
      var t2 = new Date();
      var dif = t1.getTime() - t2.getTime();

      var Seconds_from_T1_to_T2 = dif / 1000;
      var Seconds_Between_Dates = Math.abs(Seconds_from_T1_to_T2);
      if ((Seconds_Between_Dates/60) <= 3) {
        return true
      }else{
        return false
      }
    }
    return false
  }
}
</script>