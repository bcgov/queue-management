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
  <div style="display: flex; height: 75%; width: 100%; justify-content: center">
    <div class="board-85-video">
      <div class="board-video-div">
        <Video />
      </div>
      <div class="bottom-flex-div">
        <div class="flex-title"> Currently waiting: {{waiting}}</div>
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
  name: 'CallByName',
  props: ['id'],
  mounted() {
    this.$root.$on('addToBoard',( data) => { this.updateBoard(data) })
    this.initializeBoard()
    this.handleResize()
    window.addEventListener('resize', this.handleResize)
  },

  components: { Video },

  data() {
    return {
      citizens: '',
      officeType: '',
      maxVideoHeight: ''
    }
  },

  computed: {
    office_id() {
      if (this.id) {
        return this.id
      }
      return 'notfound'
    },
    url() {
      return `/smartboard/?office_number=${this.office_id}`
    },
    waiting() {
      if (this.citizens && this.citizens.length > 0) {
        return this.citizens.filter(c => c.active_period.ps.ps_name === 'Waiting').length
      }
      return 0
    }
  },

  methods: {
    initializeBoard() {
      Axios.get(this.url).then( resp => {
      console.log(resp.data)
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
    handleResize(event) {
      this.maxVideoHeight = document.documentElement.clientHeight * 0.8
    }
  }
}
</script>




