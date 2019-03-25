<template>
  <b-col cols="auto" class="p-0 m-0" style="width:100%;">
    <template v-if="setup === 'add_mode' || setup === 'edit_mode' ">
      <div v-if="setup === 'edit_mode' " class="buttons-div">
        <b-button @click="clickEditCancel"
                  :disabled="performingAction"
                  class="btn-danger"
                  id="add-citizen-cancel">Cancel</b-button>
        <b-button @click="clickEditApply"
                  :disabled="performingAction"
                  class="btn-success"
                  id="add-citizen-apply">Apply</b-button>
      </div>
      <div v-if="setup === 'add_mode' " class="buttons-div">
        <b-button @click="clickEditCancel"
                  :disabled="performingAction"
                  class="btn-danger" >Cancel</b-button>
        <b-button @click="addServiceApply"
                  :disabled="performingAction"
                  class="btn-success" >Apply</b-button>
      </div>
    </template>
    <template v-else>
      <div v-if="!simplified && reception" class="buttons-div">
        <b-button @click="cancelAddCitizensModal"
                  :disabled="performingAction"
                  class="btn-danger"
                  id="add-citizen-cancel">Cancel</b-button>
        <div style="display:inline-block">
          <b-button @click="addToQueue"
                    :disabled="performingAction"
                    class="btn-white"
                    id="add-citizen-add-to-queue">Add to queue</b-button>
          <b-button @click="beginService"
                    :disabled="performingAction"
                    class="btn-success"
                    id="add-citizen-begin-service">Begin service</b-button>
        </div>
      </div>
      <div v-if="!simplified && !reception" class="buttons-div">
        <b-button @click="cancelAddCitizensModal"
                  :disabled="performingAction"
                  class="btn-danger"
                  id="add-citizen-cancel">Cancel</b-button>
        <b-button @click="beginService"
                  :disabled="performingAction"
                  class="btn-success"
                  id="add-citizen-begin-service">Begin service</b-button>
      </div>
      <div v-if="simplified" class="buttons-div">
        <b-button @click="cancelAddCitizensModal"
                  :disabled="performingAction"
                  class="btn-danger"
                  id="add-citizen-cancel">Cancel</b-button>
        <b-button @click="beginServiceSimplified"
                  :disabled="performingAction"
                  class="btn-success"
                  id="add-citizen-begin-service">Begin service</b-button>
      </div>
    </template>
  </b-col>
</template>

<script>
  import { mapGetters, mapActions, mapMutations, mapState } from 'vuex'

  export default {
    name: 'Buttons',
    computed: {
      ...mapGetters({
        form_data: 'form_data',
        reception: 'reception',
      }),
      ...mapState({
        setup: 'addModalSetup',
        performingAction: 'performingAction',
      }),
      simplified() {
        if (this.$route.path !== '/queue') {
          return true
        }
        return false
      },
    },
    methods: {
      ...mapMutations(['toggleExamsTrackingIP']),
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
        this.clickBeginService({simple: false})
      },
      beginServiceSimplified() {
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
        this.toggleExamsTrackingIP(true)
        this.clickBeginService({simple: true})
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

<style scoped>
.buttons-div {
    display: flex;
    width: 100%;
    justify-content: space-between;
}
.btn-white {
    background: white;
    color: black;
    border: 1px solid #cecece;
}
#btn-white:hover {
    background: #e8e8e8;
}
</style>
