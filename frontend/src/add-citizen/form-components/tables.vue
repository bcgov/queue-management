<template>
  <div style="
         border: 1px solid silver;
         border-radius: 6px;
         padding: 6px;
       ">
    <b-table :fields="fields"
             id="table1"
             :small="t"
             :bordered="f"
             :fixed="t"
             >
             <template slot="HEAD_service_name" slot-scope="data">
               {{data.label}} 
             </template>
             <template slot="HEAD_parent.service_name" slot-scope="data">
               {{data.label}}
             </template>
    </b-table>
    <div style="
           height:200px; 
           overflow-y: scroll;
           margin-top: 0px;
         ">
  <b-table :items="services" 
           :fields="fields"
           :filter="filter"
           :small="t"
           :bordered="f"
           :striped="f"
           :fixed="t"
           id="table2"
           thead-class="header-table"
           @row-clicked="rowClicked"
           > 
             <template slot="HEAD_service_name" slot-scope="data">
               <div style="display: none">lala</div>
             </template>
             <template slot="HEAD_parent.service_name" slot-scope="data">
               <div style="display: none">lala</div>
             </template>
             <template slot="service_name" slot-scope="data">
               {{data.item.service_name}}
               <div style="display: none">
                 {{(data.item.service_id==selectedRow)?
                   (data.item._rowVariant='active'):
                    (data.item._rowVariant='')}}
               </div>
             </template>
  </b-table>
</div>
  
</div>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  
  export default {
    name: 'Tables',
    data() {
      return {
        selectedRow:'',
        f:false,
        t:true,
        fields: [
          {
            key: 'service_name',
            label: 'Service',
            sortable: false
          },
          {
            key: 'parent.service_name',
            label: 'Category',
            sortable: false
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

<style scoped>
.header-table{
  display: none;
}
</style>