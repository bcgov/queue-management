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
      sort-by='start_time'
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
    <ApptBookingModal :clickedTime="clickedTime" :clickedAppt="clickedAppt" />
    <CheckInModal :clickedAppt="clickedAppt" />
  </div>
</template>
<script lang="ts">
import { Action, Getter, Mutation, State, namespace } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'
import CheckInModal from '@/components/Appointments/checkin-modal.vue'
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

  // @State('clickedAppt') private clickedAppt!: any
  @appointmentsModule.State('clickedAppt') public clickedAppt: any
  @appointmentsModule.Mutation('setAgendaClickedAppt') public setAgendaClickedAppt: any


  @appointmentsModule.Action('getAppointments') public getAppointments: any
  @appointmentsModule.Mutation('toggleCheckInModal') public toggleCheckInModal: any
  @appointmentsModule.Mutation('toggleApptBookingModal') public toggleApptBookingModal: any

  
  // public clickedAppt: any = null;
  
  items = [];
  clickedTime: any = null;
  interval: any = null;

  private fields: any = [
    {
      key: 'start_time',
      label: 'Time',
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

  async updateList() {
    this.items = await this.computed_appointments();
  }

  // Note ths method does not FETCH most recent appointments!
  // Call fetch() to update underlying data
  async computed_appointments() {
    const now = new Date();

    // Changing between 1 week / 1 day seems to work tho.  Just can't go lower than 1 day?
    const pastCutoff = moment(new Date()).subtract('1', 'hour');
    const futureCutoff = moment(new Date()).add('4', 'hour');
    
    const allAppointments = await this.getAppointments()
    const filteredDates = allAppointments.filter(appt => {     
      // Already checked in, hide from agenda
      if (appt.checked_in_time || appt.is_draft) {
        return false;
      }

      // Agenda only shows appointments in near past or future.
      if ( ( moment(appt.end_time) >= pastCutoff  ) &&  ( moment(appt.start_time) <= futureCutoff  ) ) {
        return true;
      }
      return false;
    })

    // Format object for agenda table.
    return filteredDates.map(appt => {
      const service = this.$store.state.services
        .find(x => x.service_id === appt.service_id)
      
      const service_name = service ? service.service_name : 'N/A';
      
      return {
        start_time: `${moment(appt.start_time).format("LT")} to ${moment(appt.end_time).format("LT")}`,
        citizen_name: appt.citizen_name,
        service_name,
        contact_info: appt.contact_information,
        check_in: { appt },
        edit: { appt }
      }
    })
  }

  mounted () {
    this.fetch();
    // TODO - Can re-enable interval for updating?
    // this.interval = setInterval(this.fetch, 30 * 1000)
  }

  fetch() {
    console.log('Agenda fetch...');
    // Only render list when we have both serviecs and appointments
    Promise.all([this.$store.dispatch('getServices'), this.getAppointments()])
    .then(() => {
      this.updateList();
    }) 
  }

  beforeDestroy () {
    clearInterval(this.interval)
  }

  edit( appt ) {
    const tempEvent = {
      title: appt.citizen_name,
      contact_information: appt.contact_information,
      online_flag: appt.online_flag,
      service_id: appt.service_id,
      comments: appt.comments,
      start: moment(appt.start_time),
      end: moment(appt.end_time),
      appointment_id: appt.appointment_id
    }

    this.setAgendaClickedAppt(tempEvent)

    this.clickedTime =  {
      start: moment(appt.start_time),
      end: moment(appt.end_time)
    }
    this.toggleApptBookingModal(true);
  }

  checkIn( appt ) {
    console.log('checkIn', appt)
    this.setAgendaClickedAppt(appt);
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
