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
  <b-container fluid>
    <b-row class="dashrow">
      <ClientService />
      <AddCitizen />
      <Login />
    </b-row>
    <b-row no-gutters>
      <b-col>
        Citizens Waiting: {{ queueLength }}
      </b-col>
    </b-row>
    <b-row>
      <DashTable />
    </b-row>
    <b-row>
      <b-col>
        <Socket v-show="f" />
      </b-col>
      <b-col/>
      <b-col/>
    </b-row>
    <b-row :no-gutters="t">
      <b-col>
        Citizens on Hold: 0
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <DashHoldTable v-if="f"/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import ClientService from './client-service'
import Login from './Login'
import AddCitizen from './add-citizen/add-citizen'
import Socket from './Socket'
import DashTable from './dash-table'
import DashHoldTable from './dash-hold-table'

  export default {
    name: 'Dash',
    components: { 
      AddCitizen, 
      ClientService, 
      Login,
      Socket,
      DashTable,
      DashHoldTable
    },
    mounted() {
      this.$store.dispatch('getAllClients')
    },
    data() {
      return {
        t: true,
        f: false
      }
    },
    computed: {
      sortBy: {
        get() { return this.dash_status.sort },
        set(value) { this.$store.commit('updateDash'),{type:'sortby',value}}
      },
      ...mapState({
        citizens(state) {
          let filtered = state.citizens.filter(ctzn=>
            ctzn.service_reqs.length > 0
          )
        return filtered
        }
      }),
      ...mapGetters(['dash_status']),
      queueLength() {
        return this.citizens.length
      },
      sortDesc() {
        return this.dash_status.descending
      },
      totalRows() {
        return citizens.length()
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
      },
      clients() {
        return 
      }
    }
  }
</script>

<style>
  .dashrow {
    background-color: pink;
  }
