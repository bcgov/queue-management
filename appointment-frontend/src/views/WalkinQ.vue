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
        :color="myColor(Q)"
      >
        <v-card-text
          align="center"
          justify="center"
          :color="myColor(Q)"
          >
          {{ Q.ticket_number }} {{ Q.citizen_id}}
        </v-card-text>
      </v-card>
    </v-col>
    <v-col>
      <v-card
        class="pa-md-4 mx-lg-auto"
        :color="myColor(Q)"
      >
        <v-card-text
          align="center"
          justify="center">
         {{ Q.start_time}}  {{ Q.citizen_name}}
        </v-card-text>
      </v-card>
    </v-col>
    <v-col>
      <v-card
        class="pa-md-4 mx-lg-auto"
        :color="myColor(Q)"
      >
        <v-card-text
          v-if="((Q.service_begin_seconds) && !amI(Q.walkin_unique_id))"
          align="center"
          justify="center">
          <span>{{ toHHMMSS(Q.service_begin_seconds) }}</span>
        </v-card-text>
        <v-card-text
          v-else-if="!amI(Q.walkin_unique_id)"
          align="center"
          justify="center">
          <span v-if="isBooked(Q.citizen_comments) || Q.cs.cs_state_name == 'Appointment booked'">
            <!-- booked not served -->
            Booked Appointment {{Q.cs.cs_state_name}} {{Q.citizen_comments}}
            </span>
         <span v-else-if="(!(isBooked(Q.citizen_comments)) && !(Q.cs.cs_state_name == 'Appointment booked'))">
            <!-- walk not served -->
            Not Served {{Q.cs.cs_state_name}} {{Q.citizen_comments}}
          </span>
          <span v-else>
            <!-- walk not served -->
            ariyathilla {{Q.cs.cs_state_name}} {{Q.citizen_comments}}
          </span>
        </v-card-text>
        <v-card-text
           v-else-if="amI(Q.walkin_unique_id)"
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

  private myColor (Q: any) {
    let color = null
    if (Q.walkin_unique_id) {
      color = this.amI(Q.walkin_unique_id)
    }
    if (!color) {
      if ((this.isBooked(Q.citizen_comments)) || (Q.cs.cs_state_name === 'Appointment booked')) {
        // grey
        color = '#A9A9A9'
      } else if (!(this.isBooked(Q.citizen_comments)) && (Q.cs.cs_state_name === 'Active')) {
        // green
        color = '#32CD32'
      }
    }
    return color
  }

  private isBooked (comment: string) {
    if (comment) {
      if (comment.includes('|||')) {
        return true
      }
    }
    return false
  }

  private toHHMMSS (secs: any) {
    var secNum = parseInt(secs, 10)
    var hours = Math.floor(secNum / 3600)
    var minutes = Math.floor(secNum / 60) % 60
    var seconds = secNum % 60

    return [hours, minutes, seconds]
      .map(v => v < 10 ? '0' + v : v)
      .filter((v, i) => v !== '00' || i > 0)
      .join(':')
  }

  // private getTotalTime (seReq: any) {
  //   // eslint-disable-next-line no-console
  //   // console.log(service_begin_seconds)
  //   let totalEstimateSec: number = 0
  //   // // eslint-disable-next-line no-console
  //   // console.log('seReq>>', seReq)

  //   for (const element of seReq) {
  //     // eslint-disable-next-line no-console
  //     console.log(element)
  //     if (element.periods) {
  //       if (element.periods[element.periods.length - 1]) {
  //         // eslint-disable-next-line no-console
  //         console.log(element.periods[element.periods.length - 1], '+++++++++++++!11111')
  //         // eslint-disable-next-line no-console
  //         console.log(element.periods[element.periods.length - 1]?.ps.ps_name, '++++!!!!!!!!!!!!!!!+++++++++!11111', (element.periods[element.periods.length - 1]?.ps.ps_name === 'Being Served'))
  //         if (element.periods[element.periods.length - 1]?.ps.ps_name === 'Being Served') {
  //           const now = moment()
  //           const then = moment(element.periods[element.periods.length - 1]?.time_start + '+00:00')
  //           let totalEstimateSec = now.diff(then, 'seconds')
  //           // eslint-disable-next-line no-console
  //           console.log(this.toHHMMSS(totalEstimateSec), '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
  //         }
  //       }
  //     }
  //   }
  //   return this.toHHMMSS(totalEstimateSec)
  // }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/theme.scss";
</style>
