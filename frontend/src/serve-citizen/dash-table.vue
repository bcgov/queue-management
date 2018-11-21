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
    <b-table small
             head-variant="light"
             :items="citizens"
             :fields=getFields
             outlined
             hover
             @row-clicked="rowClicked"
             class="p-0 m-0"
             id="client-waiting-table">
      <template slot='qt_xn_citizen_ind' slot-scope='data'>
        {{ (data.item.qt_xn_citizen_ind===0) ? ('No') : ('Yes') }}
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
          {key: 'priority', label: 'Priority', sortable: false, thStyle: 'width: 10%'}
        ]
      }
    },
    computed: {
      ...mapState(['citizenInvited', 'serviceModalForm', 'performingAction']),
      ...mapGetters(['citizens_queue', 'active_service_id', 'reception']),
      citizens() {
        return this.citizens_queue
      },
      getFields: function() {
        if (this.reception) {
          let temp = this.fields
          temp.unshift({key: 'qt_xn_citizen_ind', label: 'Q. Txn', sortable: false, thStyle: 'width: 6%'})
          return temp
        }
        else {
          return this.fields
        }
      }
    },
    methods: {
      ...mapActions(['postInvite','clickDashTableRow']),
      formatTime(data) {
        let date = new Date(data)
        return date.toLocaleTimeString()
      },
      rowClicked(item, index) {
        if (this.performingAction) {
          return null
        }
        if (this.citizenInvited===true) {
          this.$store.commit('setMainAlert', 'You are already serving a citizen.  Click Serve Now to resume.')
        } else if (this.citizenInvited===false) {
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
