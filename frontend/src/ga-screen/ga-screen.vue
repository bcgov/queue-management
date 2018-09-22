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
    <b-table small
             head-variant="light"
             :items="this.computed_csrs()"
             :fields="fields"
             outlined
             class="p-0 m-0 w-100">
    </b-table>
  </div>
</template>

<script>

import {
  mapState, mapGetters, mapActions
}
from 'vuex'

export default {
  name: 'GAScreen',

  mounted() {
    this.fetch_csrs()
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
          key: 'citizen.service_reqs[0].service.service_name',
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
        }
      ],
      timer: null
    }
  },
  computed: {
    ...mapState(['showGAScreenModal', 'csrs', 'citizens']),
    ...mapGetters(['citizens_queue', 'on_hold_queue', 'reception'])
  },
  methods: {
    ...mapActions(['closeGAScreenModal', 'getCsrs']),
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

          if (activePeriod.ps.ps_name === 'Being Served' && activePeriod.csr_id === csr.csr_id) {
            return this.citizens[i]
          }
        }
      }

      return null
    },
    computed_csrs() {
      let computed_csrs = []
      let currentDate = new Date()
      this.csrs.forEach(csr => {
        let activeCitizen = this.get_citizen_for_csr(csr)

        if (activeCitizen === null) {
          csr['wait_time'] = null
          csr['serving_time'] = null
          computed_csrs.push(csr)
        } else {
          let firstServedPeriod = activeCitizen.service_reqs[0].periods.filter(p => p.ps.ps_name === "Being Served")[0]
          let citizenStartDate = new Date(activeCitizen.start_time)
          let firstServedPeriodDate = new Date(firstServedPeriod.time_start)

          let waitSeconds = (firstServedPeriodDate - citizenStartDate) / 1000
          let serveSeconds = (currentDate - firstServedPeriodDate) / 1000

          let waitDate = new Date(null)
          waitDate.setSeconds(waitSeconds)

          let serveDate = new Date(null)
          serveDate.setSeconds(serveSeconds)

          csr['wait_time'] = `${waitDate.getUTCHours()}h ${waitDate.getMinutes()}min`
          csr['serving_time'] = `${serveDate.getUTCHours()}h ${serveDate.getMinutes()}min`
          csr['citizen'] = activeCitizen
          console.log(csr)
          console.log(csr.citizen)
          console.log(csr.citizen.service_reqs)
          computed_csrs.push(csr)
        }
      })

      return computed_csrs
    },
    fetch_csrs() {
      this.getCsrs()
    }
  }
}

</script>
