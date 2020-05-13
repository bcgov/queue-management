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
          My Appointments
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
              <div class="mb-6">
                <div class="caption">Name</div>
                <div class="title font-weight-bold">{{name}}</div>
              </div>

              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="Email"
                required
                outlined
              ></v-text-field>

              <v-text-field
                v-model="phoneNumber"
                label="Phone"
                outlined
              ></v-text-field>

              <v-switch
                inset
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
    <v-snackbar
      multi-line
      :color="showMsg.msgType"
      v-model="showMsg.isShow"
      class="font-weight-bold"
    >
      {{ showMsg.msgText }}
    </v-snackbar>
  </v-container>
</template>

<script lang="ts">
// Libraries
import { AccountModule, AuthModule } from '@/store/modules'
import { Component, Vue } from 'vue-property-decorator'
import { User, UserUpdateBody } from '@/models/user'
import { mapActions, mapGetters, mapState } from 'vuex'
import { getModule } from 'vuex-module-decorators'

@Component({
  components: {
  },
  computed: {
    ...mapState('auth', [
      'currentUserProfile'
    ]),
    ...mapGetters('account', ['username'])
  },
  methods: {
    ...mapActions('account', [
      'updateUserAccount',
      'getUser'
    ])
  }
})
export default class AccountSettingsView extends Vue {
  private accountModule = getModule(AccountModule, this.$store)
  private authModule = getModule(AuthModule, this.$store)
  private readonly currentUserProfile!: User
  private readonly updateUserAccount!: (userBody: UserUpdateBody) => Promise<any>
  private readonly getUser!: () => void
  private readonly username!: string
  private valid:boolean = false
  private name:string = ''
  private email:string = ''
  private phoneNumber:string = ''
  private enableReminder:boolean = false
  private showMsg = {
    isShow: false,
    msgText: '',
    msgType: 'info'
  }

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
    v => /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/.test(v) || 'Phone number must be valid'
  ]

  private async beforeMount () {
    if (!this.currentUserProfile.user_id) {
      await this.getUser()
    }
    if (this.currentUserProfile) {
      this.name = this.username || ' '
      this.email = this.currentUserProfile.email
      this.phoneNumber = this.currentUserProfile.telephone
      this.enableReminder = this.currentUserProfile.send_reminders
    }
  }

  private async updateProfile () {
    try {
      const userUpdate: UserUpdateBody = {
        email: this.email,
        telephone: this.phoneNumber,
        send_reminders: this.enableReminder
      }
      const response = await this.updateUserAccount(userUpdate)
      if (response?.user_id) {
        this.showMsg.isShow = true
        this.showMsg.msgText = 'Profile Successfully Updated!'
        this.showMsg.msgType = 'success'
      }
    } catch (error) {
      this.showMsg.isShow = true
      this.showMsg.msgText = 'Error! Unable to Update Profile'
      this.showMsg.msgType = 'error'
    }
  }

  private goToAppointments () {
    this.$router.push('/booked-appointments')
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
