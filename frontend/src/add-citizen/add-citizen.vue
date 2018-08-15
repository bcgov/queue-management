

<template>
    <b-modal 
             :visible="showAddModal"
             size="lg"
             hide-header
             hide-footer
             no-close-on-backdrop
             no-close-on-esc
             class="m-0 p-0"
             @shown="setupForm()"
             >

       <div style="display: flex; flex-direction: row; justify-content: space-between" class="modal_header">
         <div><h5>{{modalTitle}}</h5></div>
         <div>
           <b-button-close size="lg"
                           @click="cancelAddCitizensModal" />
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
          <b-col cols="1" class="p-0 mr-1">Quick Txn?</b-col>
          <b-col col cols="1" class="p-0">
            <b-form-checkbox  v-model="quickTrans" value="1" unchecked-value="0"/>
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
      ...mapState(['addCitizenModal', 'showAddModal', 'addModalSetup', 'serviceModalForm']),
      ...mapGetters(['form_data', 'reception']),
      
      modalTitle() {
        if (this.addModalSetup === 'edit_mode') {
          return 'Edit Service'
        } else {
          return 'Add Citizen'
        }
      },

      quickTrans: {
        get() { return this.form_data.quick },
        set(value) { this.updateAddModalForm({type:'quick',value}) }
      }
    },

    methods: {
      ...mapActions(['cancelAddCitizensModal']),
      ...mapMutations(['updateAddModalForm', 'setDefaultChannel']),

      countDownChanged (dismissCountDown) {
        this.dismissCountDown = dismissCountDown
      },
      setupForm() {
        if (!this.serviceModalForm.citizen_id) {
          this.setDefaultChannel()
          if (!this.reception) {
            this.$root.$emit( 'focusfilter' )
          } else if (this.reception) {
            this.$root.$emit( 'focuscomments' )
          }
        }
        if (this.serviceModalForm.citizen_id) {
          this.$root.$emit( 'focusfilter' )
        }
      },
      showAlert () {
        this.dismissCountDown = this.dismissSecs
      }
    }
  }
</script>

<style>
  .disabled {
    background-color: #8e9399 !important;
    color: Gainsboro !important;
  }
  .disabled:hover {
    background-color: #8e9399 !important;
  }
</style>
