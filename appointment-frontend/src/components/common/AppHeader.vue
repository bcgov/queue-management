<template>
  <v-app-bar
    dark
    fixed
    height="64"
  >
    <v-img
      v-if="!isWalkin"
      class="mx-2 bc-logo"
      data-cy="header-image-bcgov"
      :src="($vuetify.breakpoint.xs) ? require('@/assets/img/gov3_bc_logo_mobile.png') : require('@/assets/img/gov3_bc_logo.png')"
      max-width="132"
      contain
      @click="goTo('home')"
    ></v-img>
    <v-img
      v-else
      class="mx-2 bc-logo"
      :src="($vuetify.breakpoint.xs) ? require('@/assets/img/gov3_bc_logo_mobile.png') : require('@/assets/img/gov3_bc_logo.png')"
      :max-width="($vuetify.breakpoint.xs) ? 60 : 132"
      contain
      @click="goTo('home')"
    ></v-img>
    <v-toolbar-title v-if="!isWalkin">Service BC Appointments</v-toolbar-title>
    <v-spacer></v-spacer>
    <template v-if="((!isAuthenticated) && (!isWalkin))">
      <div class='d-flex'>
        <v-btn
          light
          class="mr-3"
          min-width="90"
          @click="goTo('login')"
          >
          Login
        </v-btn>
        <v-btn
          dark
          outlined
          class="mr-3"
          min-width="90"
          @click="goTo('register')"
          >
          Register
        </v-btn>
      </div>
    </template>
    <template v-else>
      <SignedUser v-if="(!isWalkin)" :username="username"></SignedUser>
    </template>
    <v-btn
      outlined
      alt='Help - opens in new window'
      class='mr-3'
      @click="goTo('help')">
      <v-icon small class="mr-2">mdi-open-in-new</v-icon>
      Help
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'
import { Office } from '@/models/office'
import { Service } from '@/models/service'
import SignedUser from './SignedUser.vue'
import { User } from '@/models/user'

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
    ...mapState('auth', [
      'currentUserProfile'
    ]),
    ...mapGetters('auth', [
      'isAuthenticated'
    ]),
    ...mapGetters('account', [
      'username'
    ])
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
  private readonly currentUserProfile!: User
  private readonly callSnowplowClick!: (mySP: any) => any
  private readonly username!: string
  private curService: string
  private curOffice: string
  private isWalkin:boolean = false

  async mounted () {
    this.isWalkin = window.location.href.includes('walk-in-Q')
  }

  private callsp () {
    (window as any).snowplow('trackPageView')
  }

  login () {
    this.$router.push('/login')
    this.callsp()
  }

  register () {
    this.$router.push('/login')
    this.callsp()
  }

  private goTo (page) {
    let currStep = ''
    let theloc = null
    let theserv = null
    switch (this.$store.state.spLastStep) {
      case 1:
        currStep = 'Location Selection'
        break
      case 2:
        currStep = 'Select Service'
        theloc = this.currentOffice?.officeName
        break
      case 3:
        currStep = 'Select Date'
        theloc = this.currentOffice?.officeName
        theserv = this.currentService?.externalServiceName
        break
      case 4:
        currStep = 'Login to Confirm Appointment'
        break
      default:
        break
    }
    let mySP = {}
    switch (page) {
      case 'register':
        mySP = { label: 'Register', step: currStep, loggedIn: this.isAuthenticated, apptID: null, clientID: this.currentUserProfile?.userId, loc: theloc, serv: theserv, url: 'https://appointments.servicebc.gov.bc.ca/login' }
        this.callSnowplowClick(mySP)
        this.$router.push('/login')
        this.callsp()
        break
      case 'login':
        mySP = { label: 'Login', step: currStep, loggedIn: this.isAuthenticated, apptID: null, clientID: this.currentUserProfile?.userId, loc: theloc, serv: theserv, url: 'https://appointments.servicebc.gov.bc.ca/login' }
        this.callSnowplowClick(mySP)
        this.$router.push('/login')
        this.callsp()
        break
      case 'home':
        this.$router.push('/')
        this.callsp()
        break
      case 'help':
        mySP = { label: 'Help', step: currStep, loggedIn: this.isAuthenticated, apptID: null, clientID: this.currentUserProfile?.userId, loc: theloc, serv: theserv, url: 'https://www2.gov.bc.ca/gov/content/home/get-help-with-government-services' }
        this.callSnowplowClick(mySP)
        window.open('https://www2.gov.bc.ca/gov/content/home/get-help-with-government-services', '_blank')
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
