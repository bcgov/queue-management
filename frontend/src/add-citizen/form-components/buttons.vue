<template>
      <b-col cols="auto" class="p-0 m-0">
        <template v-if="setup === 'reception' ">
         
            <b-button @click="addToQueue" class="btn-primary" id="add-citizen-add-to-queue">Add to queue</b-button>
            <b-button @click="beginService" class="btn-primary" id="add-citizen-begin-service">Begin service</b-button>
            <b-button @click="cancelAddCitizensModal" class="btn-secondary" id="add-citizen-cancel">Cancel</b-button>
    
        </template>
        <template v-else-if="setup == 'edit_mode' ">
        
            <b-button @click="clickEditApply" class="btn-primary" id="add-citizen-apply">Apply</b-button>
            <b-button @click="clickEditCancel" class="btn-secondary" id="add-citizen-cancel">Cancel</b-button>
     
        </template>
        <template v-else-if="setup == 'add_mode' ">
      
            <b-button @click="addServiceApply">Apply</b-button>
            <b-button @click="clickEditCancel">Cancel</b-button>
    
        </template>
        <template v-else-if="setup === 'non_reception' ">
         
            <b-button @click="beginService" class="btn-primary" id="add-citizen-begin-service">Begin service</b-button>
            <b-button @click="cancelAddCitizensModal" class="btn-secondary" id="add-citizen-cancel">Cancel</b-button>
   
        </template>
      </b-col>
</template>

<script>
  import { mapGetters, mapActions, mapState } from 'vuex'

  export default {
    name: 'Buttons',

    computed: {
      ...mapGetters([ 'form_data' ]),
      ...mapState({ setup: state => state.addModalSetup })
    },

    methods: {
      ...mapActions([
        'clickBeginService',
        'clickAddToQueue',
        'cancelAddCitizensModal',
        'applyEdits',
        'clickEditApply',
        'clickEditCancel',
        'clickAddServiceApply'
      ]),

      addToQueue() {
        if (this.form_data.service === '') {
          this.$store.commit('setModalAlert', 'You must select a service')
          this.$root.$emit('showAddMessage')
          return null
        }
        if (this.form_data.channel === '') {
          this.$store.commit('setModalAlert', 'You must select a channel')
          this.$root.$emit('showAddMessage')
          return null
        }
        this.clickAddToQueue()
      },

      beginService() {
        if (this.form_data.service === '') {
          this.$store.commit('setModalAlert', 'You must select a service')
          this.$root.$emit('showAddMessage')
          return null
        }
        if (this.form_data.channel === '') {
          this.$store.commit('setModalAlert', 'You must select a channel')
          this.$root.$emit('showAddMessage')
          return null
        }
        this.clickBeginService()
      },
        addServiceApply() {
            if (this.form_data.service === '') {
                this.$store.commit('setModalAlert', 'You must select a service')
                this.$root.$emit('showAddMessage')
                return null
            }
            if (this.form_data.channel === '') {
                this.$store.commit('setModalAlert', 'You must select a channel')
                this.$root.$emit('showAddMessage')
                return null
            }
            this.clickAddServiceApply()
        }

    }
  }
</script>
