<template>
  <div>
    <router-view />
  </div>
</template>

<script lang="ts">
import { AccountModule, AuthModule } from '@/store/modules'
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapGetters } from 'vuex'
import { KCUserProfile } from '@/models/KCUserProfile'
import KeyCloakService from '@/services/keycloak.services'
import TokenService from '@/services/token.services'
import { getModule } from 'vuex-module-decorators'

@Component({
  components: {},
  computed: {
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  methods: {
    ...mapActions('account', ['loadUserInfo', 'getUser']),
    ...mapActions('auth', ['syncWithSessionStorage'])
  }
})
export default class MainApp extends Vue {
  private authModule = getModule(AuthModule, this.$store)
  private accountModule = getModule(AccountModule, this.$store)
  private readonly getUser!: () => void
  private readonly isAuthenticated!: boolean
  private readonly loadUserInfo!: () => KCUserProfile
  private readonly syncWithSessionStorage!: () => void
  private tokenService = new TokenService()

  private async beforeMount () {
    await KeyCloakService.setKeycloakConfigUrl('/config/kc/keycloak-public.json')
    this.syncWithSessionStorage()
  }

  private async mounted () {
    this.$store.commit('updateHeader')
    await this.initSetup()
    // Listen for event from signin component so it can initiate setup
    this.$root.$on('signin-complete', async (callback) => {
      await this.initSetup()
      callback()
    })
  }

  private async initSetup () {
    // eslint-disable-next-line no-console
    console.log('authenticaiton check:')
    // eslint-disable-next-line no-console
    console.log(this.isAuthenticated)
    if (this.isAuthenticated) {
      // Removed redundant "await" calls on next two lines
      // this.loadUserInfo()
      // this.getUser()
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
}
</script>

<style lang="scss">
.task-outer-container .row .v-select .vs__dropdown-toggle {
    width: 100% !important;
    height: 100% !important;
  }
  .service-flow-body {
    padding-right: 0px !important;
    overflow-y: hidden !important;
}
</style>
