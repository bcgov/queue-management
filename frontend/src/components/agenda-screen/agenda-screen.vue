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
    <b-table
      small
      head-variant="light"
      :items="items"
      :fields="fields"
      outlined
      class="p-0 m-0 w-100"
    >
      <template slot="edit" slot-scope="data">
        <button
          @click.stop="edit(data.value.appt)"
          class="ga-close btn btn-secondary btn-sm"
        >
          Edit
        </button>
      </template>
      <template slot="check_in" slot-scope="data">
        <button
          @click.stop="checkIn(data.value.appt)"
          class="ga-close btn btn-success btn-sm"
        >
          Check In
        </button>
      </template>
    </b-table>
    <CheckInModal :clickedAppt="clickedAppt" />
    <ApptBookingModal :clickedTime="clickedTime" :clickedAppt="clickedAppt" />
  </div>
</template>
<script lang="ts">
// /* eslint-disable */
import { Action, Getter, Mutation, State, namespace } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'
// import CheckInModal from '../Appointments/checkin-modal';
import CheckInModal from '../Appointments/checkin-modal'
import ApptBookingModal from '../Appointments/appt-booking-modal/appt-booking-modal.vue'
import { formatedStartTime } from '@/utils/helpers'



import moment from 'moment'
const appointmentsModule = namespace('appointmentsModule')

@Component({
  components: { 
    CheckInModal,
    ApptBookingModal
  }
})
export default class AgendaScreen extends Vue {
  @State('showGAScreenModal') private showGAScreenModal!: any
  @Getter('citizens_queue') private citizens_queue!: any;
  @Getter('on_hold_queue') private on_hold_queue!: any;
  @Getter('reception') private reception!: any;
  @Action('closeGAScreenModal') public closeGAScreenModal: any

  @appointmentsModule.Action('getAppointments') public getAppointments: any
  @appointmentsModule.Mutation('toggleCheckInModal') public toggleCheckInModal: any
  @appointmentsModule.Mutation('toggleApptBookingModal') public toggleApptBookingModal: any

  
  
  items = [];
  clickedTime: any = null;

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


  public clickedAppt: any = null;
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
      
      // Already checked in, hide from agenda
      // Todo - verify
      if (appt.checked_in_time) {
        return false;
      }

      // const m = moment;
      // if ( (moment(appt.start_time) <= futureCutoff ) && ( moment(appt.end_time) >= pastCutoff  ) ) {
      // if ( (moment(appt.start_time)  futureCutoff ) ) {
      // TODO - Need to check against futureTime too
      if ( ( moment(appt.end_time) >= pastCutoff  )) {
        return true;
      }
  
      return false;
    })

    // return this.$store.state.appointmentsModule.appointments.map(appt => {
    return filteredDates.map(appt => {

      //  Was working, now is throwing error, look into later
      // Problem - Have to go to Appointments page first
      // Solution > need to trigger store update somehow? dispatch proper event?
      const service = this.$store.state.services
        .find(x => x.service_id === appt.service_id)
      
      const service_name = service ? service.service_name : 'N/A';
      
      return {
        start_time: moment(appt.start_time).format("HH:mm (L)"),
        citizen_name: appt.citizen_name,
        service_name,
        contact_info: appt.contact_information,

        // check_in: { appointment_id: appt.appointment_id }
        check_in: { appt },
        edit: { appt }
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

  edit( appt ) {
    console.log('edit', appt)

    this.clickedAppt = appt;

    // const start = formatedStartTime(appt.start_time, event.time)// event.start.clone()
    this.clickedTime =  {
      start: moment(appt.start_time),
      end: moment(appt.end_time)
    }

    // set clickedAppt and even clickedTime?

    this.toggleApptBookingModal(true);
    
  }

  checkIn( appt ) {
    console.log('checkIn', appt)
    this.clickedAppt = appt;
    this.toggleCheckInModal(true);
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
