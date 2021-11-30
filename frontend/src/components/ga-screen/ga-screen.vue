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
    <div
      style="display: flex; flex-direction: row; justify-content: space-between"
    >
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
    <b-table
      small
      head-variant="light"
      :items="this.computed_csrs()"
      :fields="fields"
      outlined
      class="p-0 m-0 w-100"
    >
      <template #cell(end_service)="data">
        <button v-if="data.value"
          @click.stop="clickEnd(data.value.id)"
          class="ga-close btn btn-secondary btn-sm"
        >
          {{ data.value.label }}
        </button>
      </template>
    </b-table>
  </div>
</template>
<script lang="ts">
// /* eslint-disable */
import { Action, Getter, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

import moment from 'moment'

@Component({})
export default class GAScreen extends Vue {
  @State('showGAScreenModal') private showGAScreenModal!: any
  @State('csrs') private csrs!: any
  @State('citizens') private citizens!: any
  @State('csr_states') private csr_states!: any

  @Getter('citizens_queue') private citizens_queue!: any;
  @Getter('on_hold_queue') private on_hold_queue!: any;
  @Getter('reception') private reception!: any;

  @Action('closeGAScreenModal') public closeGAScreenModal: any
  @Action('getCsrs') public getCsrs: any
  @Action('finishServiceFromGA') public finishServiceFromGA: any

  private fields: any = [
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
      sortable: true
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
  ]

  private time_now: any = 'Sometime'
  private timer: any = null
  interval: any

  get sortedCsrs () {
    return this.csrs.sort(function (a, b) {
      if (a.username < b.username) return -1
      else if (a.username === b.username) return 0
      else return 1
    })
  }

  public time () {
    this.time_now = moment.utc()
  }

  public clickEnd (citizen_id) {
    this.finishServiceFromGA(citizen_id)
  }

  public ga_citizens_waiting () {
    return this.citizens_queue.length
  }

  public ga_citizens_on_hold () {
    return this.on_hold_queue.length
  }

  public ga_total_csrs () {
    return this.csrs.length
  }

  public ga_serving_csrs () {
    const serving_csrs: any = []
    this.citizens.forEach(c => {
      c.service_reqs.forEach(sr => {
        sr.periods.forEach((p: any) => {
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
  }

  public get_citizen_for_csr (csr) {
    for (const citz of this.citizens) {
      for (const servReq of citz.service_reqs) {
        const activePeriod = servReq.periods.filter(p => p.time_end === null)[0]
        if (activePeriod &&
          (activePeriod.ps.ps_name === 'Invited' || activePeriod.ps.ps_name === 'Being Served') && activePeriod.csr_id === csr.csr_id) {
          return citz
        }
      }
    }

    return null
  }

  public computed_csrs () {
    const computed_csrs: any = []
    const inactive_csrs: any = []
    const currentDate = this.time_now
    const breakStateID = this.csr_states.Break
    this.sortedCsrs.forEach(csr => {
      const activeCitizen = this.get_citizen_for_csr(csr)
      if (activeCitizen === null) {
        csr.csr_state_id === breakStateID ? csr.wait_time = 'ON BREAK' : csr.wait_time = null
        csr.serving_time = null
        csr.citizen = null
        csr.service_request = null
        csr.end_service = null

        if (csr.csr_state_id === breakStateID) { computed_csrs.push(csr) } else { inactive_csrs.push(csr) }
      } else {
        const activeServiceRequest = activeCitizen.service_reqs.filter(sr => sr.periods.some(p => p.time_end === null))[0]

        //  Need to sort Service Requests by ID, to get first one, for wait time.
        //  Can't do directly, as seems to lead to infinite loop.  Put SRs in separate array.
        const srs: any = []
        activeCitizen.service_reqs.forEach(sr => {
          srs.push(sr)
        })
        const sortedSRs = srs.sort(function (a, b) {
          if (a.sr_id < b.sr_id) return -1
          else if (a.sr_id === b.sr_id) return 0
          else return 1
        })

        if (activeCitizen.service_reqs[0].periods.filter(p => p.ps.ps_name === 'Being Served')[0]) {
          const waitPeriods = sortedSRs[0].periods.filter(p => p.ps.ps_name === 'Waiting')
          // TODO check functionality
          const waitDate: any = new Date(0)
          if (waitPeriods.length !== 0) {
            const waitStart: any = new Date(waitPeriods[0].time_start)
            const waitEnd: any = new Date(waitPeriods[0].time_end)
            const waitTime = waitEnd - waitStart
            waitDate.setSeconds(waitTime / 1000)
          }
          const firstServedPeriod = sortedSRs[0].periods.filter(p => p.ps.ps_name === 'Being Served')[0]
          const citizenStartDate: any = new Date(activeCitizen.start_time)
          const firstServedPeriodDate: any = new Date(firstServedPeriod.time_start)
          let timeServeClosed = 0
          let timeServeOpen = timeServeClosed
          activeServiceRequest.periods.forEach(p => {
            if (p.ps.ps_name === 'Being Served') {
              if (p.time_end != null) {
                const dateEnd: any = new Date(p.time_end)
                const dateStart: any = new Date(p.time_start)
                timeServeClosed = timeServeClosed + (dateEnd - dateStart)
              } else {
                const dateStart: any = new Date(p.time_start)
                timeServeOpen = Math.max(0, currentDate - dateStart)
              }
            }
          })
          const waitSeconds: any = (firstServedPeriodDate - citizenStartDate) / 1000
          const timeServeTotal = (timeServeClosed + timeServeOpen)
          // TODO check functionality
          const serveDate = new Date(0)
          serveDate.setSeconds(timeServeTotal / 1000)
          csr.wait_time = `${waitDate.getUTCHours()}h ${waitDate.getMinutes()}m ${waitDate.getSeconds()}s`
          let serveTime = ''
          if (!isNaN(serveDate.getUTCHours())) {
            serveTime = `${serveDate.getUTCHours()}h ${serveDate.getMinutes()}m ${serveDate.getSeconds()}s`
          }
          csr.serving_time = serveTime
        } else {
          csr.wait_time = null
          csr.serving_time = null
        }

        csr.citizen = activeCitizen
        csr.service_request = activeServiceRequest
        csr.end_service = { label: 'End Service', id: activeCitizen.citizen_id }
        computed_csrs.push(csr)
      }
    })

    //  Add inactive CSRs to bottom of list of computed CSRs.
    inactive_csrs.forEach(csr => {
      computed_csrs.push(csr)
    })

    return computed_csrs
  }

  public fetch_csrs () {
    this.getCsrs()
  }

  mounted () {
    this.interval = setInterval(this.time, 1000)
  }

  beforeDestroy () {
    clearInterval(this.interval)
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
