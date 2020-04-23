<template>
  <loading-screen :is-loading="isLoading"></loading-screen>
</template>
<script lang="ts">
import { AccountModule, AuthModule } from '@/store/modules'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { KCUserProfile } from '@/models/KCUserProfile'
import KeyCloakService from '@/services/keycloak.services'
import LoadingScreen from '@/components/common/LoadingScreen.vue'
import TokenService from '@/services/token.services'
import { getModule } from 'vuex-module-decorators'
import { mapActions } from 'vuex'

@Component({
  components: {
    LoadingScreen
  },
  methods: {
    ...mapActions('account', ['loadUserInfo'])
  }
})
export default class SigninView extends Vue {
  // private accountModule = getModule(AccountModule, this.$store)
  private isLoading = true
  @Prop({ default: 'bcsc' }) idpHint!: string
  @Prop({ default: '' }) redirectUrlLoginFail!: string
  private readonly loadUserInfo!: () => KCUserProfile

  private async mounted () {
    // Initialize keycloak session
    const kcInit = await this.initKeycloak(this.idpHint)
    kcInit.success(async (authenticated: boolean) => {
      if (authenticated) {
        // Set values to session storage
        KeyCloakService.initSession()
        // tell KeycloakServices to load the user info
        this.loadUserInfo()
        // eslint-disable-next-line no-console
        console.info('[SignIn.vue]Logged in User.Starting refreshTimer')
        let tokenService = new TokenService()
        await tokenService.init()
        tokenService.scheduleRefreshTimer()
        this.$router.push('/appointment')
      }
    })
      .error(() => {
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
</style>
