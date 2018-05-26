<template>
  <div>
    <b-form-input v-model="name"
                  id="client_name"
                  type="text"
                  placeholder="Client Name"
                  />
    <b-button @click="buttonClick()">
      Add to Queue
    </b-button>
  </div>
</template>

<script>
  export default {
    name: 'ClientInput',
    data() {
      return {
        name: ''
      }
    },
    methods: {
      buttonClick() {
        this.$store.dispatch('postClient', {name: this.name})
        this.name = ''
      }
    }
  }
</script>


