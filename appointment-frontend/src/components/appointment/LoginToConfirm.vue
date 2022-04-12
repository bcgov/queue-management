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
            Login with BC Services Card
          </v-btn>
          <a class="link-w-icon mt-6" @click="clickHyperlink('https://www2.gov.bc.ca/gov/content?id=B2B3A21E797A421A8FD39EEA86E245D6','Info: About the BC Services Card')"
            target="_blank" rel="noopener noreferrer" >
            <v-icon small class="mr-2">mdi-open-in-new</v-icon>
            <span>Learn more about BC Services Card app</span>
          </a>
        </v-col>
        <v-col class="align-row-2 fill-width" v-if="!($vuetify.breakpoint.xs)">
          <v-img
            v-if="!($vuetify.breakpoint.xs)"
            class="login-logo"
            :src="require('@/assets/img/BCServicesCard.png')"
            max-width="132"
            contain
            data-cy="step-4-image-bcsc"
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
          data-cy="step-4-button-bceid"
        >
        Login with Basic BCeID
        </v-btn>
        <a class="link-w-icon mt-6"
          target="_blank" rel="noopener noreferrer" @click="clickHyperlink('https://www.bceid.ca/directories/bluepages/details.aspx?serviceID=6971','Info: About the BCeID')">
          <v-icon small class="mr-2">mdi-open-in-new</v-icon>
          <span>Learn how to register for a Basic BCeID account</span>
        </a>
        </v-col>
        <v-col class="align-row-2 fill-width" v-if="!($vuetify.breakpoint.xs)">
        <v-img
            v-if="!($vuetify.breakpoint.xs)"
            class="login-logo"
            :src="require('@/assets/img/bceid_logo.jpg')"
            max-width="132"
            contain
            data-cy="step-4-image-bceid-login"
          ></v-img>
        </v-col>
      </v-row>
      <v-row class="text-center bcsc-btn">
        <v-col class="create-bceid"> <h3>Need a BC Services Card or a Basic BCeID account?</h3></v-col>
      </v-row>
      <v-row class="align-row-1 bcsc-btn" v-if="!hideBCServicesCard">
        <v-col class="fill-width">
          <v-btn
            width="220"
            large
            color="primary"
            @click="createBCServicesCard(BCServicesCardURL)"
          >
            Get a BC Services Card
          </v-btn>
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
import { Component, Mixins, Prop } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
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

  private createBCServicesCard (url) {
    const mySP = { label: 'Create: BCServicesCard', step: this.currStep, loggedIn: false, apptID: null, clientID: this.currentUserProfile?.user_id, loc: null, serv: null, url: url }
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

  private get BCServicesCardURL (): string {
    return ConfigHelper.getValue('BCServicesCardUrl')
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
@media (min-width: 500px) {
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
.align-new-row{
  text-align: center!important;
}

</style>
