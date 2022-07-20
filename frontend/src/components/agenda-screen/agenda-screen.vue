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
        <h5 class='mb-4'>Day Agenda View</h5>
      </div>
      <div></div>
    </div>
    <b-form inline @submit.stop.prevent>
              <label class="mr-2">
                Filter Appointments
                <font-awesome-icon
                  icon="filter"
                  class="m-0 p-0"
                  style="font-size: 1rem"
                />
              </label>
                <b-input-group>
                  <b-form-input
                    v-model="searchTerm"
                    size="sm"
                    @input="filter"
                  ></b-form-input>
                  <b-input-group-append v-if='searchTerm.length'>
                    <b-button size='sm' variant="danger" @click='clearSearch'>Clear</b-button>
                  </b-input-group-append>
                </b-input-group>
            </b-form>
    <b-table
      small
      head-variant="light"
      :items="items"
      :fields="fields"
      outlined
      class="p-0 m-0 w-100"
      sort-by='start_time'
    >
      <template #cell(comments)="data">
        <div class="truncate"  v-b-tooltip.hover :title="data.value">
          {{ data.value }}
        </div>
      </template>
      <template #cell(check_in)="data">
        <button
          @click.stop="handleClickCheckIn(data.value.appt)"
          class="ga-close btn btn-success btn-sm"
          v-if="!loadingButtons[data.value.appt.appointment_id]"
        >
          Check-In
        </button>
        <button
          class="ga-close btn btn-success btn-sm"
          v-else
        >
          <b-spinner small variant="light" label="Spinning"></b-spinner>
        </button>
      </template>
    </b-table>
  </div>
