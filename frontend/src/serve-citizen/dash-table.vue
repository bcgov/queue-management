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
  <div id='client-table'>
    <b-table small
             head-variant="light"
             :items="citizens"
             :fields="fields"
             outlined
             hover
             @row-clicked="rowClicked"
             class="p-0 m-0 w-100"
             >
      <template slot='qt_xn_citizen_ind' slot-scope='data'>
        {{ (data.item.qt_xn_citizen_ind===0) ?
             ('No') :
               ('Yes')
        }}
      </template>
      <template slot='start_time' slot-scope='data'>
        {{ formatTime(data.item.start_time) }}
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
          {key: 'qt_xn_citizen_ind', label: 'Q. Txn', sortable: false, tdClass:'col-1', thClass:'col-1'},
          {key: 'citizen_id', tdClass: 'd-none', thClass:'d-none', tdClass:'col-2', thClass:'col-2'},
          {key: 'start_time', label: 'Time', sortable: true, tdClass:'col-3', thClass:'col-3'},
          {key: 'ticket_number', label: 'Ticket', sortable: false, tdClass:'col-4', thClass:'col-4'},
          {key: 'service_reqs[0].periods[0].csr.username', label: 'Served By', sortable: false, tdClass:'col-5', thClass:'col-5'},
          {key: 'service_reqs[0].service.parent.service_name', label: 'Category', sortable: false, tdClass:'col-6', thClass:'col-6'},
          {key: 'service_reqs[0].service.service_name', label: 'Service', sortable: false, tdClass:'col-7', thClass:'col-7'},
          {key: 'citizen_comments', label: 'Comments', sortable: false, tdClass:'col-8', thClass:'col-8'}
        ]
      }
    },
    computed: {
      ...mapState(['serveButtonDisabled']),
      ...mapGetters(['filtered_citizens']),
      citizens() {
        return this.filtered_citizens
      }
    },
    methods: {
      ...mapActions(['postInvite','clickDashTableRow']),
      formatTime(data) {
        let date = new Date(data)
        return date.toLocaleTimeString()
      },
      rowClicked(item, index) {
        if (this.$store.state.serveButtonDisabled==false) {
          this.$store.commit('setAlert', 'You are already serving a citizen.  Click Serve Now to resume.')
        } else if (this.$store.state.serveButtonDisabled==true) {
          this.clickDashTableRow(item.citizen_id)
        }
      }   
    }
  }
</script>  
<style>
  .col-1 {
    width: 7%;
  }
  .col-2 {
    width: 9%;
  }
  .col-3 {
    width: 10%;
  }
  .col-4 {
    width: 6%;
  }
  .col-5 {
    width: 14%;
  }
  .col-6 {
    width: 10%;
  }
  .col-7 {
    width: 14%;
  }
  .col-8 {
    width: 28%;
  }
  
  

</style>