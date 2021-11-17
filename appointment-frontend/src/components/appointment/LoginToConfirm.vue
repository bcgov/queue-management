<template>
  <v-card-text>
    <v-col justify="center" class="pt-0">
      <v-row class="align-row-1 bcsc-btn" v-if="!hideBCServicesCard">
        <v-col class="fill-width">
          <v-btn
            width="220"
            large
            color="primary"
            @click="login(idpHint.BCSC)"
          >
            Mobile BC Services Card App
          </v-btn>
          <a class="link-w-icon mt-6" @click="clickHyperlink('https://www2.gov.bc.ca/gov/content/governments/government-id/bc-services-card/log-in-with-card','Info: About the BC Services Card')"
            target="_blank" rel="noopener noreferrer" >
            <v-icon small class="mr-2">mdi-open-in-new</v-icon>
            <span>About the mobile BC Services Card app</span>
          </a>
        </v-col>
        <v-col class="align-row-2 fill-width" v-if="!($vuetify.breakpoint.xs)">
          <v-img
            v-if="!($vuetify.breakpoint.xs)"
            class="login-logo"
            :src="require('@/assets/img/bcsc_logo.jpg')"
            max-width="132"
            contain
          ></v-img>
        </v-col>
      </v-row>
      <v-row class="align-row-1 bcsc-btn">
        <v-col class="fill-width">
          <v-btn
          width="220"
          large
          color="primary"
          @click="login(idpHint.BCEID)"
        >
        Basic BCeID Username
        </v-btn>
        <a class="link-w-icon mt-6"
          target="_blank" rel="noopener noreferrer" @click="clickHyperlink('https://www.bceid.ca/','Info: About the BCeID')">
          <v-icon small class="mr-2">mdi-open-in-new</v-icon>
          <span>About the BCeID</span>
        </a>
        </v-col>
        <v-col class="align-row-2 fill-width" v-if="!($vuetify.breakpoint.xs)">
        <v-img
            v-if="!($vuetify.breakpoint.xs)"
            class="login-logo"
            :src="require('@/assets/img/bceid_logo.jpg')"
            max-width="132"
            contain
          ></v-img>
        </v-col>
      </v-row>
      <v-row class="text-center bcsc-btn">
        <v-col class="create-bceid"> <h3>I do not have a BC Services Card or BCeID</h3></v-col>
      </v-row>
      <v-row class="align-row-1 bcsc-btn">
        <v-col class="fill-width">
          <v-btn
          min-width="150"
          large
          color="primary"
          @click="createBCEID(BCEIDRegistrationURL)"
        >
        Create Basic BCeID Username
        </v-btn>
        <a class="link-w-icon mt-3" @click="clickHyperlink('https://www2.gov.bc.ca/gov/content/home/privacy','Info: Privacy Statement')"
          target="_blank" rel="noopener noreferrer">
          <v-icon small class="mr-2">mdi-open-in-new</v-icon>
          <span>Privacy Statement</span>
        </a>
        </v-col>
        <v-col class="align-row-2 fill-width" v-if="!($vuetify.breakpoint.xs)">
        <v-img
            v-if="!($vuetify.breakpoint.xs)"
            class="login-logo"
            :src="require('@/assets/img/bceid_logo.jpg')"
            max-width="132"
            contain
          ></v-img>
        </v-col>
      </v-row>
    </v-col>
  </v-card-text>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import { AuthModule } from '@/store/modules'
import ConfigHelper from '@/utils/config-helper'
import { IdpHint } from '@/utils/constants'
import StepperMixin from '@/mixins/StepperMixin.vue'
import { User } from '@/models/user'

@Component({
  computed: {
    ...mapState('auth', [
      'currentUserProfile'
    ])
  },
  methods: {
    ...mapActions('office', [
      'callSnowplowClick'
    ])
  }
})

export default class LoginToConfirm extends Mixins(StepperMixin) {
  private idpHint = IdpHint

  private currStep = ''

  private readonly currentUserProfile!: User

  private readonly callSnowplowClick!: (mySP: any) => any

  @Prop({ default: false }) isStepperView: boolean

  async mounted () {
    switch (this.$store.state.spLastStep) {
      case 1:
        this.currStep = 'Location Selection'
        break
      case 2:
        this.currStep = 'Select Service'
        break
      case 3:
        this.currStep = 'Select Date'
        break
      case 4:
        this.currStep = 'Login to Confirm Appointmente'
        break
      default:
        break
    }
  }

  private get description () {
    return (this.isStepperView)
      ? 'To complete your appointment booking, please login using one of the following'
      : 'Please login using one of the following'
  }

  private callsp () {
    (window as any).snowplow('trackPageView')
  }

  private login (idpHint) {
    let thelabel = ''
    if (idpHint === 'bcsc') {
      thelabel = 'Login: BC Services Card'
    } else {
      thelabel = 'Login: BCeID'
    }
    let myurl = 'https://appointments.servicebc.gov.bc.ca/signin/' + idpHint
    const mySP = { label: thelabel, step: this.currStep, loggedIn: false, apptID: null, clientID: this.currentUserProfile?.user_id, loc: null, serv: null, url: myurl }
    this.callSnowplowClick(mySP)
    this.$router.push(`/signin/${idpHint}`)
    this.callsp()
  }

  private createBCEID (url) {
    const mySP = { label: 'Create: BCeID', step: this.currStep, loggedIn: false, apptID: null, clientID: this.currentUserProfile?.user_id, loc: null, serv: null, url: url }
    this.callSnowplowClick(mySP)
    window.location.href = url
    this.callsp()
  }

  private clickHyperlink (url, thelabel) {
    const mySP = { label: thelabel, step: this.currStep, loggedIn: false, apptID: null, clientID: this.currentUserProfile?.user_id, loc: null, serv: null, url: url }
    this.callSnowplowClick(mySP)
    window.open(url, '_blank')
    this.callsp()
  }

  private get hideBCServicesCard (): boolean {
    return ConfigHelper.getValue('hideBCServicesCard')
  }

  private get BCEIDRegistrationURL (): string {
    return ConfigHelper.getValue('BCEIDRegistrationUrl')
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
.link-w-icon {
  text-decoration: none;
  display: block;
  span {
    text-decoration: underline;
  }
}
.login-selection-mobile {
  .bcsc-btn {
    padding-top: 24px;
    border-top: thin solid $gray3;
    margin-top: 16px;
  }
}
.create-bceid {
  color: rgba(0,0,0,.87);
}
.align-row-1{
  text-align: center!important;
}
.align-row-2{
  text-align: center!important;
  display: table;
}
.login-logo{
  display: inline-flex;
}
.fill-width{
  min-width: 100%;
}
@media (min-width: 400px) {
  .align-row-1{
  text-align: right!important;
  }
  .align-row-2{
    text-align: left!important;
    margin-left: 0;
    margin-right: 0;
  }
  .fill-width{
    min-width: unset;
  }
}
</style>
