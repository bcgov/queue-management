<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="9">
        <v-btn
          color="primary"
          text
          class="mb-2"
          @click="goToAppointments"
        >
          <v-icon left class="mr-2">mdi-arrow-left</v-icon>
          Return to My Appointments
        </v-btn>
        <v-card>
          <v-card-title>
            <h2 class="px-4 py-2">Account Settings</h2>
          </v-card-title>
          <v-card-text class="px-6">
            <v-divider></v-divider>
            <v-form
              class="pt-6"
              ref="accountSettingsForm"
              v-model="valid"
              lazy-validation
            >
              <v-text-field
                v-model="name"
                :rules="nameRules"
                label="Name"
                required
                outlined
                readonly
              ></v-text-field>

              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="Email"
                required
                outlined
              ></v-text-field>

              <v-switch
                v-model="enableReminder"
                label="Send me appointment reminders via email"
              ></v-switch>
            </v-form>
            <v-row>
              <v-col class="d-flex">
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  large
                >
                  Update
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
// Libraries
import { Component, Vue } from 'vue-property-decorator'

@Component({
  components: {
  }
})
export default class AccountSettingsView extends Vue {
  private valid:boolean = false
  private name:string = 'Jon Snow'
  private email:string = ''
  private enableReminder:boolean = false

  $refs: {
    accountSettingsForm: HTMLFormElement
  }

  private nameRules = [
    v => !!v || 'Name is required'
  ]

  private emailRules = [
    v => !!v || 'Email is required',
    v => /.+@.+\..+/.test(v) || 'Email must be valid'
  ]

  private goToAppointments () {
    this.$router.push('/booked-appointments')
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
