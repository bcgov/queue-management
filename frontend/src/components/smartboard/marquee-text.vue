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
  <div class="marquee-container1" v-if="isMessageEnabled">
    <marquee width="100%" direction="left" height="100px" class="marquee-text marquee-ds">
      <span v-if="msg1">{{msg1}} &nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span v-if="msg2"> | &nbsp;&nbsp;&nbsp;&nbsp; {{msg2}} &nbsp;&nbsp;&nbsp;&nbsp;</span>
      <span v-if="msg3"> | &nbsp;&nbsp;&nbsp;&nbsp; {{msg3}} &nbsp;&nbsp;&nbsp;&nbsp;</span>
    </marquee>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Component, Prop, Vue } from 'vue-property-decorator'
import Video from './video.vue'

@Component({
  components: {
    Video
  }
})
export default class MarqueeText extends Vue {
  @Prop({ default: {} })
  private office!: any

  @Prop({ default: '' })
  private smartboardData!: any

  private citizens: any = ''
  private officeType: string = ''
  private msg1: string = ''
  private msg2: string = ''
  private msg3: string = ''
  private sboffice: any
  private isMessageEnabled: boolean = false

  mounted () {
    this.$root.$emit('boardConnect', { office_id: this.smartboardData && this.smartboardData.office_number })
    /* this.$root.$on('onDigitalSignageMsgUpdate', (data) => { this.updateBoard(data) }) */
  }

  created () {
    this.sboffice = this.office.office
    if (this.sboffice.office) {
      if (this.sboffice.office.digital_signage_message === 1) {
        this.isMessageEnabled = true
        if (this.sboffice.office.digital_signage_message_1) {
          this.msg1 = this.sboffice.office.digital_signage_message_1
        }
        if (this.sboffice.office.digital_signage_message_2) {
          this.msg2 = this.sboffice.office.digital_signage_message_2
        }
        if (this.sboffice.office.digital_signage_message_3) {
          this.msg3 = this.sboffice.office.digital_signage_message_3
        }
      }
    }
  }
}
</script>
