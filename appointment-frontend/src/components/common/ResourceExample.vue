<template>
  <v-card>
    <h1>Welcome {{name}}</h1>
    <p>This is your message: {{message}}</p>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class ResourceExample extends Vue {
  @Prop({ default: '' })
  private name!: string

  @Prop({ default: '' })
  private message!: string
}
</script>

<style lang="scss" scoped>
</style>
