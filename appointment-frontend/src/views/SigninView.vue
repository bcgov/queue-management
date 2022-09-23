<template>
  <loading-screen :is-loading="isLoading"></loading-screen>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapGetters } from 'vuex'
import { KCUserProfile } from '@/models/KCUserProfile'
import KeyCloakService from '@/services/keycloak.services'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import TokenService from '@/services/token.services'

@Component({
  components: {
    LoadingScreen
  },
  computed: {
    ...mapGetters('auth', [
      'isAuthenticated'
    ])
  },
  methods: {
    ...mapActions('account', ['loadUserInfo']),
    ...mapActions('auth', ['postCreateUser'])
  }
})
export default class SigninView extends Vue {
  // private accountModule = getModule(AccountModule, this.$store)
  private isLoading = true
  @Prop({ default: 'bcsc' }) idpHint!: string
  @Prop({ default: '' }) redirectUrl: string
  @Prop({ default: '' }) redirectUrlLoginFail!: string
  private readonly loadUserInfo!: () => KCUserProfile
  private readonly postCreateUser!: () => void
  private readonly isAuthenticated!: boolean

  private callsp () {
    (window as any).snowplow('trackPageView')
  }

  private async mounted () {
    // Initialize keycloak session
    const kcInit = this.initKeycloak(this.idpHint)
    kcInit.then(async (authenticated: boolean) => {
      if (authenticated) {
        // Set values to session storage
        KeyCloakService.initSession()
        // tell KeycloakServices to load the user info
        this.loadUserInfo()
        // Removed redundant "await" on next line
        this.postCreateUser()
        // eslint-disable-next-line no-console
        console.info('[SignIn.vue]Logged in User.Starting refreshTimer')
        const tokenService = new TokenService()
        await tokenService.init()
        tokenService.scheduleRefreshTimer()

        if (this.isAuthenticated) {
          this.$root.$emit('signin-complete', () => {
            // perform redirection here
            this.$router.push('/appointment')
            this.callsp()
          })
        }
      }
    })
      .catch(() => {
        if (this.redirectUrlLoginFail) {
          window.location.assign(decodeURIComponent(this.redirectUrlLoginFail))
        }
      })
  }

  async initKeycloak (idpHint: string) {
    return KeyCloakService.init(idpHint, this.$store)
  }
}
</script>

<style lang="scss" scoped>
// empty block
</style>
