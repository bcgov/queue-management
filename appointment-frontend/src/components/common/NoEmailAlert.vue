<template>
  <v-alert
    v-if="!hideAlert"
    v-model="showAlert"
    border="left"
    type="warning"
    close-text="Close Alert"
    color="warning"
    icon="mdi-alert-circle-outline"
    dense
    dismissible
>
  <div v-if="isEmailMissing">Please <router-link to="account-settings">configure your email address</router-link> to receive notifications.</div>
  <div v-if="isReminderFlagMissing">Please <router-link to="account-settings">subscribe to email reminders</router-link> to receive appointment reminders.</div>
  <div v-if="isPhoneMissing">Please <router-link to="account-settings">add your phone number</router-link> to ensure we can contact you.</div>
  <div v-if="isSmsReminderFlagMissing">Please <router-link to="account-settings">subscribe to sms text message reminders </router-link> to receive appointment reminders.</div>
</v-alert>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import ConfigHelper from '@/utils/config-helper'
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
  private showAlert: boolean = false

  private isEmailMissing:boolean = false
  private isPhoneMissing:boolean = false
  private isReminderFlagMissing:boolean = false
  private isSmsReminderFlagMissing:boolean = false

  private mounted () {
    this.showAlert = !this.currentUserProfile?.email || !this.currentUserProfile?.sendEmailReminders
    if (ConfigHelper.isEmsEnabled()) {
      this.showAlert = this.showAlert || !this.currentUserProfile?.telephone || !this.currentUserProfile?.sendSmsReminders
    }

    if (!this.currentUserProfile?.email) {
      this.isEmailMissing = true
    } else if (!this.currentUserProfile?.sendEmailReminders) {
      this.isReminderFlagMissing = true
    }

    if (ConfigHelper.isEmsEnabled()) {
      if (!this.currentUserProfile?.telephone) {
        this.isPhoneMissing = true
      } else if (!this.currentUserProfile?.sendSmsReminders) {
        this.isSmsReminderFlagMissing = true
      }
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
