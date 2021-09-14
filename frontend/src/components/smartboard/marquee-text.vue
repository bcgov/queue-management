<!-- /*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/
-->
<template>
  <div class="marquee" v-if="isMessageEnabled">
    <span>
      <span v-if="msg_1">{{msg_1}}</span>
      <span v-if="msg_2">{{msg_2}}</span>
      <span v-if="msg_3">{{msg_3}}</span>
    </span>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Component, Prop, Vue } from 'vue-property-decorator'

// import axios from 'axios'
import Axios from '@/utils/axios'
import Video from './video.vue'

@Component({
  components: {
    Video
  }
})
export default class MarqueeText extends Vue {
  @Prop({ default: '' })
  private smartboardData!: any

  @Prop({ default: '' }) office_number!: string

  @Prop({ default: '' })
  private networkStatus!: string

  @Prop({ default: {} })
  private office!: any

  private citizens: any = ''
  private officeType: string = ''
  private maxVideoHeight: string | number = ''
  private msg:string = 'This is a sample scrolling text that has scrolls texts to left.'

  private msg_1: string = ''
  private msg_2: string = ''
  private msg_3: string = ''
  private sboffice: any
  private isMessageEnabled: boolean = false

  get url () {
    return `/smartboard/?office_number=${this.smartboardData.office_number}`
  }

  get waiting () {
    if (this.citizens && this.citizens.length > 0) {
      return this.citizens.filter(c => c.active_period.ps.ps_name === 'Waiting').length
    }
    return 0
  }

  initializeBoard () {
    Axios.get(this.url).then(resp => {
      this.officeType = resp.data.office_type
      this.citizens = resp.data.citizens
      // TODO check can't see  this.office_id Declared . so commented
      // this.$root.$emit('boardConnect', this.office_id)
      // so change to below line to get office id
      this.$root.$emit('boardConnect', { office_id: this.smartboardData && this.smartboardData.office_number })
    })
  }

  updateBoard (ticketId) {
    Axios.get(this.url).then(resp => {
      this.citizens = resp.data.citizens
    })
  }

  // TODO check event param
  // event
  handleResize () {
    this.maxVideoHeight = document.documentElement.clientHeight * 0.8
  }

  mounted () {
    this.$root.$on('onDigitalSignageMsgUpdate', (data) => { this.updateBoard(data) })
    this.initializeBoard()
    this.handleResize()
    window.addEventListener('resize', this.handleResize)
  }

  created () {
    this.sboffice = this.office.office
    if (this.sboffice.office) {
      if(this.sboffice.office.digital_signage_message_1) {
        this.isMessageEnabled = true
        this.msg_1 = this.sboffice.office.digital_signage_message_1
      }
      if(this.sboffice.office.digital_signage_message_2) {
        this.isMessageEnabled = true
        this.msg_2 = this.sboffice.office.digital_signage_message_2
      }
      if(this.sboffice.office.digital_signage_message_3) {
        this.isMessageEnabled = true
        this.msg_3 = this.sboffice.office.digital_signage_message_3
      }
    }
  }
}
</script>
