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
  <div v-html="alertText"></div>

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

  private alertText: string = ''

  private mounted () {
    this.showEmailAlert = !this.currentUserProfile?.email || !this.currentUserProfile?.send_reminders
    if (!this.currentUserProfile?.email) {
      this.alertText = 'Please <a href="#" @click="goToAccountSettings">configure your email address</a> to receive notifications'
    } else if (!this.currentUserProfile?.send_reminders) {
      this.alertText = 'Please <a href="#" @click="goToAccountSettings">subscribe to email reminders</a> to receive appointment reminders'
    }
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
