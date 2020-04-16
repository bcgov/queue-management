<template>
  <v-app-bar
    dark
    fixed
    height="64"
  >
    <v-img
      class="mx-2"
      src="@/assets/img/gov3_bc_logo.png"
      max-width="132"
      contain
    ></v-img>
    <v-toolbar-title>Service BC Appointments</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn
      light
      @click="login"
      >
      Login
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class AppHeader extends Vue {
  login () {
    this.$router.push('/signin/bcsc')
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";

.v-app-bar {
  background-color: $BCgovBlue5 !important;
  border-bottom: 2px solid $BCgovGold5 !important;
}
</style>
