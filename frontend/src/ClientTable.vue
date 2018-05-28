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
    <b-table small
             :current-page="currentPage"
             :per-page="perPage"
             :items="this.$store.state.items"
             :fields="fields"
             :sort-by.sync="sortBy"
             :sort-desc.sync="sortDesc">
    </b-table>
      <b-pagination :total-rows="totalRows"
                    :per-page="perPage"
                    v-model="currentPage"
                    class="client-table-pagination">
      </b-pagination>
  </div>
</template>

<script>
  import Delete from './delete'

  export default {
    name: 'ClientTable',
    components: { Delete },
    data() {
      return {
        totalRows() {
          let items = this.$store.state.items
          return items.length
        },
        fields: [
          {key: 'name', sortable: true},
          {key: 'id', sortable: true}
        ],
        sortBy: 'id',
        currentPage: 1,
        perPage: 10,
        sortDesc: true
      }
    },
    created() {
      this.$store.dispatch('getAllClients')
    }
  }
</script>
