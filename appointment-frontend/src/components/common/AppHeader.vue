<template>
  <v-app-bar
    dark
    fixed
    height="64"
  >
    <v-img
      class="mx-2 bc-logo"
      :src="($vuetify.breakpoint.xs) ? require('@/assets/img/gov3_bc_logo_mobile.png') : require('@/assets/img/gov3_bc_logo.png')"
      max-width="132"
      contain
      @click="goTo('home')"
    ></v-img>
    <v-toolbar-title>Service BC Appointments <v-chip pill color='info'>Beta</v-chip></v-toolbar-title>

    <v-spacer></v-spacer>

    <v-btn
      href="https://www2.gov.bc.ca/gov/content/home/get-help-with-government-services"
      target="_blank"
      outlined
      alt='Help - opens in new window'
      class='mx-3'>
      <v-icon small class="mr-2">mdi-open-in-new</v-icon>
      Help
    </v-btn>

    <template v-if="!isAuthenticated">
      <div class='d-flex'>
        <v-btn
          dark
          outlined
          class="mr-3"
          min-width="90"
          @click="goTo('register')"
          >
          Register
        </v-btn>
        <v-btn
          light
          min-width="90"
          @click="goTo('login')"
          >
          Login
        </v-btn>
      </div>
    </template>
    <template v-else>
      <SignedUser :username="username"></SignedUser>
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import { AccountModule, AuthModule, OfficeModule } from '@/store/modules'
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import SignedUser from './SignedUser.vue'

@Component({
  components: {
    SignedUser
  },
  computed: {
    ...mapState('office', [
      'currentOffice',
      'currentService',
      'currentSnowPlow'
    ]),
    ...mapGetters('auth', ['isAuthenticated']),
    ...mapGetters('account', ['username'])
  },
  methods: {
    ...mapActions('office', [
      'callSnowplowClick'
    ])
  }
})
export default class AppHeader extends Vue {
  private readonly isAuthenticated!: boolean
  private readonly currentOffice!: Office
  private readonly currentService!: Service
  private readonly callSnowplowClick!: (mySP: any) => any
  private readonly username!: string
  private curService: string
  private curOffice: string

  async mounted () {
  }

  login () {
    this.$router.push('/login')
  }
  register () {
    this.$router.push('/login')
  }
  private goTo (page) {
    let currStep = ''
    switch (this.$store.state.spLastStep) {
      case 1:
        currStep = 'Locations List'
        break
      case 2:
        currStep = 'Service Selection'
        break
      case 3:
        currStep = 'Date Selection'
        break
      case 4:
        currStep = 'Login to Confirm'
        break
      default:
        break
    }
    let mySP = {}
    switch (page) {
      case 'register':
        mySP = { label: 'Register', step: currStep, loc: null, serv: null, url: 'https://appointments.servicebc.gov.bc.ca/login' }
        this.callSnowplowClick(mySP)
        break
      case 'login':
        mySP = { label: 'Login', step: currStep, loc: null, serv: null, url: 'https://appointments.servicebc.gov.bc.ca/login' }
        this.callSnowplowClick(mySP)
        this.$router.push('/login')
        break
      case 'home': this.$router.push('/')
        break
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";

.v-app-bar {
  background-color: $BCgovBlue5 !important;
  border-bottom: 2px solid $BCgovGold5 !important;
}
.user-name {
  font-weight: 600 !important;
  text-transform: uppercase !important;
}
.bc-logo {
  cursor: pointer;
}
</style>
