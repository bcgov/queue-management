<template>
<v-container>
  <v-alert
      id="nav-alert"
      icon="mdi-alert"
      elevation=8
      v-if="!userBrowser.is_allowed"
    >
    <div class="alert-title">Browser Upgrade Recommended</div>
    You are using an unsupported browser, and may have a degraded experience. To increase performance and access all features please use a modern browser.
  </v-alert>
  <v-container fill-height fluid>
  <v-row align="center"
      justify="center">
      <p>How many people are ahead of me?</p>
  </v-row>
  <v-row align="center"
      justify="center">
      <p><b>Please note:</b> booked appointments take priority and will move to the top of queue </p>
  </v-row>
  <v-row>
    <v-col> </v-col>
    <v-col align="center"
      justify="center">Est. time</v-col>
    <v-col align="center"
      justify="center">Tot. time</v-col>
  </v-row>
  <v-row v-for="Q in theWalkinQ"
        :key="Q.citizen_id">
    <v-col>
      <v-card
        class="pa-md-4 mx-lg-auto"
        :color="amI(Q.walkin_unique_id)"
      >
        <v-card-text
          align="center"
          justify="center"
          :color="amI(Q.walkin_unique_id)"
          >
          {{ Q.ticket_number }}
        </v-card-text>
      </v-card>
    </v-col>
    <v-col>
      <v-card
        class="pa-md-4 mx-lg-auto"
        :color="amI(Q.walkin_unique_id)"
      >
        <v-card-text
          align="center"
          justify="center">
         {{ Q.start_time}}
        </v-card-text>
      </v-card>
    </v-col>
    <v-col>
      <v-card
        class="pa-md-4 mx-lg-auto"
        :color="amI(Q.walkin_unique_id)"
      >
        <v-card-text
          v-if="!amI(Q.walkin_unique_id)"
          align="center"
          justify="center">
          <span v-if="isBooked(Q.citizen_comments)">
            Booked Appointment </span>
          <span v-else>
            {{ Q.start_time}}
          </span>
        </v-card-text>
        <v-card-text
          v-else
          align="center"
          justify="center">
          <v-btn
              icon
              color="red lighten-2"
          >
            <v-icon
                large
                color="blue darken-2"
              >
            mdi-account
            </v-icon>
            Me
          </v-btn>
         </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import CommonUtils from '@/utils/common-util'
import { WalkinModule } from '@/store/modules'
import { getModule } from 'vuex-module-decorators'
import { mapActions } from 'vuex'

@Component({
  methods: {
    ...mapActions('walkin', [
      'getAllWalkin'
    ])
  }
})

export default class WalkinQ extends Vue {
  @Prop({ default: '' }) uniqueId!: string

  private readonly getAllWalkin!: (uniqueId: string) => Promise<any>
  private WalkinModule = getModule(WalkinModule, this.$store)

  private theWalkinQ: any = {}
  private userBrowser = {
    is_allowed: true,
    current_browser: '',
    current_version: '',
    allowed_browsers: ''
  }

  mounted () {
    this.userBrowser = CommonUtils.isAllowedBrowsers()
  }

  private async created () {
    // eslint-disable-next-line no-console
    console.log(this.uniqueId, '++++++++++++++i creadtedddddddd+++++222')
    const resp = await this.getAllWalkin(this.uniqueId)
    // eslint-disable-next-line no-console
    console.log(resp, '++++++++++++', resp?.status)
    if (resp?.status === 200) {
      this.theWalkinQ = resp?.data?.citizen
      // eslint-disable-next-line no-console
      console.log(resp)
    }
  }

  private amI (ID: string) {
    if (ID) {
      if (ID === this.uniqueId) {
        return 'secondary'
      }
    }
    return null
  }

  private isBooked (comment: string) {
    if (comment) {
      if (comment.includes('|||')) {
        return true
      }
    }
    return false
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
