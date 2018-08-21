

<template>  
  <b-container class="mt-4">
    <b-row>
      <b-col>
        <b-table 
        :fields="fields"
        :items="invited_service_reqs"
        head-variant="light"
        class="m-0 p-0 align-middle"
        small
        id="serve-table"
        fixed
        bordered
        style="text-align: center"
        >
          <template slot="status" slot-scope="row">
            <div v-if="row.item.periods.some(p=>p.time_end===null)===true">
              <div style="display: inline-block;
                          color: white;
                          font-size: .75rem;
                          padding-top: 3px;
                          padding-bottom: 2px;
                          padding-right: 10px;
                          padding-left: 10px;
                          border-radius: 16px;
                          border: 1.5px solid #2dc01d;
                          background-color: limegreen;"
                          >
                  Active
              </div>
            </div>
            <div v-if="row.item.periods.some(p=>p.time_end===null)===false">
              Innactive
            </div>
          </template>
          
          <template slot="quantity" slot-scope="row">
            <div v-if="row.item.periods.some(p=>p.time_end===null)===true" >
              <div class="w-25" style="margin: auto">
                <b-input :value="getQuantity()" @input="setQuantity" size="sm" style="height: 1.8em;"></b-input>
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
            <div v-if="row.item.periods.some(p => p.time_end === null) === true" >
              <b-button size="sm"
                        @click="clickEdit"
                        style="height: 1.8em;
                               display: inline-block;
                               padding-top: 3px;
                               padding-bottom: 3px;
                               padding-left: 8px;
                               padding-right: 8px;"
                        >
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
        {key:'status', label: 'Status', thStyle:'text-align: center;'},
        {key:'service.parent.service_name', tdClass: 'align-middle', label:'Category', thStyle:'text-align: center;'},
        {key:'service.service_name', tdClass: 'align-middle', label:'Service', thStyle:'text-align: center;'},
        {key:'quantity', label:'Quantity', thStyle:'text-align: center;'},
        {key:'editBut', label:'Change Service', thStyle:'text-align: center;'}
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
