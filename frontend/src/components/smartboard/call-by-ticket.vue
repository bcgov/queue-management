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
      <div v-bind:class="videoStyle.cssStyle">
        <Video :office_number="smartboardData.office_number" />
      </div>
      <div class="board-25-table">
        <div class="board-content-div">
          <b-table
            :items="items"
            :fields="fields"
            :small="longlist"
            thead-tr-class="testclass"
            v-bind:thead-class="headclass"
            v-bind:tbody-class="bodyclass"
          >
            <template #cell(ticket_number)="data">
              <div
                v-if="highlighted.includes(data.value)"
                class="flashing-ticket"
              >
                {{ data.value }}
              </div>
              <div v-else>
                {{ data.value }}
                {{ (data.item._rowVariant = '') }}
              </div>
            </template>
            <template #cell(overflow)="data">
              {{
                showOverflow === false
                  ? (data.item._tdClass = 'd-none')
                  : (data.item._tdClass = '')
              }}
              {{
                showOverflow === false
                  ? (data.item._thClass = 'd-none')
                  : (data.item._thClass = '')
              }}
              <div
                v-if="highlighted.includes(data.value)"
                class="flashing-ticket"
              >
                {{ data.value }}
              </div>
              <div v-else>
                {{ data.value }}
                {{ (data.item._rowVariant = '') }}
              </div>
            </template>
          </b-table>
          <div v-if="networkStatus.networkDown" class="loading small">
          </div>
      </div>
    </div>
    <div v-if="!networkStatus.networkDown" class="bottom-flex-div">
      <div class="flex-title">Currently waiting: {{ waiting }}</div>
    </div>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Component, Prop, Vue } from 'vue-property-decorator'

import Axios from '@/utils/axios'
import Video from './video.vue'
import config from '../../../config'

@Component({
  components: {
    Video
  }
})
export default class CallByTicket extends Vue {
  @Prop({ default: '' })
  private smartboardData!: any

  @Prop({ default: '' })
  private networkStatus!: string

  @Prop({ default: '' })
  private cssStyle!: string

  private tz: any = Intl.DateTimeFormat().resolvedOptions().timeZone

  private options: any = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: this.tz
  }

  private highlighted: any = []
  private fields: any = [
    { key: 'ticket_number', label: 'Now Calling', tdClass: 'text-center' },
    { key: 'overflow', label: '', tdClass: 'd-none', thClass: 'd-none' }
  ]

  private citizens: any = ''
  private intervals: any = {}
  private overflow: any = []
  private showOverflow: boolean = false
  private overflowStyle: string = 'd-none'
  private videoStyle: string = ''

  get items () {
    if (this.showOverflow === true) {
      const base: any = this.invited
      this.overflow.forEach((c, i) => {
        base[i].overflow = c.ticket_number
      })
      return base
    } else {
      return this.invited
    }
  }

  get longlist () {
    if (this.invited.length > 6) {
      return true
    }
    return false
  }

  get headclass () {
    // TODO change  longList longlist
    // check impact
    if (this.longlist) {
      return 'sm-boardtable-head'
    }
    return 'lg-boardtable-head'
  }

  get bodyclass () {
    if (this.longlist) {
      return 'sm-boardtable-body pr-3'
    }
    return 'lg-boardtable-body pr-3'
  }

  get url () {
    return `/smartboard/?office_number=${this.smartboardData.office_number}`
  }

  get invited () {
    if (this.citizens && this.citizens.length > 0) {
      const citizens = this.citizens.filter(c => c.active_period.ps.ps_name === 'Invited')
      let invited: any = null
      if (citizens.length > 8) {
        this.overflow = citizens.slice(8, (citizens.length - 1))
        this.showOverflow = true
        invited = citizens.slice(0, 8)
      } else {
        this.overflow = []
        this.showOverflow = false
        invited = citizens
      }
      if (invited.length != 0) {
        const tickets: any = []
        invited.forEach(item => tickets.push({ ticket_number: item.ticket_number }))
        return tickets
      }
    }
    return [{ ticket_number: '' }]
  }

  get waiting () {
    if (this.citizens && this.citizens.length > 0) {
      return this.citizens.filter(c => c.active_period.ps.ps_name === 'Waiting').length
    }
    return 0
  }

  get date () {
    const d = new Date()
    return d.toLocaleDateString('en-CA', this.options)
  }

  initializeBoard () {
    Axios.get(this.url).then(resp => {
      this.citizens = resp.data.citizens
      this.$root.$emit('boardConnect', { office_id: this.smartboardData && this.smartboardData.office_number })
    })
  }

  updateBoard () {
    Axios.get(this.url).then(resp => {
      this.citizens = resp.data.citizens
    })
  }

  mounted () {
    this.videoStyle = this.cssStyle
    this.$root.$on('addToBoard', () => { this.updateBoard() })
    this.initializeBoard()
  }
}
</script>
