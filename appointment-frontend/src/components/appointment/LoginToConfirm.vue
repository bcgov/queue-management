<template>
  <v-card-text :class="{'login-selection-mobile': $vuetify.breakpoint.xs}">
    <v-row justify="center">
      <v-col cols="12" sm="5" class="text-center">
        <v-btn
          min-width="150"
          large
          color="primary"
          @click="login(idpHint.BCEID)"
        >
          BCeID
        </v-btn>
        <a class="link-w-icon mt-6" href="https://www.bceid.ca/"
          target="_blank" rel="noopener noreferrer">
          <v-icon small class="mr-2">mdi-open-in-new</v-icon>
          <span>About the BCeID</span>
        </a>
        <v-btn :href="BCEIDRegistrationURL"
          min-width="150"
          large class="create-bceid"
          color="primary"
        >
        Create BCeID
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
      <v-col cols="12" sm="5" class="text-center bcsc-btn" v-if="!hideBCServicesCard">
        <v-btn
          min-width="150"
          large
          color="primary"
          @click="login(idpHint.BCSC)"
        >
          BC Services Card
        </v-btn>
        <a class="link-w-icon mt-6" href="https://www2.gov.bc.ca/gov/content/governments/government-id/bc-services-card"
          target="_blank" rel="noopener noreferrer">
          <v-icon small class="mr-2">mdi-open-in-new</v-icon>
          <span>About the BC Services Card</span>
        </a>
      </v-col>
    </v-row>
  </v-card-text>
</template>

<script lang="ts">
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator'
import { AuthModule } from '@/store/modules'
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
      ? `To complete your appointment booking, please login using one of the following`
      : `Please login using one of the following`
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
  margin-top: 15px
}
</style>
