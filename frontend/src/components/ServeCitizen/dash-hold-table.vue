<!--
/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/-->

<template>
  <div id="client-hold-table">
    <b-table
      :items="on_hold_queue"
      :fields="getFields"
      head-variant="light"
      small
      outlined
      hover
      @row-clicked="rowClicked"
      class="p-0 m-0"
    >
      <template #cell(counter_id)="data">{{ showCounter(data.item.counter_id) }}</template>
      <template #cell(start_time)="data">{{ formatTime(data.item.start_time) }}</template>
      <template #cell(csr)="data">{{ showCSR(data.item.citizen_id) }}</template>
      <template #cell(category)="data">{{ showCategory(data.item.citizen_id) }}</template>
      <template #cell(service)="data">{{ showService(data.item.citizen_id) }}</template>
      <template #cell(priority)="data">{{ showPriority(data.item.priority) }}</template>
      <template #cell(citizen_comments)="row">
        <template v-if="row.item.citizen_name">
          <span style="color: teal">{{ parseComments(row.item).appt }}</span>
          <br />
          <span class="mr-2">{{ parseComments(row.item).text }}</span>
        </template>
        <template v-else>{{ parseComments(row.item) }}</template>
      </template>
      <template slot="reminder_flag" slot-scope="row" v-if="isNotificationEnabled === 1">
        <b-button 
          v-if="(row.item.reminder_flag == 0) && (row.item.notification_phone || row.item.notification_email)"
          @click="sentReminder(row.item.citizen_id, 'first')"
          variant="secondary"
          >
          <font-awesome-icon
            icon="phone"
          />
        </b-button>
        <b-button 
          v-if="row.item.reminder_flag == 1 && (row.item.notification_phone || row.item.notification_email)"
          variant="primary"
          @click="sentReminder(row.item.citizen_id, 'second')"
          >
          <font-awesome-icon
            icon="phone"
          />
        </b-button>
        <b-button 
          disabled
          v-if="row.item.reminder_flag == 2 && (row.item.notification_phone || row.item.notification_email)"
          variant="danger"
          >
          <font-awesome-icon
            icon="phone"
            disabled
          />
        </b-button>
      </template>
      <template slot="notification_phone" slot-scope="row" v-if="isNotificationEnabled === 1">
        <b-row v-if="row.item.notification_phone">
          {{row.item.notification_phone}}
        </b-row>
        <b-row v-if="row.item.notification_email">
          {{row.item.notification_email}}
        </b-row>
      </template>
      <template slot="notification_sent_time" slot-scope="row" v-if="isNotificationEnabled === 1">
         <b-button 
          disabled
          v-if="row.item.notification_sent_time"
          variant="info"
          >
          <font-awesome-icon
            disabled
            icon="clock"
          />
        </b-button>
        <span v-if="row.item.notification_sent_time">{{timeFormat(row.item.notification_sent_time)}} </span>
      </template>
    </b-table>
  </div>
</template>

<script lang="ts">
/* eslint-disable */
import { Action, Getter, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

import moment from 'moment'

@Component({})
export default class DashHoldTable extends Vue {
  @State('citizens') private citizens!: any
  @State('citizenInvited') private citizenInvited!: any
  @State('performingAction') private performingAction!: any
  @State('showTimeTrackingIcon') private showTimeTrackingIcon!: any
  @State('user') private user!: any

  @Getter('on_hold_queue') private on_hold_queue!: any;
  @Getter('citizens_queue') private citizens_queue!: any;
  @Getter('active_service') private active_service!: any;
  @Getter('active_index') private active_index!: any;
  @Getter('active_service_id') private active_service_id!: any;
  @Getter('reception') private reception!: any;

  @Action('clickRowHoldQueue') public clickRowHoldQueue: any
  @Action('sentNotificationReminder') public sentNotificationReminder: any

  private t: boolean = true
  private f: boolean = false
  public isNotificationEnabled: number = 0

  private fields_with_notification: any = [
    { key: 'citizen_id', thClass: 'd-none', tdClass: 'd-none' },
    { key: 'start_time', label: 'Time', sortable: true, thStyle: 'width: 10%' },
    { key: 'ticket_number', label: 'Ticket', sortable: false, thStyle: 'width: 6%' },
    { key: 'csr', label: 'Served By', sortable: false, thStyle: 'width: 10%' },
    { key: 'category', label: 'Category', sortable: false, thStyle: 'width: 17%' },
    { key: 'service', label: 'Service', sortable: false, thStyle: 'width: 17%' },
    { key: 'citizen_comments', label: 'Comments', sortable: false, thStyle: 'width: 10%' },
    { key: 'reminder_flag', label: 'Action', sortable: false, thStyle: 'width: 4%' },
    { key: 'notification_phone', label: 'Notification', sortable: false, thStyle: 'width: 20%' },
    { key: 'notification_sent_time', label: 'Time Sent', sortable: false, thStyle: 'width: 20%' }
  ]
  private fields_without_notification: any = [
    { key: 'citizen_id', thClass: 'd-none', tdClass: 'd-none' },
    { key: 'start_time', label: 'Time', sortable: true, thStyle: 'width: 10%' },
    { key: 'ticket_number', label: 'Ticket', sortable: false, thStyle: 'width: 6%' },
    { key: 'csr', label: 'Served By', sortable: false, thStyle: 'width: 10%' },
    { key: 'category', label: 'Category', sortable: false, thStyle: 'width: 17%' },
    { key: 'service', label: 'Service', sortable: false, thStyle: 'width: 17%' },
    { key: 'citizen_comments', label: 'Comments', sortable: false, thStyle: 'width: 10%' }
  ]

  private fields: any = this.fields_without_notification


  get getFields () {
    if (this.isNotificationEnabled === 1) {
      this.fields = this.fields_with_notification
    } else {
      this.fields = this.fields_without_notification
    }
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
    if (this.citizenInvited === true) {
      this.$store.commit('setMainAlert', 'You are already serving a citizen.  Click Serve Now to resume.')
    } else if (this.citizenInvited === false) {
      this.clickRowHoldQueue(item.citizen_id)
    }
  }

  private showCounter (value: any) {
    for (let counter of this.user.office.counters) {
      if (counter.counter_id == value) {
        return counter.counter_name
      }
    }
  }

  private showCSR (id: any) {
    const service = this.active_service_id(id)
    if (!service) {
      return null
    }
    const n = service.periods.findIndex(p => p.time_end === null)
    return service.periods[n].csr.username
  }

  private showCategory (id: any) {
    const service = this.active_service_id(id)
    if (!service) {
      return null
    }
    return service.service.parent.service_name
  }

  private showService (id: any) {
    const service = this.active_service_id(id)
    if (!service) {
      return null
    }
    return service.service.service_name
  }

  private showPriority (priority: any) {
    switch (priority) {
      case 1:
        return 'High'
      case 2:
        return 'Default'
      case 3:
        return 'Low'
      default:
        return null
    }
  }

  public timeFormat (value: any) {
    return moment.utc(value).local().format('hh:mm A')
  }

  private sentReminder (citizen_id: any, count: any) {
    let payload = {}
    if (count === 'first') {
      payload = {
        'citizen_id' : citizen_id,
        'is_first_reminder' : true,
        'is_second_reminder' : false
      }
    }
    if (count === 'second') {
      payload = {
        'citizen_id' : citizen_id,
        'is_first_reminder' : false,
        'is_second_reminder' : true
      }
    }
    this.sentNotificationReminder(payload)
  }

  private mounted () {
    this.isNotificationEnabled = this.$store.state.user.office.check_in_notification
  }
}

</script>
