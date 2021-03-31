<template>
  <v-card-text>
    <v-col justify="center">
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
          <a class="link-w-icon mt-6" href="https://www2.gov.bc.ca/gov/content/governments/government-id/bc-services-card/log-in-with-card"
            target="_blank" rel="noopener noreferrer">
            <v-icon small class="mr-2">mdi-open-in-new</v-icon>
            <span>About the mobile BC Services Card app</span>
          </a>
        </v-col>
        <v-col class="align-row-2 fill-width">
          <v-img
            class="login-logo"
            :src="($vuetify.breakpoint.xs) ? require('@/assets/img/bcsc_logo_sm.jpg') : require('@/assets/img/bcsc_logo.jpg')"
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
        <a class="link-w-icon mt-6" href="https://www.bceid.ca/"
          target="_blank" rel="noopener noreferrer">
          <v-icon small class="mr-2">mdi-open-in-new</v-icon>
          <span>About the BCeID</span>
        </a>
        </v-col>
        <v-col class="align-row-2 fill-width">
        <v-img
            class="login-logo"
            :src="($vuetify.breakpoint.xs) ? require('@/assets/img/bceid_logo_sm.jpg') : require('@/assets/img/bceid_logo.jpg')"
            max-width="132"
            contain
          ></v-img>
        </v-col>
      </v-row>
      <v-row class="text-center bcsc-btn">
        <v-col class="create-bceid">I do not have a BC Services Card or BCeID</v-col>
      </v-row>
      <v-row class="align-row-1 bcsc-btn">
        <v-col class="fill-width">
          <v-btn :href="BCEIDRegistrationURL"
          width="220"
          large
          color="primary"
        >
        Create Basic BCeID Username
        </v-btn>
        <!--a class="link-w-icon mt-3" :href="BCEIDRegistrationURL"
          target="_self" rel="noopener noreferrer">
          <v-icon small class="mr-2">mdi-open-in-new</v-icon>
          <span>Don't have a BCeID? Click Here</span>
        </a-->
        <a class="link-w-icon mt-3" href="https://www2.gov.bc.ca/gov/content/home/privacy"
          target="_blank" rel="noopener noreferrer">
          <v-icon small class="mr-2">mdi-open-in-new</v-icon>
          <span>Privacy Statement</span>
        </a>
        </v-col>
        <v-col class="align-row-2 fill-width">
        <v-img
            class="login-logo"
            :src="($vuetify.breakpoint.xs) ? require('@/assets/img/bceid_logo_sm.jpg') : require('@/assets/img/bceid_logo.jpg')"
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
import ConfigHelper from '@/utils/config-helper'
import { IdpHint } from '@/utils/constants'
import StepperMixin from '@/mixins/StepperMixin.vue'
import { User } from '@/models/user'
import { mapState } from 'vuex'

@Component({
  computed: {
    ...mapState('auth', [
      'currentUserProfile'
    ])
  }
})
export default class LoginToConfirm extends Mixins(StepperMixin) {
  private idpHint = IdpHint
  private readonly currentUserProfile!: User
  @Prop({ default: false }) isStepperView: boolean

  private get description () {
    return (this.isStepperView)
      ? 'To complete your appointment booking, please login using one of the following'
      : 'Please login using one of the following'
  }

  private login (idpHint) {
    this.$router.push(`/signin/${idpHint}`)
    // this.stepNext()
  }

  private get hideBCServicesCard (): boolean {
    return ConfigHelper.getValue('hideBCServicesCard')
  }

  private get BCEIDRegistrationURL (): string {
    // return 'https://www.test.bceid.ca/os/?7521&SkipTo=Basic'
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
