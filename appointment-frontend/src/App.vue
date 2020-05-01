<template>
  <v-app id="app">
    <div class="app-body">
      <app-header :key="$store.state.refreshKey"></app-header>
      <main class="main-block container">
        <router-view />
      </main>
      <app-footer></app-footer>
    </div>

  </v-app>
</template>

<script lang="ts">
import { AccountModule, AuthModule } from '@/store/modules'
import { AppFooter, AppHeader } from '@/components/common'
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapGetters } from 'vuex'
import ConfigHelper from '@/utils/config-helper'
import { KCUserProfile } from '@/models/KCUserProfile'
import KeyCloakService from '@/services/keycloak.services'
import { SessionStorageKeys } from '@/utils'
import TokenService from '@/services/token.services'
import { User } from './models/user'
import { getModule } from 'vuex-module-decorators'

@Component({
  components: {
    AppHeader,
    AppFooter
  },
  computed: {
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  methods: {
    ...mapActions('account', ['loadUserInfo']),
    ...mapActions('auth', ['syncWithSessionStorage'])
  }
})
export default class App extends Vue {
  private authModule = getModule(AuthModule, this.$store)
  private accountModule = getModule(AccountModule, this.$store)
  private readonly loadUserInfo!: () => KCUserProfile
  private readonly syncWithSessionStorage!: () => void
  private readonly isAuthenticated!: boolean
  private tokenService = new TokenService()

  private async beforeMount () {
    // eslint-disable-next-line no-console
    console.log(`${process.env.VUE_APP_PATH}config/kc/keycloak.json`)
    await KeyCloakService.setKeycloakConfigUrl(`${process.env.VUE_APP_PATH}config/kc/keycloak.json`)
    this.syncWithSessionStorage()
  }

  private async mounted () {
    // eslint-disable-next-line no-console
    console.log('this.isAuthenticated ', this.isAuthenticated)
    this.$store.commit('updateHeader')
    this.loadUserInfo()
    // Listen for event from signin component so it can initiate setup
    this.$root.$on('signin-complete', async (callback) => {
      await this.initSetup()
      callback()
    })
  }

  private getAccountFromSession (): User {
    return JSON.parse(ConfigHelper.getFromSession(SessionStorageKeys.CurrentUserProfile || '{}'))
  }

  private async initSetup () {
    // eslint-disable-next-line no-console
    console.log('this.isAuthenticated ', this.isAuthenticated)
    if (this.isAuthenticated) {
      this.loadUserInfo()
      try {
        await this.tokenService.init(this.$store)
        this.tokenService.scheduleRefreshTimer()
      } catch (e) {
        // eslint-disable-next-line no-console
        console.log('Could not initialize token refresher: ' + e)
        // this.$store.dispatch('user/reset')
        this.$store.commit('loadComplete')
        this.$router.push('/')
      }
    }
    this.$store.commit('loadComplete')
  }

  private destroyed () {
    this.$root.$off('signin-complete')
  }
}
</script>

<style lang="scss">
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  color: #2c3e50;
}
.main-block {
  margin-top: 64px;
  margin-bottom: 50px;
}
</style>
