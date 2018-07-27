<template>
  <b-form-row>
      <b-col align-h="end">
        <template v-if="setup === reception">
          <b-form-group>
            <b-button @click="addToQueue">Add to queue</b-button>
            <b-button @click="beginService">Begin service</b-button>
            <b-button @click="cancelAddCitizensModal">Cancel</b-button>
          </b-form-group>
        </template>
        <template v-else-if="setup == serve_now">
          <b-form-group>
            <b-button @click="beginService">Apply</b-button>
            <b-button @click="cancelAddCitizensModal">Cancel</b-button>
          </b-form-group>
        </template>
        <template v-else-if="setup === non_reception">
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
    data() {
      return {
        non_reception: 'non_reception',
        serve_now: 'serve_now',
        reception: 'reception'
      }
    },
    computed: {
      ...mapGetters({
        form_data: 'form_data', 
        setup: 'search_screen_setup'
      })
    },
    methods: {
      ...mapActions([
        'clickBeginService',
        'clickAddToQueue',
        'cancelAddCitizensModal'
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