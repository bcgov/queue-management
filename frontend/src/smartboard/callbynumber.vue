/*Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.*/

<template>
<div style="width: 100%; height: 100%;">
  <div class="top-flex-div"> 
    <div class="flex-title">Welcome to ServiceBC</div>
  </div>
  <div style="display: flex; height: 75%; width: 100%;">
    <div class="board-75-video">
      <div class="board-video-div">
        <Video vidh="504" vidw="896"></Video>
      </div>
    </div>
    <div class="board-25-table">
      <div class="board-content-div">
        <b-table :items="items"
                 :fields="fields"
                 :small="longlist"
                 thead-tr-class="testclass"
                 v-bind:thead-class="headclass"
                 v-bind:tbody-class="bodyclass"
                 >
          <template slot="ticket_number" slot-scope="data">
            <div v-if="highlighted.includes(data.value)" class="flashing-ticket">
              {{data.value}}
            </div>
            <div v-else>
              {{data.value}}
              {{data.item._rowVariant=''}}
            </div>
          </template>
          <template slot="overflow" slot-scope="data">
            {{ this.showOverflow === false ? 
              data.item._tdClass = 'd-none': data.item._tdClass = ''}}
              {{ this.showOverflow === false ? 
                data.item._thClass = 'd-none': data.item._thClass = ''}}
            <div v-if="highlighted.includes(data.value)" class="flashing-ticket">
              {{data.value}}
            </div>
            <div v-else>
              {{data.value}}
              {{data.item._rowVariant=''}}
            </div>
          </template>
        </b-table>
      </div>
    </div>
  </div>
  <div class="board-footer-div">
    <div style="width: 5%"></div>
    <div style="display:flex;flex-direction:column;justify-content:flex-end"> 
      <div>{{date}}</div>
      <div style="text-align: start">{{time}}</div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'
import Video from './video'

const Axios = axios.create({
        baseURL: process.env.API_URL,
        withCredentials: true,
        headers: {
          'Accept': 'application/json'
        }
      })

export default {
  name: 'CallByNumber',
  
  mounted() {
    this.$root.$on('addToBoard',( data) => { this.updateBoard(data) })
    setInterval( () => { this.now() }, 3000)
    this.initializeBoard()
  },
  
  components: { Video },
  
  data() {
    return {
      highlighted: [],
      fields: [
        {key: 'ticket_number', label: 'Now Calling', tdClass:'text-center'},
        {key: 'overflow', label:'', tdClass: 'd-none', thClass: 'd-none'}
      ],
      options:{weekday:'long',year:'numeric',month:'long',day:'numeric',},
      timeOpts: {hour12: true, hour: 'numeric', minute: '2-digit'},
      citizens: '',
      time: '',
      intervals: {},
      overflow: [],
      showOverflow: false,
      overflowStyle: 'd-none'
    }
  },
  
  computed: {
    items() {
      if (this.showOverflow === true) {
        let base = this.invited
        this.overflow.forEach( (c,i) => {
          base[i].overflow = c.ticket_number
        })
        return base
      } else {
        return this.invited
      }
    },
    longlist() {
      if (this.invited.length > 6) {
        return true
      }
      return false
    },
    headclass() {
      if (this.longList) {
        return 'sm-boardtable-head'
      }
      return 'lg-boardtable-head'
    },
    bodyclass() {
      if (this.longList) {
        return 'sm-boardtable-body pr-3'
      }
      return 'lg-boardtable-body pr-3'
    },
    office_id() {
      let path = window.location.pathname.split('/')
      if (path.length >= 3) {
        return path[2]
      } else {
        return 'notfound'
      }
    },
    url() {
      return `/smartboard/?office_id=${this.office_id}`
    },
    invited() {
      if (this.citizens && this.citizens.length > 0) {
        let citizens = this.citizens.filter(c=>c.state === 'Invited')
        if (citizens.length > 8) {
          this.overflow = citizens.slice(8, (citizens.length-1))
          this.showOverflow = true
          return citizens.slice(0,8)
        } else {
          this.overflow = []
          this.showOverflow = false
          return citizens
        }
      }
      return [{ticket_number:''}]
    },
    waiting() {
      if (this.citizens && this.citizens.length > 0) {
        return this.citizens.filter(c=>c.state === 'Waiting').length
      }
      return 0
    },
    date() {
      let d = new Date()
      return d.toLocaleDateString('en-CA', this.options)
    },
  
  },
  
  methods: {
    initializeBoard() {
      Axios.get(this.url).then( resp => {
        this.citizens = resp.data.citizens
        this.$root.$emit('boardConnect', this.office_id)
      })
    },
    updateBoard(ticketId) {
      let ticketFlash = () => {
        this.highlighted.push(ticketId)
        setTimeout( () => { ticketUnFlash() }, 300)
      }
      let ticketUnFlash = () => {
        let i = this.highlighted.indexOf(ticketId)
        this.highlighted.splice(i, 1)
      }
      let clearFlasher = () => {
        clearInterval(interval)
        let i = this.highlighted.indexOf(ticketId)
        if (i >= 0) {
          this.highlighted.splice(i, 1)
        }
      }
      let interval = setInterval( () => { ticketFlash() }, 600 )
      setTimeout( () => { clearFlasher() }, 5000)
      Axios.get(this.url).then( resp => {
        this.citizens = resp.data.citizens
      })
    },
    now() {
      let d = new Date()
      this.time = d.toLocaleTimeString('en-CA', this.timeOpts)
    }
  }
}
</script>



