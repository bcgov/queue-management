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
      'callSnowplow'
    ])
  }
})
export default class AppHeader extends Vue {
  private readonly isAuthenticated!: boolean
  private readonly currentOffice!: Office
  private readonly currentService!: Service
  private readonly callSnowplow!: (mySP: any) => any
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
    // snowplow call needs null value not undefined, and depending on where we click login button, one of these values might be undefined.
    // eslint-disable-next-line no-console
    console.log('APP HEADER called - this.currentOffice?.office_name', this.currentOffice)
    // eslint-disable-next-line no-console
    console.log('APP HEADER called - this.currentService?.external_service_name', this.currentService)
    if (this.currentOffice?.office_name === undefined) {
      this.curOffice = null
    } else {
      this.curOffice = this.currentOffice?.office_name
    }
    if (this.currentService?.external_service_name === undefined) {
      this.curService = null
    } else {
      this.curService = this.currentService?.external_service_name
    }

    let mySP = {}
    switch (page) {
      case 'register':
        mySP = { step: 'Register', loggedIn: this.isAuthenticated, apptID: null, clientID: null, loc: this.curOffice, serv: this.curService }
        this.callSnowplow(mySP)
        break
      case 'login':
        mySP = { step: 'Login to Account', loggedIn: this.isAuthenticated, apptID: null, clientID: null, loc: this.curOffice, serv: this.curService }
        this.callSnowplow(mySP)
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
