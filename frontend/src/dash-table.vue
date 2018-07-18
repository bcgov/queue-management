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
  <div id='client-table' class='client-table'>
    <b-table :small='t'
             :current-page="currentPage"
             :per-page="perPage"
             :items="clients"
             :fields="fields"
             :sort-by.sync="sortBy"
             :sort-desc.sync="sortDesc">
      <template slot="actions" slot-scope="row">
        <b-button size="sm" @click.stop="deleteCustomer(row.item)" class="mr-1">
          Delete
        </b-button>
      </template>
    </b-table>
    <b-pagination :total-rows="totalRows"
                  :per-page="perPage"
                  v-model="currentPage"
                  class="client-table-pagination"
                  />
  </div>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'

  export default {
    name: 'DashTable',
    props: ['tabe_status'],
    data() {
      return {
        t:'true',
        f:'false',
        fields: [
          {key: 'name', sortable: true},
          {key: 'id', sortable: true},
          {key: 'actions', label:'Actions'}
        ],
        sortby: this.table_status.sortby,
        page: this.table_status.page,
        perpage: this.table_status.perpage,
        descending: this.table_status.descending,
        totalRows: this.table_status.totalRows
      }
    }
  }
</script>
