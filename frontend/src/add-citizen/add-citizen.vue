

<template>
  <b-col >
    <b-button @click="clickModal">Add Citizen</b-button>
    <b-modal id="add_citizen_modal" 
             :visible="showModal" 
             size="lg"
             no-close-on-backdrop
             no-close-on-esc
             class="m-0 p-0"
             >
        <template slot="modal-header">
          <b-form-row>
            <b-col no-gutters class="p-0 m-0">
          <h6>Search Screen</h6>
        </b-col>
      </b-form-row>
        </template>
        <template slot="modal-footer" style="v-l">
            <b-form-group label="Quick Txn?">
                <b-form-checkbox v-model="quickTrans" id="add_citizen_quick_checkbox" />
            </b-form-group>
            <Buttons />
            </b-form>
        </template>
        <AddCitizenForm />
    </b-modal>
  </b-col>
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
    computed: {
      ...mapState(['addCitizenModal']),
      ...mapGetters(['form_data']),
      quickTrans: {
        get() { return this.form_data.quick },
        set(value) { this.updateModalForm({type:'quick',value}) }
      },
      showModal() {
        return this.addCitizenModal.visible
      }
    },
    methods: {
      ...mapMutations(['toggleAddCitizen','updateModalForm']),
      ...mapActions(['addCitizen']),
      ...mapMutations(['toggleAddCitizen']),
      clickModal() {
        this.toggleAddCitizen(true)
        this.addCitizen()
      }
    }
  }

</script>