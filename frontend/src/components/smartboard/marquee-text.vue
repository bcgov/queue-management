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
      <span v-if="msg_1">{{msg_1}}
        &nbsp;	&nbsp;	&nbsp; &nbsp;
        |
        &nbsp;	&nbsp;	&nbsp; &nbsp;
        </span>
      <span v-if="msg_2">{{msg_2}}
      &nbsp;	&nbsp;	&nbsp;	&nbsp;
      |
      &nbsp;	&nbsp;	&nbsp; &nbsp;
      </span>
      <span v-if="msg_3">{{msg_3}}
      &nbsp;	&nbsp; 	&nbsp;	&nbsp;
      </span>
    </marquee>
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

  @Prop({ default: {} })
  private office!: any

  private officeType: string = ''
  private msg_1: string = ''
  private msg_2: string = ''
  private msg_3: string = ''
  private isMessageEnabled: boolean = false

  created () {
    this.office = this.office.office
    if (this.office.office) {
      if(this.office.office.digital_signage_message == 1) {
        this.isMessageEnabled = true
        if(this.office.office.digital_signage_message_1) {
          this.msg_1 = this.office.office.digital_signage_message_1
        }
        if(this.office.office.digital_signage_message_2) {
          this.msg_2 = this.office.office.digital_signage_message_2
        }
        if(this.office.office.digital_signage_message_3) {
          this.msg_3 = this.office.office.digital_signage_message_3
        }
      }
    }
  }
}
</script>
