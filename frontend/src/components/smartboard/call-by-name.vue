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
      <div v-if="((!networkStatus.networkDown) && (office.office.show_currently_waiting_bottom === 1))" class="bottom-flex-div">
        <div class="flex-title">Currently waiting: {{ waiting }}</div>
      </div>
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

// import axios from 'axios'
import Axios from '@/utils/axios'
import Video from './video.vue'
import config from '../../../config'
import MarqueeText from './marquee-text.vue'

@Component({
  components: {
    Video,
    MarqueeText
  }
})
export default class CallByName extends Vue {
  @Prop({ default: '' })
  private smartboardData!: any

  @Prop({ default: '' })
  private networkStatus!: string

  @Prop({ default: [] })
  private office!: any

  @Prop({ default: false })
  private isMessageEnabled!: boolean

  private citizens: any = ''
  private officeType: string = ''
  private maxVideoHeight: string | number = ''
  private office_number: string = this.smartboardData.office_number
  private networkDown: boolean = false

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
    this.$root.$on('addToBoard', (data) => { this.updateBoard(data) })
    this.initializeBoard()
    this.handleResize()
    window.addEventListener('resize', this.handleResize)
  }
}
</script>
