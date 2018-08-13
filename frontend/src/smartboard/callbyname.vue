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
  <div>
    <div class="top-flex-div"> 
      <div class="flex-title-2">{{ date }} {{ time }}</div>
    </div>
    
    <div style="display: flex; height: 75%; width: 100%; justify-content: center">
      
      <div class="board-75-video">
        <div class="board-video-div">
          <Video vidh="504" vidw="896" />
        </div>
      </div>
    </div>
    <div class="board-footer-div">
      <div v-if="officeType==='callbynumber'" style="width: 100%; text-align: center;"> Currently waiting:
        {{waiting}}</div>
      <div style="width: 100%; text-align: center; font-size: 1.2em">{{ message }}</div>
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
  name: 'CallByName',
  
  mounted() {
    this.$root.$on('addToBoard',( data) => { this.updateBoard(data) })
    setInterval( () => { this.now() }, 3000)
    this.initializeBoard()
  },
  
  components: { Video },
  
  data() {
    return {
      options:{weekday:'long',year:'numeric',month:'long',day:'numeric',},
      timeOpts: {hour12: true, hour: 'numeric', minute: '2-digit'},
      citizens: '',
      time: '',
      message: 'Welcome to ServiceBC'
    }
  },
  
  computed: {
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
    waiting() {
      if (this.citizens && this.citizens.length > 0) {
        return this.citizens.filter(c=>c.state === 'Waiting').length
      }
      return 0
    },
    date() {
      let d = new Date()
      return d.toLocaleDateString('en-CA', this.options)
    }
  },
  
  methods: {
    initializeBoard() {
      Axios.get(this.url).then( resp => {
        this.officeType = resp.data.office_type
        this.citizens = resp.data.citizens
        this.$root.$emit('boardConnect', this.office_id)
      })
    },
    updateBoard(ticketId) {
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




