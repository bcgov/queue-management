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
    <b-table small
             head-variant="light"
             :items="citizens"
             :fields=getFields
             outlined
             hover
             @row-clicked="rowClicked"
             class="p-0 m-0">
             <!--id="client-waiting-table"-->
      <template slot='counter_id' slot-scope='row'>
        {{ showCounter(row.item.counter_id) }}
      </template>
      <template slot='start_time' slot-scope='row'>
        {{ formatTime(row.item.start_time) }}
      </template>
      <template slot='csr' slot-scope='row'>
        {{ showCSR(row.item.citizen_id) }}
      </template>
      <template slot='category' slot-scope='row'>
        {{ showCategory(row.item.citizen_id) }}
      </template>
      <template slot='service' slot-scope='row'>
        {{ showService(row.item.citizen_id) }}
      </template>
      <template slot='priority' slot-scope='row'>
        {{ showPriority(row.item.priority) }}
      </template>
      <template slot="citizen_comments" slot-scope="row">
        <template v-if="row.item.citizen_name">
          <span style="color: teal">{{ parseComments(row.item).appt }}</span><br>
          <span class="mr-2">{{ parseComments(row.item).text }}</span>
        </template>
        <template v-else>
          {{ parseComments(row.item) }}
        </template>
      </template>
    </b-table>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex'

  export default {
    name: 'DashTable',
    data() {
      return {
        t:true,
        f:false,
        fields: [
          {key: 'citizen_id', thClass:'d-none', tdClass:'d-none' },
          {key: 'start_time', label: 'Time', sortable: true, thStyle: 'width: 10%'},
          {key: 'ticket_number', label: 'Ticket', sortable: false, thStyle: 'width: 6%'},
          {key: 'csr', label: 'Served By', sortable: false, thStyle: 'width: 10%'},
          {key: 'category', label: 'Category', sortable: false, thStyle: 'width: 17%'},
          {key: 'service', label: 'Service', sortable: false, thStyle: 'width: 17%'},
          {key: 'citizen_comments', label: 'Comments', sortable: false, thStyle: 'width: 17%'},
        ]
      }
    },
    computed: {
      ...mapState(['citizenInvited', 'serviceModalForm', 'performingAction', 'showTimeTrackingIcon', 'user']),
      ...mapGetters({
        citizens_queue: 'citizens_queue',
        active_service_id: 'active_service_id',
        reception: 'reception',
        apointments: 'appointmentsModule/appointment_even'
      }),
      citizens() {
        return this.citizens_queue
      },
      getFields: function() {
        if (this.reception) {
          let temp = this.fields
          temp.unshift({key: 'counter_id', label: 'Counter', sortable: false, thStyle: 'width: 8%'})
          temp.unshift({key: 'priority', label: 'Priority', sortable: false, thStyle: 'width: 8%'})
          return temp
        } else {
          let temp = this.fields
          temp.unshift({key: 'priority', label: 'Priority', sortable: false, thStyle: 'width: 10%'})
          return temp
        }
      }
    },
    methods: {
      ...mapActions(['clickDashTableRow', 'postInvite']),
      formatTime(data) {
        let date = new Date(data)
        return date.toLocaleTimeString()
      },
      setAppointmentDisplayData(id) {

      },
      parseComments(item) {
        if (!item.citizen_comments) {
          return ''
        }
        let comments = item.citizen_comments
        if (!comments.includes('|||')) {
          return comments
        } else {
          let bits = comments.split('|||')
          return {
            appt: `${bits[0]} Appt: ${item.citizen_name}`,
            text: bits[1]
          }
        }
      },

      rowClicked(item, index) {
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
      },
      showCSR(id) {
        let service = this.active_service_id(id)
        if (!service) {
          return null
        }
        let n = service.periods.findIndex(p => p.time_end === null)
        return service.periods[n].csr.username
      },
      showCounter(value) {
        for(let i = 0; i < this.user.office.counters.length; i++){
          if(this.user.office.counters[i].counter_id == value){
            return this.user.office.counters[i].counter_name
          }
        }
      },
      showCategory(id) {
        let service = this.active_service_id(id)
        if (!service) {
          return null
        }
        if(service.service.parent){
          return service.service.parent.service_name
        } else { // @TODO DELETE THIS
          return "category"
        }
      },
      log(data) {
        console.log(data)
        return 'wee'
      },
      showService(id) {
        let service = this.active_service_id(id)
        if (!service) {
          return null
        }
        return service.service.service_name
      },
      showPriority(priority) {
        return priority == 1 ? 'High' : priority == 2 ? 'Default' : priority == 3 ? 'Low' : null
      }

    }
  }
</script>
