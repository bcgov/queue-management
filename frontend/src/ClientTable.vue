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
             <template slot="actions" slot-scope="row">
        <!-- We use @click.stop here to prevent a 'row-clicked' event from also happening -->
        <b-button size="sm" @click.stop="deleteCustomer(row.item)" class="mr-1">
          Delete
        </b-button>

      </template>
    </b-table>
      <b-pagination :total-rows="totalRows"
                    :per-page="perPage"
                    v-model="currentPage"
                    class="client-table-pagination">
      </b-pagination>
  </div>
</template>

<script>

  export default {
    name: 'ClientTable',
    data() {
      let length = this.$store.state.items.length
      return {
        totalRows: length,
        fields: [
          {key: 'name', sortable: true},
          {key: 'id', sortable: true},
          {key: 'actions', label:'Actions'}
        ],
        sortBy: 'id',
        currentPage: 1,
        perPage: 10,
        sortDesc: true
      }
    },
    created() {
      this.$store.dispatch('getAllClients')
    },
    methods: {
      deleteCustomer(item) {
        let id = item.id
        let url = `/citizens/${id}/`
        this.$axios.delete(url, { headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
          }
        })
        console.log(`delete id ${id}`)
      }
    }
  }
</script>
