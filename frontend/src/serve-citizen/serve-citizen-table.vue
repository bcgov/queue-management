

<template>  
  <b-container class="mt-4">
    <b-row>
      <b-col>
        <b-table :fields="fields"
                 :items="service_reqs"
                 head-variant="light"
                 small
                 id="serve-table"
                 fixed
                 bordered
                 style="text-align: center; veritcal-align: middle"
                 >
                 <template slot="status" slot-scope="row">
                   <div v-if="row.index === 0" >
                     <b-badge variant="success">Active </b-badge>
                   </div>
                   <div v-if="row.index > 0">
                     Finished
                   </div>
                 </template>
                 <div style="al"
                 <template slot="quantity" slot-scope="row">
                   <div v-if="row.index === 0">
                     <div class="w-25" style="margin: auto">
                       <b-input v-model="quantity" size="sm"></b-input>
                     </div>
                   </div>
                   <div v-if="row.index > 0">
                     {{ citizen.service_reqs[row.index].quantity }}
                   </div>
                 </template>
                 <template slot="editBut" v-if="row.index===0" slot-scope="row">
                   <b-button size="sm" @click="clickEdit">
                     edit
                   </b-button>
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
        text1: '',
        fields: [
          {key:'status', label: 'Status'},
          {key:'service.parent.service_name', label:'Category'},
          {key:'service.service_name', label:'Service'},
          {key:'quantity', label:'Quantity'},
          {key:'editBut', label:'Change Service'}
        ]
      }
    },
    computed: {
      ...mapState({
        citizen: 'invitedCitizen',
        currentQuantity: 'currentQuantity'
      }),
      ...mapGetters(['service_reqs']),
      quantity: {
        get() { return this.citizen.service_reqs[0].quantity },
        set(value) { this.editInvitedQuantity({type:'quantity', value}) }
      }
    },
    methods: {
      ...mapActions(['clickEdit']),
      ...mapMutations(['editInvitedQuantity']),

      formatTime(data) {
        let time = new Date(data)
        return time.toLocaleTimeString()
      }
    }
  }
</script>


