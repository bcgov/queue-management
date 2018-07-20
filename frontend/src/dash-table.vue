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
             :items="citizens"
             :fields="fields"
             outlined
             hover
             striped
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
  import { mapState, mapGetters } from 'vuex'

  export default {
    name: 'DashTable',
    data() {
      return {
        t:true,
        f:false,
        fields: [
          {key: 'qt_xn_citizen_ind', label: 'Q. Txn', sortable: false},
          {key: 'start_time', label: 'Time', sortable: true},
          {key: 'ticket_number', label: 'Ticket', sortable: false},
          {key: 'service_reqs[0].periods[0].csr.username', label: 'Served By', sortable: false},
          {key: 'service_reqs[0].service.parent.service_name', label: 'Category', sortable: false},
          {key: 'service_reqs[0].service.service_name', label: 'Service', sortable: false},
          {key: 'service_reqs[0].periods[0].ps.ps_name', label: 'State', sortable: false},
          {key: 'citizen_comments', label: 'Comments', sortable: false}
        ]
      }
    },
    computed: {
      ...mapState({
        citizens(state) {
          let filtered = state.citizens.filter(ctzn=>
            ctzn.service_reqs.length > 0
          )
        return filtered
        }
      })
    },
    methods: {
      formatTime(data) {
        let date = new Date(data)
        let display = date.toLocaleTimeString()
        return display
      }
    }
  }
</script>

<style scoped>
  .dashtabletrthead {
    color: red;
  }
</style>