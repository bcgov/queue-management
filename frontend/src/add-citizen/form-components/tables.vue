<template>
  <b-container fluid 
               class="mt-1 add_citizen_form"
               style="border: 1px solid silver;
                      border-radius: 6px;
                      margin: 0 px;
                      padding: 6px;"
                      >
    <b-form-row no-gutters class="add_citizen_form_table">
      <b-col class="ml-2">Service</b-col>
      <b-col>Category</b-col>
    </b-form-row>
    <b-form-row no-gutters>
      <b-col>
        <div id="innertable"
             style="height: 200px; 
                    overflow-y: scroll;
                    margin: 4px;"
                    >
          <b-table :items="services" 
                   :fields="fields"
                   :filter="filter"
                   :small="t"
                   :bordered="f"
                   :striped="f"
                   :fixed="t"
                   id="table2"
                   :thstyle="thstyle"
                   @row-clicked="rowClicked"
                   class="add_citizen_categories_table"
                   > 
            <template slot="service_name" slot-scope="data">
              {{data.item.service_name}}
              <div style="display: none">
               {{ (data.item.service_id==form_data.service) ?
                    (data.item._rowVariant='active') :
                      (data.item._rowVariant='') }}
              </div>
            </template>
          </b-table>
        </div>
      </b-col>
    </b-form-row>
  </b-container>
  </b-col>
</b-form-row>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  
  export default {
    name: 'Tables',
    data() {
      return {
        thstyle: {
          display: 'none',
          hidden: true
        },
        f:false,
        t:true,
        fields: [
          {
            key: 'service_name',
            label: 'Service',
            sortable: false,
            thStyle:{display: 'none'}
          },
          {
            key: 'parent.service_name',
            label: 'Category',
            sortable: false,
            thStyle:{display: 'none'}
          }
        ]
      }
    },
    computed: {
      ...mapState(['addCitizenModal']),
      ...mapGetters(['index','form_data']),
      filter() {
        return this.form_data.search
      },
      index() {
        return this.index
      },
      services() {
        if (this.$store.state.services) {
          let category = this.form_data.category
          if (category === '') {
            return this.$store.state.services
          } else if (category) {
            let services = this.$store.state.services.filter(
              srv => srv.parent.service_id === category
            )
            return services
          } 
        }
      }
    },
    methods: {
      rowClicked(item, index) {
        let id = item.service_id
        this.selectedRow = id
        this.$store.commit('updateModalForm', {type:'service',value:id})
      }
    }
  }
</script

<style>
.add_citizen_categories_table {
  padding: 0px;
}
</style>