

<template>  
  <b-container class="mt-4">
    <b-row>
      <b-col>
        <b-table 
        :fields="fields"
        :items="invited_service_reqs"
        head-variant="light"
        small
        id="serve-table"
        fixed
        bordered
        style="text-align: center"
        >
          <template slot="status" slot-scope="row">
            <div v-if="row.item.periods.some(p=>p.time_end===null)===true">
              <b-badge variant="success" size="sm">
                <h6 class="pt-1 px-2" style="font-size: 15px">
                  Active
                </h6> 
              </b-badge>
            </div>
            <div v-if="row.item.periods.some(p=>p.time_end===null)===false">
              Innactive
            </div>
          </template>
          
          <template slot="quantity" slot-scope="row">
            <div v-if="row.item.periods.some(p=>p.time_end===null)===true" >
              <div class="w-25" style="margin: auto">
                <b-input :value="getQuantity()" @input="setQuantity" size="sm"></b-input>
              </div>
            </div>
            <div v-if="row.item.periods.some(p=>p.time_end===null)===false">
              {{ invited_service_reqs[row.index].quantity }}
            </div>
          </template>
          
          <template slot="service.service_name" slot-scope="row">
            {{ row.item.service.service_name }}
            <div style="display: none">
              {{ 
                row.item.periods.some(p=>p.time_end===null) ? 
                   row.item._rowVariant='info' : row.item._rowVariant='' 
              }}
            </div>
          </template>
              
          <template slot="editBut"  slot-scope="row">
            <div v-if="row.item.periods.some(p=>p.time_end===null)===true" >
              <b-button size="sm" @click="clickEdit">
                edit
              </b-button>
            </div>
            <div v-if="row.item.periods.some(p=>p.time_end===null)===false">
              <b-button size="sm" variant="link" @click="clickMakeActive(row.item.sr_id)">
              make active
              </b-button>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

export default {
  name: 'ServeCitizenTable',
  
  data() {
    return {
      fields: [
        {key:'status', label: 'Status', thStyle:'text-align: center; font-size: 15px'},
        {key:'service.parent.service_name', label:'Category', thStyle:'text-align: center; font-size: 15px'},
        {key:'service.service_name', label:'Service', thStyle:'text-align: center; font-size: 15px'},
        {key:'quantity', label:'Quantity', thStyle:'text-align: center; font-size: 15px'},
        {key:'editBut', label:'Change Service', thStyle:'text-align: center; font-size: 15px'}
      ]
    }
  },
  
  computed: {
    ...mapState(['serviceModalForm']),
    ...mapGetters([
      'invited_service_reqs', 
      'active_service',
      'active_index'
    ])
  },
  
  methods: {
    ...mapActions([
      'clickEdit', 
      'clickMakeActive'
    ]),
    ...mapMutations(['editServiceModalForm']),
    
    formatTime(data) {
      let time = new Date(data)
      return time.toLocaleTimeString()
    },
    
    setQuantity(value) {
      this.editServiceModalForm({
        type: 'activeQuantity',
        value
      })
    },
    
    getQuantity() { 
      if (!this.serviceModalForm.activeQuantity) {
        return ''
      } else {
        return this.serviceModalForm.activeQuantity
      }
    }
  }
}
</script>




