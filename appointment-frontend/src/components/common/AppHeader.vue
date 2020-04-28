<template>
  <v-app-bar
    dark
    fixed
    height="64"
  >
    <v-img
      class="mx-2"
      src="@/assets/img/gov3_bc_logo.png"
      max-width="132"
      contain
    ></v-img>
    <v-toolbar-title>Service BC Appointments</v-toolbar-title>

    <v-spacer></v-spacer>

    <template v-if="!isAuthenticated">
      <div class="mb-1">
        <v-btn
          dark
          outlined
          class="mr-3"
          min-width="90"
          @click="register"
          >
          Register
        </v-btn>
        <v-btn
          light
          min-width="90"
          @click="login"
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

  async mounted () {
  }

  login () {
    this.$router.push('/signin/bcsc')
  }
  register () {
    this.$router.push('/signin/bcsc')
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
</style>
