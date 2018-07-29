

<template>
    <b-modal id="add_citizen_modal" 
             :visible="showAddModal" 
             size="lg"
             hide-header	
             hide-footer
             no-close-on-backdrop
             no-close-on-esc
             class="m-0 p-0"
             >
             
       <div style="display: flex; flex-direction: row; justify-content: space-between" class="modal_header">
         <div><h5>{{modalTitle}}</h5></div>
         <div>
           <b-button-close size="lg" 
                           @click="cancelAddCitizensModal" 
                           />
         </div>
         
       </div>
       <b-alert :show="dismissCountDown"
                style="h-align: center"
                variant="danger"
                @dismissed="dismissCountDown=0"
                @dismiss-count-down="countDownChanged">
         {{this.$store.state.alertMessage}}
       </b-alert>
      <AddCitizenForm />
      <b-container class="mt-3 pr-3">
        
        <b-row align-v="center" align-h="end">
          <b-col cols="auto" class="p-0">Quick Txn?</b-col>
          <b-col cols="1">
            <b-form-checkbox v-model="quickTrans"/>
          </b-col>
        <Buttons />
      </b-row>
      </b-container>
      
    </b-modal>
</template>

<script>

import {
  mapState, mapGetters, mapMutations, mapActions
}
from 'vuex'
import Buttons from './form-components/buttons'
import AddCitizenForm from './add-citizen-form'

export default {
    name: 'AddCitizen',
    components: {
        AddCitizenForm, Buttons
    },
    mounted() {
      this.$root.$on('showAddMessage', () => {
        this.showAlert()
      })
    },
    
    data() {
      return {
        dismissSecs: 5,
        dismissCountDown: 0
      }
    },
    
    computed: {
      ...mapState(['addCitizenModal', 'showAddModal']),
      ...mapGetters(['form_data', 'add_modal_setup']),
      
      modalTitle() {
        if (this.add_modal_setup === 'edit_mode') {
          return 'Edit Service'
        } else {
          return 'Search Screen'
        }
      },
      
      quickTrans: {
        get() { return this.form_data.quick },
        set(value) { this.updateModalForm({type:'quick',value}) }
      }
    },
    
    methods: {
      ...mapActions(['cancelAddCitizensModal']),
      ...mapMutations(['updateModalForm']),
      
      countDownChanged (dismissCountDown) {
        this.dismissCountDown = dismissCountDown
      },
      
      showAlert () {
        this.dismissCountDown = this.dismissSecs
      }
    }
  }

</script>