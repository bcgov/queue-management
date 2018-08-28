<template>
  <b-col cols="auto" class="p-0 m-0">
    <template v-if="setup === 'add_mode' || setup === 'edit_mode' ">
      <div v-if="setup === 'edit_mode' ">
        <b-button @click="clickEditApply" class="btn-primary" id="add-citizen-apply">Apply</b-button>
        <b-button @click="clickEditCancel" class="btn-secondary" id="add-citizen-cancel">Cancel</b-button>
      </div>
      <div v-else-if="setup === 'add_mode' ">
        <b-button class="btn-primary" @click="addServiceApply">Apply</b-button>
        <b-button class="btn-secondary" @click="clickEditCancel">Cancel</b-button>
      </div>
    </template>
    <template v-else>
      <div v-if="reception">
        <b-button @click="addToQueue" class="btn-primary" id="add-citizen-add-to-queue">Add to queue</b-button>
        <b-button @click="beginService" class="btn-primary" id="add-citizen-begin-service">Begin service</b-button>
        <b-button @click="cancelAddCitizensModal" class="btn-secondary" id="add-citizen-cancel">Cancel</b-button>
      </div>
      <div v-if="!reception">
        <b-button @click="beginService" class="btn-primary" id="add-citizen-begin-service">Begin service</b-button>
        <b-button @click="cancelAddCitizensModal" class="btn-secondary" id="add-citizen-cancel">Cancel</b-button>
      </div>
    </template>
  </b-col>
</template>

<script>
  import { mapGetters, mapActions, mapState } from 'vuex'

  export default {
    name: 'Buttons',

    computed: {
      ...mapGetters([ 'form_data', 'reception' ]),
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
