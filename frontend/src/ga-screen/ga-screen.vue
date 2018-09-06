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
             :items="csrs"
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
    this.timer = setInterval(() => {
      this.refresh_board()
    }, 5000)
  },

  beforeDestroy() {
    clearInterval(this.timer);
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
          key: 'periods[0].sr.service.service_name',
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
          key: 'periods[0].sr.citizen.citizen_comments',
          label: 'Comments',
          sortable: true,
          formatter: (value) => { return value }
        }
      ],
      timer: null
    }
  },
  computed: {
    ...mapState(['showGAScreenModal', 'csrs']),
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
      let allCsrs = this.csrs;
      return allCsrs.length
    },
    ga_serving_csrs() {
      let allCsrs = this.csrs.filter(c => c.periods.length > 0 && c.periods[0].ps.ps_name === "Being Served");
      return allCsrs.length
    },
    refresh_board() {
      this.getCsrs()
    }
  }
}

</script>
