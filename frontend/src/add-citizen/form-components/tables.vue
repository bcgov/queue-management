<template>
  <b-container fluid
               class="add_citizen_form"
               style="border: 1px solid dimgrey;
                      margin: 0px;
                      padding-left: 0px;
                      padding-right: 0px;
                      padding-bottom: 5px;"
                      >
    <b-form-row no-gutters class="m-0 add_citizen_table_header"
                       >
      <b-col class="m-0 p-0">&nbsp&nbspService</b-col>
      <b-col class="m-0 p-0" v-if="!simplifiedModal">Category</b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
        <div id="innertable"
             style="height: 200px;
                    overflow-y: scroll;
                    margin: 0px;
                    background-color: #fcfcfc">
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
                   class="add_citizen_categories_table">
            <template slot="service_name" slot-scope="data">
              <div>
                <span v-bind:title="data.item.service_desc">
                  {{data.item.service_name}}
                </span>
                <div style="display: none">
                  {{ data.item.service_id==form_data.service ?
                      data.item._rowVariant='active' : data.item._rowVariant='' }}
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
      }
    },
    computed: {
      ...mapState({
        addModalSetup: 'addModalSetup',
        addCitizenModal: 'addCitizenModal',

      }),
      ...mapGetters({form_data: 'form_data', filtered_services: 'filtered_services',}),
      simplified() {
        if (this.$route.path !== '/queue') {
          return true
        }
        return false
      },
      simplifiedModal() {
        if (this.simplified && this.addModalSetup !== 'edit_mode') {
          return true
        }
        return false
      },
      fields() {
        if (!this.simplifiedModal) {
          return [
            { key: 'service_name', label: 'Service', sortable: false, thClass: 'd-none', tdClass: 'addcit-td',},
            { key: 'parent.service_name', label: 'Category', sortable: false, thClass: 'd-none', tdClass: 'addcit-td',},
            { key: 'service_desc', label: 'Description', sortable: false, thClass: 'd-none', tdClass: 'd-none',}
          ]
        }
        return [
          { key: 'service_name', label: 'Service', sortable: false, thClass: 'd-none', tdClass: 'addcit-td',},
        ]
      },
      filter(value) {
        if (!this.simplified) {
          return this.form_data.search
        }
        return 'Exams'
      },
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
.add_citizen_table_header {
    background-color: rgb(179, 183, 186);
    color: white;
    height: 35px;
    padding-top: 6px;
    padding-left: 0px;
    text-align: center;
    font-size: 17px;
    text-shadow: 0px 0px 2px #a5a5a5;
}
.addcit-td {
  cursor: pointer;
}
</style>
