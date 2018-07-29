<template>
  <b-form-row>
      <b-col align-h="end">
        <template v-if="setup === 'reception' ">
          <b-form-group>
            <b-button @click="addToQueue">Add to queue</b-button>
            <b-button @click="beginService">Begin service</b-button>
            <b-button @click="cancelAddCitizensModal">Cancel</b-button>
          </b-form-group>
        </template>
        <template v-else-if="setup == 'edit_mode' ">
          <b-form-group>
            <b-button @click="clickEditApply">Apply</b-button>
            <b-button @click="clickEditCancel">Cancel</b-button>
          </b-form-group>
        </template>
        <template v-else-if="setup === 'non_reception' ">
          <b-form-group>
            <b-button @click="beginService">Begin service</b-button>
            <b-button @click="cancelAddCitizensModal">Cancel</b-button>
          </b-form-group>
        </template>
      </b-col>
    </b-form-row>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  
  export default {
    name: 'Buttons',
    
    computed: {
      ...mapGetters({
        form_data: 'form_data', 
        setup: 'add_modal_setup'
      })
    },
    methods: {
      ...mapActions([
        'clickBeginService',
        'clickAddToQueue',
        'cancelAddCitizensModal',
        'applyEdits',
        'clickEditApply',
        'clickEditCancel'
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
      }
    }
  }
</script>