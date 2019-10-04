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
  <div>
    <div style="display: flex; flex-direction: row; justify-content: space-between">
      <div></div>
      <div v-if="reception">
        <h5>Citizens Waiting</h5>
        <h6>{{ this.ga_citizens_waiting() }}</h6>
      </div>
      <div v-if="!reception">
        <h5>Citizens on Hold</h5>
        <h6>{{ this.ga_citizens_on_hold() }}</h6>
      </div>
      <div>
        <h5>Total CSRs</h5>
        <h6>{{ this.ga_total_csrs() }}</h6>
      </div>
      <div>
        <h5>Serving CSRs</h5>
        <h6>{{ this.ga_serving_csrs() }}</h6>
      </div>
      <div></div>
    </div>
    <!--<div>-->
      <!--The time is now: {{time_now}}-->
    <!--</div>-->
    <b-table small
             head-variant="light"
             :items="this.computed_csrs()"
             :fields="fields"
             outlined
             class="p-0 m-0 w-100">

        <template slot="end_service" slot-scope="data" v-if="data.value">
            <button @click.stop="clickEnd(data.value.id)" class="ga-close btn btn-secondary btn-sm">
                {{data.value.label}}
            </button>
        </template>

    </b-table>
  </div>
</template>

<script>

import moment from 'moment'
import {
  mapState, mapGetters, mapActions
}
from 'vuex'

