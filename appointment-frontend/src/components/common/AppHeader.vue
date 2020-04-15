<template>
  <v-app-bar
    color="navBg"
    dark
  >
    <v-toolbar-title>Service BC Appointments</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn
      light
      >
      Login
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class AppHeader extends Vue {
}
</script>

<style lang="scss" scoped>
</style>
