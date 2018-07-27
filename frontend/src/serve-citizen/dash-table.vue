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
             fixed
             @row-clicked="rowClicked"
             class="p-0 m-0"
             thead-tr-class="dashtabletrthead"
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
          {key: 'qt_xn_citizen_ind', label: 'Q. Txn', sortable: false},
          {key: 'citizen_id', tdClass: 'd-none', thClass:'d-none'},
          {key: 'start_time', label: 'Time', sortable: true},
          {key: 'ticket_number', label: 'Ticket', sortable: false},
          {key: 'service_reqs[0].periods[0].csr.username', label: 'Served By', sortable: false},
          {key: 'service_reqs[0].service.parent.service_name', label: 'Category', sortable: false},
          {key: 'service_reqs[0].service.service_name', label: 'Service', sortable: false},
          {key: 'citizen_comments', label: 'Comments', sortable: false}
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
        console.log(item)
        if (this.$store.state.serveButtonDisabled==false) {
          console.log('true')
          this.$store.commit('setAlert', 'You are already serving a citizen.  Click Serve Now to resume.')
        } else if (this.$store.state.serveButtonDisabled==true) {
          this.clickDashTableRow(item.citizen_id)
        }
      }   
    }
  }
</script>   
<style scoped>
  .dashtabletrthead {
    color: red;
  }
</style>