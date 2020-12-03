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
  <div v-if="isEmailMissing">Please <router-link to="account-settings">configure your email address</router-link> to receive notifications</div>
  <div v-if="isReminderFlagMissing">Please <router-link to="account-settings">subscribe to email reminders</router-link> to receive appointment reminders</div>
  <div v-if="isPhoneMissing">Please <router-link to="account-settings">add your phone number</router-link> to receive notifications and ensure we can contact you.</div>
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

  private isEmailMissing:boolean = false
  private isPhoneMissing:boolean = false
  private isReminderFlagMissing:boolean = false

  private mounted () {
    this.showEmailAlert = !this.currentUserProfile?.email || !this.currentUserProfile?.send_reminders || !this.currentUserProfile?.telephone

    if (!this.currentUserProfile?.email) {
      this.isEmailMissing = true
    } else if (!this.currentUserProfile?.send_reminders) {
      this.isReminderFlagMissing = true
    }
    if (!this.currentUserProfile?.telephone) {
      this.isPhoneMissing = true
    }
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