</template>
<script lang="ts">
/* eslint-disable */
import { Action, Getter, State, namespace } from 'vuex-class'
import { Component, Vue, Watch } from 'vue-property-decorator'
import CheckInModal from '@/components/Appointments/checkin-modal.vue'
import ApptBookingModal from '../Appointments/appt-booking-modal/appt-booking-modal.vue'
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

  @appointmentsModule.State('clickedAppt') public clickedAppt: any
  @appointmentsModule.State('appointments') public appointments: any
  @appointmentsModule.State('checkInClicked') private checkInClicked!: any
  @appointmentsModule.Mutation('setAgendaClickedAppt') public setAgendaClickedAppt: any
  @appointmentsModule.Mutation('setAgendaClickedTime') public setAgendaClickedTime: any
  @appointmentsModule.Mutation('toggleCheckInModal') public toggleCheckInModal: any
  @appointmentsModule.Mutation('toggleApptBookingModal') public toggleApptBookingModal: any
  @appointmentsModule.Mutation('toggleCheckInClicked') public toggleCheckInClicked: any
  @appointmentsModule.Action('getAppointments') public getAppointments: any
  @appointmentsModule.Action('postCheckIn') public postCheckIn: any
  @appointmentsModule.Action('getServices') public getServices: any
  
  items = [];
  clickedTime: any = null;
  interval: any = null;
  searchTerm: string = '';

  private fields: any = [
    {
      key: 'start_time',
      label: 'Time',
      sortable: true,
      formatter: (value) => { return moment(value).format("LT") }
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
      key: 'comments',
      label: 'Comments'
    },
    {
      key: 'check_in',
      label: 'Check-In'
    }
  ]

  @Watch('appointments')
  onAppointmentChange(x) {
    this.updateList();
  }
  
  async updateList() {
    this.items = await this.computed_appointments();
  }

  // Note ths method does not FETCH most recent appointments!
  // Call fetch() to update underlying data
  async computed_appointments() {
    // Changing between 1 week / 1 day seems to work tho.  Just can't go lower than 1 day?
    const pastCutoff = moment(new Date()).subtract('1', 'hour');
    const futureCutoff = moment(new Date()).add('4', 'hour');
    
    const allAppointments = this.appointments
    const filteredDates = allAppointments.filter(appt => {     
      // Only show "actual" appointments
      if (appt.checked_in_time || appt.is_draft || appt.blackout_flag === 'Y') {
        return false;
      }
      // Agenda only shows appointments in near past or future.
      if ( ( moment(appt.start_time) >= pastCutoff  ) &&  ( moment(appt.start_time) <= futureCutoff  ) ) {
        return true;
      }
      return false;
    })

    if (this.$store.state.services.length === 0) {
      //  INC0074865 - Services not loaded on initial entry - call appointments to fetch services when serviceList length is 0
      this.getAppointments()  
    }
    // Format object for agenda table.
    return filteredDates.map(appt => {
      const service = this.$store.state.services
        .find(x => x.service_id === appt.service_id)
      
      const service_name = service ? service.service_name : 'N/A';
      
      return {
        start_time: appt.start_time,
        citizen_name: appt.citizen_name,
        service_name,
        contact_info: appt.contact_information,
        comments: appt.comments,
        check_in: { appt }
      }
    })
  }

  mounted () {
    this.fetch();
    // Update list every  15min.
    const fifteenMin = 1000 * 60 * 15
    this.interval = setInterval(() => { this.fetch() },  fifteenMin)
  }

  fetch() {
    // Fetch all data before rendering list
    Promise.all([
      this.getAppointments(), 
      this.$store.dispatch('getServices'), // Needed to display services names to users
      this.getServices() // REQUIRED, even if it looks like a duplicate of above
      // We have to get services twice, once for each module/store.
      // If this.getServices() is missing, a sneaky bug will appear when unchecking and re-checking in
      // causing them to disappear due to missing rootState in appointments-module.
    ])
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

  handleClickCheckIn(  appt ) {  
    // Copied this check over from check-in  modal
    // Essentially, we do not want to  allow the user to check in a user if  another user
    // is actively being served but minimized. They must instead be put on hold by CSR.
    if (this.cannotCheckIn) {
      this.$store.commit('setMainAlert', 'Already have appointment in progress.  Please close ticket then check-in citizen')
    } else {
      this.checkIn(appt);
    }
  }

  /**
   * If the Serve Citizen Modal has a citizen served, we cannot begin serving another.
   */
  get cannotCheckIn(): boolean {
    return !!this.$store.state.serviceModalForm.citizen_id
  }

  // A map of appointment_ids with true/false to show the loading spinner
  private loadingButtons = {}
  checkIn( appt ) {
    const tempEvent  = {
      title: appt.citizen_name,
      contact_information: appt.contact_information,
      online_flag: appt.online_flag,
      service_id: appt.service_id,
      comments: appt.comments,
      start: moment(appt.start_time),
      end: moment(appt.end_time),
      appointment_id: appt.appointment_id,
      recurring_uuid: null,
      blackout_flag: 'N',
      citizen_id: appt.citizen_id,
      //for invite fix
      start_time: appt.start_time
    }
    this.setAgendaClickedAppt(tempEvent)
    this.clickedTime =  {
      start: moment(appt.start_time),
      end: moment(appt.end_time)
    }
    this.setAgendaClickedTime(this.clickedTime);

    this.loadingButtons[appt.appointment_id] = true;
    this.postCheckIn(this.clickedAppt).then(response => {
      this.$root.$emit('clear-clicked-appt')
      this.$root.$emit('clear-clicked-time')
      this.loadingButtons[appt.appointment_id] = false;
    }).catch(() => {
      this.loadingButtons[appt.appointment_id] = false;
    }).finally(() => {
      this.loadingButtons[appt.appointment_id] = false;
    });
  }
  
  APPOINTMENT_FILTER_FIELDS = ['start_time', 'citizen_name', 'service_name', 'contact_info', 'comments']

  async filter() {
    const appointments = await this.computed_appointments()
    const search = this.searchTerm.toLowerCase()
    this.items = appointments.filter(appt => {
      let hasMatch = false;
      this.APPOINTMENT_FILTER_FIELDS.forEach(field => {        
        if (appt[field] && appt[field].toLowerCase && appt[field].toLowerCase().includes(search)) {
          hasMatch = true;
        }
      })
      return hasMatch;
    }) 
  }

  async clearSearch() {
    this.searchTerm = '';
    this.items = await this.computed_appointments();
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
.truncate {
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 225px;
}
</style>
