<template>
  <div>
    <form inline>
      <b-button class="btn-primary" @click="prev">
        <font-awesome-icon icon="angle-left"
                           class="m-0 p-0"
                           style="font-size: 1rem;"/>
      </b-button>
      <b-button class="btn-primary" @click="next">
        <font-awesome-icon icon="angle-right"
                           class="m-0 p-0"
                           style="font-size: 1rem;"/>
      </b-button>
      <b-button class="btn-primary mx-2" @click="today">This Week</b-button>
    </form>
  </div>
</template>

<script>
  export default {
    name: 'ButtonsAgenda',
    methods: {
      next() {
        this.$root.$emit('next')
      },
      prev() {
        this.$root.$emit('prev')
      },
      today() {
        this.$root.$emit('today')
      },
    }
  }
</script>