export default {
  name: 'GAScreen',

  mounted() {
    this.interval = setInterval(this.time, 1000);
  },

  beforeDestroy() {
    clearInterval(this.interval)
  },

  data() {
    return {
      fields: [
        {
          key: 'username',
          label: 'Staff Member',
          sortable: true
        },
        {
          key: 'service_request.service.service_name',
          label: 'Service',
          sortable: true
        },
        {
          key: 'wait_time',
          label: 'Wait Time',
          sortable: true
        },
        {
          key: 'serving_time',
          label: 'Serving Time',
          sortable: true,
        },
        {
          key: 'citizen.citizen_comments',
          label: 'Comments',
          sortable: true,
          formatter: (value) => { return value }
        },
        {
            key: 'end_service',
            label: 'End Service'
        }
      ],
      time_now: 'Sometime',
      timer: null
    }
  },
  computed: {
    ...mapState(['showGAScreenModal', 'csrs', 'citizens', 'csr_states']),
    ...mapGetters(['citizens_queue', 'on_hold_queue', 'reception']),
    sortedCsrs() {
      return this.csrs.sort(function(a,b) {
                                            if (a.username < b.username) return -1;
                                            else if (a.username === b.username) return 0;
                                            else return 1;});
    }
  },
  methods: {
    ...mapActions(['closeGAScreenModal', 'getCsrs', 'finishServiceFromGA']),
    time() {
      // this.time_now = new Date();
      // this.time_now = moment().format();
      this.time_now = moment.utc()
    },
    clickEnd(citizen_id){
        this.finishServiceFromGA(citizen_id)
    },
    ga_citizens_waiting() {
      return this.citizens_queue.length
    },
    ga_citizens_on_hold() {
      return this.on_hold_queue.length
    },
    ga_total_csrs() {
      return this.csrs.length
    },
    ga_serving_csrs() {
      let serving_csrs = []
      this.citizens.forEach(c => {
        c.service_reqs.forEach(sr => {
          sr.periods.forEach(p => {
            if (p.time_end === null) {
              if (p.ps.ps_name === 'Invited' || p.ps.ps_name === 'Being Served') {
                if (serving_csrs.indexOf(p.csr_id) === -1) {
                  serving_csrs.push(p.csr_id)
                }
              }
            }
          })
        })
      })
      return serving_csrs.length
    },
    get_citizen_for_csr(csr) {
      for(let i = 0; i < this.citizens.length; i++) {
        for(let j = 0; j < this.citizens[i].service_reqs.length; j++) {
          let activePeriod = this.citizens[i].service_reqs[j].periods.filter(p => p.time_end === null)[0]
          if (activePeriod && (activePeriod.ps.ps_name === 'Invited' || activePeriod.ps.ps_name === 'Being Served') && activePeriod.csr_id === csr.csr_id) {
            return this.citizens[i]
          }
        }
      }

      return null
    },
    computed_csrs() {
      let computed_csrs = []
      // let currentDate = new Date()
      let currentDate = this.time_now;
      const breakStateID = this.csr_states['Break'];
      // console.log("==> Sorted CSRs in computed_csrs");
      // this.sortedCsrs.forEach(csr => {
      //   console.log("    --> CSR name: " + csr.username)
      // });
      // console.log("==> Processing CSRs")
      this.sortedCsrs.forEach(csr => {
        let activeCitizen = this.get_citizen_for_csr(csr)
        if ((csr.csr_state.csr_state_name !== "Logout") || (activeCitizen !== null)) {
          // console.log("    --> Logged in or active citizen: Csr: " + csr.username + "; State: " + csr.csr_state.csr_state_name);

          if (activeCitizen === null) {

            csr.csr_state_id === breakStateID ? csr['wait_time'] = 'ON BREAK' : csr['wait_time'] = null;
            csr['serving_time'] = null
            csr['citizen'] = null
            csr['service_request'] = null
            csr['end_service'] = null
            computed_csrs.push(csr)
          } else {
            let activeServiceRequest = activeCitizen.service_reqs.filter(sr => sr.periods.some(p => p.time_end === null))[0]

            // Add Wait time and Serve time when service begins
            if (activeCitizen.service_reqs[0].periods.filter(p => p.ps.ps_name === "Being Served")[0]) {
              let firstServedPeriod = activeCitizen.service_reqs[0].periods.filter(p => p.ps.ps_name === "Being Served")[0]
              let citizenStartDate = new Date(activeCitizen.start_time)
              let firstServedPeriodDate = new Date(firstServedPeriod.time_start)

              // console.log("==> Periods for Active Service Request: " + activeServiceRequest.service.service_name);
              let timeServeClosed = 0
              // console.log("==> timeServeClosed")
              // console.log(timeServeClosed)
              // console.log(timeServeClosed.toString())
              let timeServeOpen = timeServeClosed
              activeServiceRequest.periods.forEach(p => {
                // console.log("    --> Name: " + p.ps.ps_name + "; Start: " + p.time_start.toString() + "; End: " + (p.time_end === null ? "N/A" : p.time_end.toString()));
                if (p.ps.ps_name === "Being Served") {
                  if (p.time_end != null) {
                    let dateEnd = new Date(p.time_end)
                    let dateStart = new Date(p.time_start)
                    // console.log("        --> Being served, done. Served: " + timeServeClosed.toString() + "; Added: " + (p.time_end - p.time_start).toString())
                    // console.log("        --> Being served, done. dateEnd: " + dateEnd.toString() + "; dateStart: " + dateStart.toString())
                    // console.log("        --> Being served, done. Served: " + timeServeClosed.toString() + "; Added: " + (dateEnd - dateStart).toString())
                    timeServeClosed = timeServeClosed + (dateEnd - dateStart)
                  } else {
                    let dateStart = new Date(p.time_start)
                    timeServeOpen = Math.max(0, currentDate - dateStart)
                    // console.log("        --> Being served, active. Time Started: " + p.time_start.toString() + "; Time Open: " + timeServeOpen.toString())
                  }
                }
              })
              let waitSeconds = (firstServedPeriodDate - citizenStartDate) / 1000
              // console.log("==> waitSeconds");
              // console.log(waitSeconds);
              // console.log("==> serveClosed");
              // console.log(timeServeClosed);
              // console.log("==> serveOpen")
              // console.log(timeServeOpen)
              let timeServeTotal = (timeServeClosed + timeServeOpen)
              // console.log("==> serveTotal")
              // console.log(timeServeTotal)

              let waitDate = new Date(null)
              waitDate.setSeconds(waitSeconds)
              // let sd = new Date(null)
              // sd.setSeconds(serveClosed)
              // serveClosed = (currentDate - firstServedPeriodDate) / 1000

              let serveDate = new Date(null)
              serveDate.setSeconds(timeServeTotal / 1000)
              // console.log("            ==> Wait: " + `${waitDate.getUTCHours()}:${waitDate.getMinutes()}:${waitDate.getSeconds()}`
              //                        + "; Serve: " + `${serveDate.getUTCHours()}:${serveDate.getMinutes()}:${serveDate.getSeconds()}`)
              // csr['wait_time'] = `${waitDate.getUTCHours()}h ${waitDate.getMinutes()}min`
              // csr['serving_time'] = `${serveDate.getUTCHours()}h ${serveDate.getMinutes()}min`
              csr['wait_time'] = `${waitDate.getUTCHours()}h ${waitDate.getMinutes()}m ${waitDate.getSeconds()}s`
              csr['serving_time'] = `${serveDate.getUTCHours()}h ${serveDate.getMinutes()}m ${serveDate.getSeconds()}s`
            } else {
              csr['wait_time'] = null
              csr['serving_time'] = null
            }

            csr['citizen'] = activeCitizen
            csr['service_request'] = activeServiceRequest
            csr['end_service'] = {label: 'End Service', id: activeCitizen.citizen_id}
            computed_csrs.push(csr)
          }
        }
      });

      this.sortedCsrs.forEach(csr => {
        if (csr.csr_state.csr_state_name === "Logout") {
          // console.log("    --> Logged out: csr: " + csr.username + "; State: " + csr.csr_state.csr_state_name);

          csr['wait_time'] = 'Logout';
          csr['serving_time'] = null
          csr['citizen'] = null
          csr['service_request'] = null
          csr['end_service'] = null
          computed_csrs.push(csr)
        }
      });

      return computed_csrs
    },
    fetch_csrs() {
      this.getCsrs()
    }
  }
}

</script>

<style>
td {
    vertical-align: middle;
}
.ga-close {
    font-size: 13px;
}
</style>

