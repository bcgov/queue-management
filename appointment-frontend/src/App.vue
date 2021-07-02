<template>
  <v-app id="app">
    <div class="app-body" :class="{'app-mobile': $vuetify.breakpoint.xs}">
      <app-header :key="$store.state.refreshKey"></app-header>
      <feedback v-if="(isFeedbackEnabled && (!isWalkin))"></feedback>
      <main class="main-block container">
        <v-alert
          border="left"
          type="info"
          close-text="Close Alert"
          color="#d9eaf7"
          icon="mdi-alert-circle-outline"
          dense
          dismissible
        >
          <div class="bc-gov-alertbanner bc-gov-alertbanner-info text-center container py-2" role="alert">
            {{ headerMsg[0] }} <a :href="headerLinks[0]" target="_blank">{{ headerMsg[1] }}</a>
            {{ headerMsg[2] }} <a :href="headerLinks[1]" target="_blank">{{ headerMsg[3] }}</a>
            {{ headerMsg[4] }} <a :href="headerLinks[2]" target="_blank">{{ headerMsg[5] }}</a>
            {{ headerMsg[6] }} <a :href="headerLinks[3]" target="_blank">{{ headerMsg[7] }}</a>
            {{ headerMsg[8] }} <a :href="headerLinks[4]" target="_blank">{{ headerMsg[9] }}</a>
          </div>
        </v-alert>
      <router-view />
      </main>
      <app-footer id="footer"></app-footer>
    </div>

  </v-app>
</template>

<script lang="ts">
import { AccountModule, AuthModule } from '@/store/modules'
import { AppFooter, AppHeader } from '@/components/common'
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapGetters } from 'vuex'
import CommonUtils from './utils/common-util'
import ConfigHelper from '@/utils/config-helper'
import { Feedback } from './components/feedback'
import { KCUserProfile } from '@/models/KCUserProfile'
import KeyCloakService from '@/services/keycloak.services'
import { SessionStorageKeys } from '@/utils'
import TokenService from '@/services/token.services'
import { User } from './models/user'
import { getModule } from 'vuex-module-decorators'

@Component({
  components: {
    AppHeader,
    AppFooter,
    Feedback
  },
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
export default class App extends Vue {
  private authModule = getModule(AuthModule, this.$store)
  private accountModule = getModule(AccountModule, this.$store)
  private readonly loadUserInfo!: () => KCUserProfile
  private readonly syncWithSessionStorage!: () => void
  private readonly getUser!: () => void
  private readonly isAuthenticated!: boolean
  private tokenService = new TokenService()
  private isScrolled = false
  private isFeedbackEnabled: boolean = ConfigHelper.isFeedbackEnabled()
  private isWalkin:boolean = false
  private headerMsg = []
  private headerLinks = []

  private async beforeMount () {
    await KeyCloakService.setKeycloakConfigUrl(`${process.env.VUE_APP_PATH}config/kc/keycloak-public.json`)
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
    this.isWalkin = window.location.href.includes('walk-in-Q')
    let hm = ConfigHelper.getHeaderText()
    let hl = ConfigHelper.getHeaderLinks()
    this.headerMsg = hm.split('{link}')
    this.headerLinks = hl.split('{link}')
  }

  private getAccountFromSession (): User {
    return JSON.parse(ConfigHelper.getFromSession(SessionStorageKeys.CurrentUserProfile || '{}'))
  }

  private async initSetup () {
    // eslint-disable-next-line no-console

    if (this.isAuthenticated) {
      await this.loadUserInfo()
      await this.getUser()
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
.app-mobile {
  .main-block {
    padding: 0;
    padding-top: 4px;
  }
}
body {
  font-family: 'BC Sans', 'Noto Sans', Arial, 'sans serif';
  color: #313132;
  font-size: 16px;
  line-height: 1.5em;
}

a {
  text-decoration: underline;
}

.bc-gov-alertbanner {
  border: 1px solid transparent;
  border-radius: 4px;
  font-weight: 700;
  margin-bottom: 20px;
  padding: 15px;
}

.bc-gov-alertbanner:before {
  float: left;
  font-family: 'Font Awesome 5 Free';
  font-size: larger;
  font-style: normal;
  line-height: 1;
  margin-right: 10px;
  position: relative;
  top: 3px;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
}

.bc-gov-alertbanner p {
  font-size: 18px;
  margin: 0;
  padding-left: 35px;
}

.bc-gov-alertbanner-error {
  background-color: #f2dede;
  border-color: #ebccd1;
  color: #a12622;
}

.bc-gov-alertbanner-error:before {
  content: "\f06a";
}

.bc-gov-alertbanner-error a {
  color: #843534;
}

.bc-gov-alertbanner-warning {
  background-color: #f9f1c6;
  border-color: #faebcc;
  color: #6c4a00;
}

.bc-gov-alertbanner-warning:before {
  content: "\f071";
}

.bc-gov-alertbanner-warning a {
  color: #66512c;
}

.bc-gov-alertbanner-info {
  background-color: #d9eaf7;
  color: black;
}

.bc-gov-alertbanner-info a {
  color: #1a5a96;
}

.bc-gov-alertbanner-success {
  background-color: #dff0d8;
  border-color: #d6e9c6;
  color: #2d4821;
}

.bc-gov-alertbanner-success:before {
  content: "\f058";
}

.bc-gov-alertbanner-success a {
  color: #2b542c;
}
</style>
