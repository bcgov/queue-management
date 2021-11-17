<template>
  <b-col cols="auto" class="p-0 m-0" style="width:100%;">
    <template v-if="$route.path === '/appointments' ">
      <div class="button-row">
        <b-button class="btn-success ml-3" v-if="citizenButtons" @click="addService">Add</b-button>
        <b-button class="btn-danger" v-if="citizenButtons" @click="closeAddServiceModal">Cancel</b-button>
      </div>
    </template>
    <template v-if="$route.path !== '/appointments'">
      <template v-if="setup === 'add_mode' || setup === 'edit_mode' ">
        <div v-if="setup === 'edit_mode' " class="buttons-div">
          <b-button
            @click="clickEditCancel"
            :disabled="performingAction"
            v-if="citizenButtons"
            class="btn-danger"
            id="add-citizen-cancel"
          >Cancel</b-button>
          <b-button
            v-if="citizenButtons"
            @click="clickEditApply"
            :disabled="performingAction"
            class="btn-success"
            id="add-citizen-apply"
          >Apply</b-button>
        </div>
        <div v-if="setup === 'add_mode' " class="buttons-div">
          <b-button
            @click="clickEditCancel"
            v-if="citizenButtons"
            :disabled="performingAction"
            class="btn-danger"
          >Cancel</b-button>
          <b-button
            v-if="citizenButtons"
            @click="addServiceApply"
            :disabled="performingAction"
            class="btn-success"
          >Apply</b-button>
        </div>
      </template>
      <template v-else>
        <div v-if="!simplified && reception" class="buttons-div">
          <b-button
            @click="cancelAddCitizensModal"
            v-if="citizenButtons"
            :disabled="performingAction"
            class="btn-danger"
            id="add-citizen-cancel"
          >Cancel</b-button>
          <div style="display:inline-block">
            <b-button
              @click="addToQueue"
              v-if="citizenButtons"
              :disabled="performingAction || commentsTooLong"
              class="btn-white"
              id="add-citizen-add-to-queue"
            >Add to queue</b-button>
            <b-button
              @click="beginService"
              v-if="citizenButtons"
              :disabled="performingAction || commentsTooLong"
              class="btn-success"
              id="add-citizen-begin-service"
            >Begin service</b-button>
          </div>
        </div>
        <div v-if="!simplified && !reception" class="buttons-div">
          <b-button
            @click="cancelAddCitizensModal"
            :disabled="performingAction"
            v-if="citizenButtons"
            class="btn-danger"
            id="add-citizen-cancel"
          >Cancel</b-button>
          <b-button
            @click="beginService"
            v-if="citizenButtons"
            :disabled="performingAction"
            class="btn-success"
            id="add-citizen-begin-service"
          >Begin service</b-button>
        </div>
        <div v-if="simplified" class="buttons-div">
          <b-button
            @click="cancelAddCitizensModal"
            v-if="citizenButtons"
            :disabled="performingAction"
            class="btn-danger"
            id="add-citizen-cancel"
          >Cancel</b-button>
          <b-button
            @click="beginServiceSimplified"
            v-if="citizenButtons"
            :disabled="performingAction"
            class="btn-success"
            id="add-citizen-begin-service"
          >Begin service</b-button>
        </div>
      </template>
    </template>
  </b-col>
</template>

<script lang="ts">
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class Buttons extends Vue {
  @State('addModalSetup') private setup!: any
  @State('performingAction') private performingAction!: any
  @State('addModalForm') private addModalForm!: any
  @State('citizenButtons') private citizenButtons!: any

  @Getter('form_data') private form_data!: any;
  @Getter('reception') private reception!: any;
  @Getter('commentsTooLong') private commentsTooLong!: any;

  @Action('applyEdits') public applyEdits: any
  @Action('cancelAddCitizensModal') public cancelAddCitizensModal: any
  @Action('clickAddServiceApply') public clickAddServiceApply: any
  @Action('clickAddToQueue') public clickAddToQueue: any
  @Action('clickBeginService') public clickBeginService: any
  @Action('clickEditApply') public clickEditApply: any
  @Action('clickEditCancel') public clickEditCancel: any
  @Action('resetAddCitizenModal') public resetAddCitizenModal: any

  @Mutation('toggleAddModal') public toggleAddModal: any
  @Mutation('toggleExamsTrackingIP') public toggleExamsTrackingIP: any

  get simplified () {
    if (this.$route.path !== '/queue') {
      return true
    }
    return false
  }

  addService () {
    this.$store.commit('appointmentsModule/setSelectedService', this.addModalForm.service)
    this.closeAddServiceModal()
  }

  addServiceApply () {
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

  addToQueue () {
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
  }

  beginService () {
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
    this.clickBeginService({ simple: false })
  }

  beginServiceSimplified () {
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
    this.clickBeginService({ simple: true })
  }

  closeAddServiceModal () {
    this.resetAddCitizenModal()
    this.$store.commit('appointmentsModule/toggleApptBookingModal', true)
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
