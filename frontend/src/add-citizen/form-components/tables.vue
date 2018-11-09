<template>
  <b-container fluid
               class="mt-1 add_citizen_form"
               style="border: 1px solid dimgrey;
                      margin: 0px;
                      padding-left: 0px;
                      padding-right: 0px;
                      padding-bottom: 7px;"
                      >
    <b-form-row no-gutters class="m-0"
                style="background-color: #f0f2f8;
                       border-top: 2px solid white;
                       border-bottom: 2px solid #e6e9ed;
                       height: 35px;
                       padding-top: 7px;
                       padding-left: 0px;"
                       >
      <b-col class="m-0 p-0">&nbsp&nbspService</b-col>
      <b-col class="m-0 p-0">Category</b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
        <div id="innertable"
             style="height: 200px;
                    overflow-y: scroll;
                    margin: 0px;
                    background-color: #fcfcfc"
                    >
          <b-table :items="filtered_services"
                   :fields="fields"
                   sort-by="parrent.service_name"
                   :filter="filter"
                   :small="t"
                   :bordered="f"
                   :striped="f"
                   :fixed="t"
                   id="table2"
                   @row-clicked="rowClicked"
                   class="add_citizen_categories_table"
                   >
            <template slot="service_name" slot-scope="data">
              <div>
                <span v-bind:title="data.item.service_desc">
                  {{data.item.service_name}}
                </span>
                <div style="display: none">
                  {{
                    (data.item.service_id==form_data.service) ?
                    (data.item._rowVariant='active') : (data.item._rowVariant='')
                  }}
                </div>
              </div>
            </template>
          </b-table>
        </div>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
  import { mapState, mapGetters, mapMutations } from 'vuex'

  export default {
    name: 'Tables',

    data() {
      return {
        f:false,
        t:true,
        fields: [
          { key: 'service_name', label: 'Service', sortable: false, thClass: 'd-none' },
          { key: 'parent.service_name', label: 'Category', sortable: false, thClass: 'd-none' },
          { key: 'service_desc', label: 'Description', sortable: false, thClass: 'd-none', tdClass: 'd-none' }
        ]
      }
    },

    computed: {
      ...mapState(['addCitizenModal']),
      ...mapGetters(['form_data', 'filtered_services']),

      filter(value) {
        return this.form_data.search
      }
    },

    methods: {
      ...mapMutations(['setAddModalSelectedItem']),

      rowClicked(item, index) {
        let id = item.service_id
        this.setAddModalSelectedItem(item.service_name)
        this.selectedRow = id
        this.$store.commit('updateAddModalForm', {type:'service',value:id})
      }
    }
  }
</script>

<style>
.add_citizen_categories_table {
  padding: 0px;
}
</style>
