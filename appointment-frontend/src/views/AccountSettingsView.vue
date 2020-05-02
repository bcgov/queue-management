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

              <v-text-field
                v-model="phoneNumber"
                :rules="phoneNumberRules"
                label="Phone"
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
                  @click="updateProfile"
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
import { AccountModule, AuthModule } from '@/store/modules'
import { Component, Vue } from 'vue-property-decorator'
import { User, UserUpdateBody } from '@/models/user'
import { mapActions, mapState } from 'vuex'
import { getModule } from 'vuex-module-decorators'

@Component({
  components: {
  },
  computed: {
    ...mapState('auth', [
      'currentUserProfile'
    ])
  },
  methods: {
    ...mapActions('account', [
      'updateUserAccount'
    ])
  }
})
export default class AccountSettingsView extends Vue {
  private accountModule = getModule(AccountModule, this.$store)
  private authModule = getModule(AuthModule, this.$store)
  private readonly currentUserProfile!: User
  private readonly updateUserAccount!: (userBody: UserUpdateBody) => Promise<any>
  private valid:boolean = false
  private name:string = ''
  private email:string = ''
  private phoneNumber:string = ''
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

  private phoneNumberRules = [
    v => !!v || 'Phone number is required'
  ]

  private async beforeMount () {
    if (this.currentUserProfile) {
      this.name = this.currentUserProfile.display_name
      this.email = this.currentUserProfile.email
      this.phoneNumber = this.currentUserProfile.telephone
      this.enableReminder = this.currentUserProfile.send_reminders
    }
  }

  private async updateProfile () {
    const userUpdate: UserUpdateBody = {
      email: this.email,
      telephone: this.phoneNumber,
      send_reminders: this.enableReminder
    }
    const response = await this.updateUserAccount(userUpdate)
    // eslint-disable-next-line no-console
    console.log(response)
  }

  private goToAppointments () {
    this.$router.push('/booked-appointments')
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
