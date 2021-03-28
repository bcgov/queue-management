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
  <div id="client-waiting-table">
    <b-table
      small
      head-variant="light"
      :items="citizens"
      :fields="getFields"
      outlined
      hover
      @row-clicked="rowClicked"
      class="p-0 m-0"
    >
      <!--id="client-waiting-table"-->
      <template #cell(counter_id)="row">{{ showCounter(row.item.counter_id) }}</template>
      <template #cell(start_time)="row">{{ formatTime(row.item.start_time) }}</template>
      <template #cell(csr)="row">{{ showCSR(row.item.citizen_id) }}</template>
      <template #cell(category)="row">{{ showCategory(row.item.citizen_id) }}</template>
      <template #cell(service)="row">{{ showService(row.item.citizen_id) }}</template>
      <template #cell(priority)="row">{{ showPriority(row.item.priority) }}</template>
      <template #cell(citizen_comments)="row">
        <template v-if="row.item.citizen_name">
          <span style="color: teal">{{ parseComments(row.item).appt }}</span>
          <br />
          <span class="mr-2">{{ parseComments(row.item).text }}</span>
        </template>
        <template v-else>{{ parseComments(row.item) }}</template>
      </template>
    </b-table>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Action, Getter, State, namespace } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

const AppointmentsModule = namespace('appointmentsModule')

@Component({})
export default class DashTable extends Vue {
  @State('citizenInvited') private citizenInvited!: any
  @State('serviceModalForm') private serviceModalForm!: any
  @State('performingAction') private performingAction!: any
  @State('showTimeTrackingIcon') private showTimeTrackingIcon!: any
  @State('user') private user!: any

  @Getter('citizens_queue') private citizens_queue!: any;
  @Getter('active_service_id') private active_service_id!: any;
  @Getter('reception') private reception!: any;

  @AppointmentsModule.Getter('apointments') private apointments!: any;

  @Action('clickDashTableRow') public clickDashTableRow: any
  @Action('postInvite') public postInvite: any

  private t: boolean = true
  private f: boolean = false
  private fields: any = [
    { key: 'citizen_id', thClass: 'd-none', tdClass: 'd-none' },
    { key: 'start_time', label: 'Time', sortable: true, thStyle: 'width: 10%' },
    { key: 'ticket_number', label: 'Ticket', sortable: false, thStyle: 'width: 6%' },
    { key: 'csr', label: 'Served By', sortable: false, thStyle: 'width: 10%' },
    { key: 'category', label: 'Category', sortable: false, thStyle: 'width: 17%' },
    { key: 'service', label: 'Service', sortable: false, thStyle: 'width: 17%' },
    { key: 'citizen_comments', label: 'Comments', sortable: false, thStyle: 'width: 17%' }
  ]

  get citizens () {
    return this.citizens_queue
  }

  get getFields () {
    if (this.reception) {
      const temp = this.fields
      temp.unshift({ key: 'counter_id', label: 'Counter', sortable: false, thStyle: 'width: 8%' })
      temp.unshift({ key: 'priority', label: 'Priority', sortable: false, thStyle: 'width: 8%' })
      return temp
    } else {
      const temp = this.fields
      temp.unshift({ key: 'priority', label: 'Priority', sortable: false, thStyle: 'width: 10%' })
      return temp
    }
  }

  private formatTime (data: any) {
    const date = new Date(data)
    return date.toLocaleTimeString()
  }

  private setAppointmentDisplayData (id: any) {

  }

  private parseComments (item: any) {
    if (!item.citizen_comments) {
      return ''
    }
    const comments = item.citizen_comments
    if (!comments.includes('|||')) {
      return comments
    } else {
      const bits = comments.split('|||')
      return {
        appt: `${bits[0]} Appt: ${item.citizen_name}`,
        text: bits[1]
      }
    }
  }

  private rowClicked (item: any, index: any) {
    if (this.showTimeTrackingIcon) {
      this.$store.commit('setMainAlert', 'You are already serving a citizen.  Click the Stopwatch to resume')
      return null
    }
    if (this.performingAction) {
      return null
    }
    if (this.citizenInvited) {
      this.$store.commit('setMainAlert', 'You are already serving a citizen.  Click Serve Now to resume.')
    } else if (!this.citizenInvited) {
      this.clickDashTableRow(item.citizen_id)
    }
  }

  private showCSR (id: number) {
    const service = this.active_service_id(id)
    if (!service) {
      return null
    }
    const n = service.periods.findIndex(p => p.time_end === null)
    return service.periods[n].csr.username
  }

  private showCounter (value: any) {
    for (let i = 0; i < this.user.office.counters.length; i++) {
      if (this.user.office.counters[i].counter_id == value) {
        return this.user.office.counters[i].counter_name
      }
    }
  }

  private showCategory (id: number) {
    const service = this.active_service_id(id)
    if (!service) {
      return null
    }
    if (service.service.parent) {
      return service.service.parent.service_name
    } else { // @TODO DELETE THIS
      return 'category'
    }
  }

  private log (data: any) {
    console.log(data)
    return 'wee'
  }

  private showService (id: any) {
    const service = this.active_service_id(id)
    if (!service) {
      return null
    }
    return service.service.service_name
  }

  private showPriority (priority: any) {
    return priority === 1 ? 'High' : priority === 2 ? 'Default' : priority === 3 ? 'Low' : null
  }
}
</script>
