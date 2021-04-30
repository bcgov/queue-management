<template>
  <div>
    <form inline>
      <b-button class="btn-primary" @click="prev">
        <font-awesome-icon icon="angle-left" class="m-0 p-0" style="font-size: 1rem;" />
      </b-button>
      <b-button class="btn-primary ml-1" @click="next">
        <font-awesome-icon icon="angle-right" class="m-0 p-0" style="font-size: 1rem;" />
      </b-button>
      <b-button class="btn-primary mx-2" @click="today">This Week</b-button>
    </form>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component({})
export default class ButtonsAgenda extends Vue {
  next () {
    this.$root.$emit('agenda-next')
  }

  prev () {
    this.$root.$emit('agenda-prev')
  }

  today () {
    this.$root.$emit('agenda-today')
  }
}

</script>
