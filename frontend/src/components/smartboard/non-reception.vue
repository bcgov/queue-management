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
  <div style="width: 100%; height: 100%">
    <div class="board-nameticket-video">
      <Video :office_number="smartboardData.office_number" />
      <MarqueeText
        v-if="isMessageEnabled.isMessageEnabled"
        :smartboardData="{ office_number }"
        :networkStatus="{ networkDown }"
        :office="{office}"
      />
    </div>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Component, Prop, Vue } from 'vue-property-decorator'
import Video from './video.vue'
import MarqueeText from './marquee-text.vue'

@Component({
  components: {
    Video,
    MarqueeText
  }
})
export default class NonReception extends Vue {
  @Prop({ default: {} })
  private smartboardData!: any

  @Prop({ default: {} })
  private networkStatus!: any

  @Prop({ default: {} })
  private office!: any

  @Prop({ default: {} })
  private isMessageEnabled!: any

  
  private office_number: string = this.smartboardData.office_number
  private networkDown: boolean = false

  created () {
    this.office = this.office.office
    this.isMessageEnabled = this.isMessageEnabled.isMessageEnabled
    this.networkStatus = this.networkStatus.networkStatus
  }
}
</script>
