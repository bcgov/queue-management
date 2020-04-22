<template>
  <v-card>
    <v-card-title class="justify-center">
      <h3>Login</h3>
    </v-card-title>
    <v-divider class="mx-4"></v-divider>
    <v-card-text>
      <p class="step-desc">To complete your appointment booking, please login using one of the following</p>
      <v-row justify="center">
        <v-col cols="12" sm="5" class="text-center">
          <v-btn
            min-width="150"
            large
            color="primary"
          >
            BCeID
          </v-btn>
          <a class="link-w-icon mt-6" href="https://www.bceid.ca/"
            target="_blank" rel="noopener noreferrer">
            <v-icon small class="mr-2">mdi-open-in-new</v-icon>
            <span>About the BCeID</span>
          </a>
          <a class="link-w-icon mt-3" href="https://www.bceid.ca/register/"
            target="_blank" rel="noopener noreferrer">
            <v-icon small class="mr-2">mdi-open-in-new</v-icon>
            <span>Don't have a BCeID? Click Here</span>
          </a>
          <a class="link-w-icon mt-3" href="https://www2.gov.bc.ca/gov/content/home/privacy"
            target="_blank" rel="noopener noreferrer">
            <v-icon small class="mr-2">mdi-open-in-new</v-icon>
            <span>Privacy Statement</span>
          </a>
        </v-col>
        <v-col cols="12" sm="5" class="text-center">
          <v-btn
            min-width="150"
            large
            color="primary"
          >
            BC Service Card
          </v-btn>
          <a class="link-w-icon mt-6" href="https://www2.gov.bc.ca/gov/content/governments/government-id/bc-services-card"
            target="_blank" rel="noopener noreferrer">
            <v-icon small class="mr-2">mdi-open-in-new</v-icon>
            <span>About the BC Service Card</span>
          </a>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class LoginToConfirm extends Vue {
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
</style>
