<template>
  <v-app-bar
    dark
    fixed
    height="64"
  >
    <v-img
      v-if="!isWalkin"
      class="mx-2 bc-logo"
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
    <v-toolbar-title v-if="!isWalkin">Service BC Appointments <v-chip pill color='info'>Beta</v-chip></v-toolbar-title>

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

    <template v-if="((!isAuthenticated) && (!isWalkin))">
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
      <SignedUser v-if="(!isWalkin)" :username="username"></SignedUser>
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import { AccountModule, AuthModule } from '@/store/modules'
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapGetters } from 'vuex'
import SignedUser from './SignedUser.vue'

@Component({
  components: {
    SignedUser
  },
  computed: {
    ...mapGetters('auth', ['isAuthenticated']),
    ...mapGetters('account', ['username'])
  }
})
export default class AppHeader extends Vue {
  private readonly isAuthenticated!: boolean
  private readonly username!: string
  private isWalkin:boolean = false

  async mounted () {
    this.isWalkin = window.location.href.includes('walk-in-Q')
  }

  login () {
    this.$router.push('/login')
  }

  register () {
    this.$router.push('/login')
  }

  private goTo (page) {
    switch (page) {
      case 'register':
      case 'login': this.$router.push('/login')
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
