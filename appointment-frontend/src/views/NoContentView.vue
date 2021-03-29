<template>
  <v-container class="no-content-view">
    <v-alert
      text
      outlined
      prominent
      color="deep-orange accent-3"
      icon="mdi-alert-circle"
    >
      <div class="title font-weight-bold">{{msgHeading}}</div>
      {{msgBody}}
    </v-alert>
  </v-container>
</template>

<script lang="ts">
// Libraries
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component({
})
export default class NoContentView extends Vue {
  @Prop({ default: '' }) msgType!: string
  private msgHeading: string = ''
  private msgBody: string = ''

  mounted () {
    switch (this.msgType) {
      case 'unauthorized':
        this.msgHeading = 'Unauthorized!'
        this.msgBody = 'Sorry, You are unauthorized to use this Appointment Booking Online Service'
        break
      case 'unavailable':
        this.msgHeading = 'Not Available!'
        this.msgBody = 'Sorry, This application is not available in this browser. Please use any modern browsers like Google Chrome, Safari, Mozilla Firefox etc.'
        break
      case 'not-in-Q':
        this.msgHeading = 'Data not Available!'
        this.msgBody = `Sorry, Your Details are not available in the system. Seems like you are not in the Queue anymore.`
        break
      default:
        this.msgHeading = ''
        this.msgBody = ''
    }
  }
}
</script>
