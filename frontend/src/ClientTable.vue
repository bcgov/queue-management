<template>
  <b-table small :items="items"></b-table>
</template>

<script>
  export default {
    name: 'ClientTable',
    data() {
      return {
        items: this.$store.state.items
      }
    }
  }
</script>