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
      <div>
        <h5>Day Agenda View</h5>
      </div>
      <div></div>
    </div>
    <!--<div>-->
    <!--The time is now: {{time_now}}-->
    <!--</div>-->
    <b-table
      small
      head-variant="light"
      :items="items"
      :fields="fields"
      outlined
      class="p-0 m-0 w-100"
    >
      <template slot="edit" slot-scope="data" v-if="data.value">
        <button
          @click.stop="edit(data.value.id)"
          class="ga-close btn btn-secondary btn-sm"
        >
          {{ data.value.label }}
          <!-- data.value.label here -->
        </button>
      </template>
      <template slot="check_in" slot-scope="data" v-if="data.value">
        <button
          @click.stop="checkIn(data.value.id)"
          class="ga-close btn btn-secondary btn-sm"
        >
          {{ data.value.label }}
          <!-- data.value.label here -->
        </button>
      </template>
    </b-table>
  </div>
</template>
<script lang="ts">
// /* eslint-disable */
import { Action, Getter, Mutation, State, namespace } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'

import moment from 'moment'
// import {
//   mapActions, mapGetters, mapState
// }
//   from 'vuex'

const appointmentsModule = namespace('appointmentsModule')

@Component({})
export default class AgendaScreen extends Vue {
  @State('showGAScreenModal') private showGAScreenModal!: any
  // @State('csrs') private csrs!: any
  // @State('citizens') private citizens!: any
  // @State('csr_states') private csr_states!: any

  // @State()

  @Getter('citizens_queue') private citizens_queue!: any;
  @Getter('on_hold_queue') private on_hold_queue!: any;
  @Getter('reception') private reception!: any;

  @Action('closeGAScreenModal') public closeGAScreenModal: any
  // @Action('getCsrs') public getCsrs: any
  // @Action('finishServiceFromGA') public finishServiceFromGA: any

  @appointmentsModule.Action('getAppointments') public getAppointments: any
  
  items = [];


  private fields: any = [
    {
      key: 'start_time',
      label: 'Start Time',
      sortable: true
    },
    {
      key: 'citizen_name',
      label: 'Citizen Name',
      sortable: true
    },
    {
      key: 'service_name',
      label: 'Service',
      sortable: true
    },
    {
      key: 'contact_info',
      label: 'Contact Info',
      sortable: true
    },
    {
      key: 'edit',
      label: 'Edit'
    },
    {
      key: 'check_in',
      label: 'Check In'
    }
  ]

  // private time_now: any = 'Sometime'
  // private timer: any = null
  // interval: any

  public fetch_csrs () {
    // this.getCsrs()
  }

  updateList() {
    this.items = this.computed_appointments();
  }

  computed_appointments() {
    // Note This does not FETCH most recent appointments!
    const now = new Date();
    const pastCutoff = moment(new Date()).subtract('1', 'week');
    const futureCutoff = moment(new Date()).add('4', 'hour');
    
    const filteredDates = this.$store.state.appointmentsModule.appointments
    // .sort((a, b) => {
    //   return a.start_time - b.start_time;
    // })
    .filter(appt => {      
      const m = moment;
      // if ( (moment(appt.start_time) <= futureCutoff ) && ( moment(appt.end_time) >= pastCutoff  ) ) {
      // if ( (moment(appt.start_time)  futureCutoff ) ) {
      // TODO - Need to check against futureTime too
      if ( ( moment(appt.end_time) >= pastCutoff  )) {
        return true;
      }
      
      return false;
      // return true;
    })

    // return this.$store.state.appointmentsModule.appointments.map(appt => {
    return filteredDates.map(appt => {

      //  Was working, now is throwing error, look into later
      // Problem - Have to go to Appointments page first
      // Solution > need to trigger store update somehow? dispatch proper event?
      const service_name = this.$store.state.services
        .find(x => x.service_id === appt.service_id).service_name
      
      return {
        start_time: moment(appt.start_time).format("HH:mm (L)"),
        citizen_name: appt.citizen_name,
        // service_name: 'todo?',
        // service_name: this.getServiceNameById(appt.service_id),
        service_name,
        contact_info: appt.contact_information
      }
    })
  }

  mounted () {
    // Only render list when we have  both serviecs and appointments
    Promise.all([this.$store.dispatch('getServices'), this.getAppointments()])
    .then(() => {
      this.updateList();
    }) 
  }

  beforeDestroy () {
    // clearInterval(this.interval)
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
