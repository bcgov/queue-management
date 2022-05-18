<template>
  <v-menu bottom left fixed transition="slide-y-transition" content-class="account-menu">
    <template v-slot:activator="{ on }">
      <v-btn text large v-on="on" class="mb-1" :class="{'pr-0': $vuetify.breakpoint.xs}">
        <v-avatar data-cy="appointment-cancel-user-nav" color="grey lighten-1" light left size="32" class="black--text mr-2">
          {{ username.slice(0,1) }}
        </v-avatar>
        <div class="user-info" v-if="!$vuetify.breakpoint.xs">
          <div class="user-name" data-test="user-name">{{ username }}</div>
        </div>
        <v-icon small class="ml-2">mdi-chevron-down</v-icon>
      </v-btn>
    </template>
    <v-list tile dense>
      <v-list-item two-line>
        <v-list-item-avatar size="34" color="primary" class="white--text font-weight-bold mr-3">
          {{ username.slice(0,1) }}
        </v-list-item-avatar>
        <v-list-item-content class="user-info">
          <v-list-item-title class="user-name" data-test="menu-user-name">{{ username }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item @click="goTo('appointments')">
        <v-list-item-icon left>
          <v-icon>mdi-calendar-multiple</v-icon>
        </v-list-item-icon>
        <v-list-item-title data-cy="appointment-cancel-nav-appointments">My Appointments</v-list-item-title>
      </v-list-item>
      <v-list-item @click="goTo('account')">
        <v-list-item-icon left>
          <v-icon>mdi-account-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-title data-cy="account-settings-nav">Account Settings</v-list-item-title>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item @click="goTo('logout')">
        <v-list-item-icon left>
          <v-icon>mdi-logout-variant</v-icon>
        </v-list-item-icon>
        <v-list-item-title>Log out</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component({
})
export default class SignedUser extends Vue {
  @Prop({ default: '' })
  private username:string

  private async mounted () {
    // I assume this is intentionally empty.
  }

  private callsp () {
    (window as any).snowplow('trackPageView')
  }

  private goTo (page) {
    switch (page) {
      case 'appointments':
        this.$router.push('/booked-appointments')
        this.callsp()
        break
      case 'account':
        this.$router.push('/account-settings')
        this.callsp()
        break
      case 'logout':
        this.$router.push('/signout')
        this.callsp()
        break
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";

.user-name {
  font-weight: 600 !important;
  text-transform: uppercase !important;
}
</style>
