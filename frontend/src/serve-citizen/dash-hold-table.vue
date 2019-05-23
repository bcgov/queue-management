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

  <div id='client-hold-table'>
    <b-table :items="on_hold_queue"
             :fields=getFields
             head-variant="light"
             small
             outlined
             hover
             @row-clicked="rowClicked"
             class="p-0 m-0">
             <template slot='counter_id' slot-scope='data'>
               {{ showCounter(data.item.counter_id) }}
             </template>
             <template slot='start_time' slot-scope='data'>
               {{ formatTime(data.item.start_time) }}
             </template>
             <template slot='csr' slot-scope='data'>
             {{ showCSR(data.item.citizen_id) }}
             </template>
             <template slot='category' slot-scope='data'>
               {{ showCategory(data.item.citizen_id) }}
             </template>
             <template slot='service' slot-scope='data'>
               {{ showService(data.item.citizen_id) }}
             </template>
             <template slot='priority' slot-scope='data'>
               {{ showPriority(data.item.priority) }}
             </template>
    </b-table>
  </div>
</template>

<script>
  import { mapState, mapGetters, mapActions } from 'vuex'

  export default {
    name: 'DashHoldTable',
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
          {key: 'citizen_comments', label: 'Comments', sortable: false, thStyle: 'width: 17%'}
        ]
      }
    },

    computed: {
      ...mapState(['citizens', 'citizenInvited', 'performingAction', 'showTimeTrackingIcon', 'user']),
      ...mapGetters([
        'on_hold_queue',
        'citizens_queue',
        'active_service',
        'active_index',
        'active_service_id',
        'reception'
      ]),
      getFields: function() {
        if (this.reception) {
          let temp = this.fields
          temp.unshift({key: 'counter_id', label: 'Counter', sortable: false, thStyle: 'width: 8%'})
          temp.unshift({key: 'priority', label: 'Priority', sortable: false, thStyle: 'width: 8%'})
          return temp
        }
        else {
          let temp = this.fields
          temp.unshift({key: 'priority', label: 'Priority', sortable: false, thStyle: 'width: 10%'})
          return temp
        }
      }
    },
    methods: {
      ...mapActions(['clickRowHoldQueue']),
      formatTime(data) {
        let date = new Date(data)
        let display = date.toLocaleTimeString()
        return display
      },

      rowClicked(item, index) {
        if (this.showTimeTrackingIcon) {
          this.$store.commit('setMainAlert', 'You are already serving a citizen.  Click the Stopwatch to resume')
          return null
        }
        if (this.performingAction) {
          return null
        }
        if (this.citizenInvited===true) {
          this.$store.commit('setMainAlert', 'You are already serving a citizen.  Click Serve Now to resume.')
        } else if (this.citizenInvited===false) {
          this.clickRowHoldQueue(item.citizen_id)
        }
      },
      showCounter(value) {
        for(let i = 0; i < this.user.office.counters.length; i++){
          if(this.user.office.counters[i].counter_id == value){
            return this.user.office.counters[i].counter_name
          }
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
      showCategory(id) {
        let service = this.active_service_id(id)
        if (!service) {
          return null
        }
        return service.service.parent.service_name
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
