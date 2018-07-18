<template>
  <b-modal id="add_citizen_modal"
           v-model="showModal" 
           title="Search Screen"
           size="lg"
           >
    <template slot="modal-footer" style="v-l">
      <b-form-group label="Quick Txn?">
          <b-form-checkbox v-model="quickTrans"
                      id="add_citizen_quick_checkbox"
                      />
        </b-form-group>
        <Buttons />
      </b-form>
      
    </template>
    <AddCitizenForm />
  </b-modal>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import Buttons from './form-components/buttons'
  import AddCitizenForm from './add-citizen-form'
  
  export default {
    name: 'AddCitizen',
    components: { AddCitizenForm, Buttons },
    computed: {
      ...mapState(['addCitizenModal']),
      ...mapGetters(['form_data']),
      quickTrans: {
        get() { return this.form_data.quick },
        set(value) { this.$store.commit('updateModalForm',{type:'quick',value})}
      },
      showModal: {
        get() { return this.addCitizenModal.visible },
        set(value) {this.$store.commit('toggleAddCitizen', value)}
      }
    }
  }
</script>