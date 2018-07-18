<template>

      <b-form-group>
        <template v-if="office == 1">
          <div id="button_group_1">
            <b-button @click="addQueue">Add to queue</b-button>
            <b-button @click="beginService">Begin service</b-button>
            <b-button>Cancel</b-button>
          </div>
        </template>
        <template v-else-if="office == 2">
          <div id="button_group_2">
            <b-button @click="beginService">Apply</b-button>
            <b-button>Cancel</b-button>
          </div>
        </template>
        <template v-else-if="office == 3">
          <div id="button_group_3">
            <b-button @click="beginService">Begin service</b-button>
            <b-button>Cancel</b-button>
          </div>
        </template>
      </b-form-group>
</template>

<script>
  
  export default {
    name: 'Buttons',
    data() {
      return {
        notice: 'ddfdffds ssssss'
      }
    },
    computed: {
      office() {
        return this.$store.state.userOfficeType
      },
      ready() {
        return this.$store.getters.add_citizen_form_ready
      }
    },
    methods: {
      beginService() {
        if (this.ready) {
          this.$store.dispatch('putCitizenInService')
        } else if (!this.ready) {
          this.notice = 'some warning'
        }
      },
      addQueue() {
        this.$store.dispatch('putCitizenInQueue')
      }
    }
  }
</script>