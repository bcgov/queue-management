<template>
  <v-app id="app">
    <div class="app-body">
      <app-header></app-header>
      <main>
        <router-view />
      </main>
    </div>

  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { AppHeader } from '@/components/common'
import KeyCloakService from '@/services/keycloak.services'

@Component({
  components: {
    AppHeader
  }
})
export default class App extends Vue {
  private async mounted () {
    await KeyCloakService.setKeycloakConfigUrl(`${process.env.VUE_APP_PATH}config/kc/keycloak.json`)
  }
}
</script>

<style lang="scss">
#app {
   font-family: 'Avenir', Helvetica, Arial, sans-serif;
   -webkit-font-smoothing: antialiased;
   -moz-osx-font-smoothing: grayscale;
   text-align: center;
   color: #2c3e50;
 }
</style>
