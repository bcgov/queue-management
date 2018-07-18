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
  <DashTable :table_status="dash_status" />
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import DashTable from './dash-table'

  export default {
    name: 'Dash',
    components: { DashTable },
    created() {
      this.$store.dispatch('getAllClients')
    },
    computed: {
      ...mapState(['clients',]),
      ...mapGetters(['dash_status']),
      totalRows() {
        return this.clients.length
      },
      sortDesc() {
        return this.dash_status.descending
      },
      sortBy: {
        get() { return this.dash_status.sort },
        set(value) { this.$store.commit('updateDash'),{type:'sortby',value}}
      },
      currentPage: {
        get() { return this.dash_status.page },
        set(value) { this.$store.commit('updateDash', {type:'page',value})}
      },
      perPage: {
        get() { return this.dash_status.perpage },
        set(value) { this.$store.commit('updateDash',{type:'perpage',value}) }
      }
    }
  }
</script>
