<template>
  <v-alert
    v-if="!hideAlert"
    v-model="showEmailAlert"
    border="left"
    type="warning"
    close-text="Close Alert"
    color="warning"
    icon="mdi-alert-circle-outline"
    dense
    dismissible
>
    Please <span class="clickable" @click="goToAccountSettings">configure your email address</span> to receive notifications
</v-alert>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { User } from '@/models/user'
import { mapState } from 'vuex'

@Component({
  computed: {
    ...mapState('auth', [
      'currentUserProfile'
    ])
  }
})
export default class NoEmailAlert extends Vue {
  @Prop({ default: false })
  private hideAlert!: boolean

  private readonly currentUserProfile!: User
  private showEmailAlert: boolean = false

  private mounted () {
    this.showEmailAlert = !this.currentUserProfile?.email
  }

  private goToAccountSettings () {
    this.$router.push('/account-settings')
  }
}
</script>

<style lang="scss" scoped>
.clickable {
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
}
</style>
