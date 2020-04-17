<template>
  <v-app id="app">
    <div class="app-body">
      <app-header></app-header>
      <main class="main-block container">
        <router-view />
      </main>
      <app-footer></app-footer>
    </div>

  </v-app>
</template>

<script lang="ts">
import { AppFooter, AppHeader } from '@/components/common'
import { Component, Vue } from 'vue-property-decorator'
import KeyCloakService from '@/services/keycloak.services'

@Component({
  components: {
    AppHeader,
    AppFooter
  }
})
export default class App extends Vue {
  private async mounted () {
  }

  private async beforeMount () {
    await KeyCloakService.setKeycloakConfigUrl(`${process.env.VUE_APP_PATH}config/kc/keycloak.json`)
  }
}
</script>

<style lang="scss">
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.main-block {
  margin-top: 64px;
}
</style>
