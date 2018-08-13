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

        <div class="board-video-div-2">
          <Video vidh="605" vidw="1075" />
        </div>
    </div>
    <div class="board-footer-div" style="align-items: flex-end">
      <div style="width: 100%; text-align: center; font-size: 1.2em padding-top:30px">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import Video from './video'

export default {
  name: 'NonReception',
  
  mounted() {
    setInterval( () => { this.now() }, 3000)
  },
  
  components: { Video },
  
  data() {
    return {
      options:{weekday:'long',year:'numeric',month:'long',day:'numeric',},
      timeOpts: {hour12: true, hour: 'numeric', minute: '2-digit'}, citzens: '',
      time: '',
      message: 'Welcome to ServiceBC'
    }
  },
  
  computed: {
    date() {
      let d = new Date()
      return d.toLocaleDateString('en-CA', this.options)
    }
  },
  
  methods: {
    now() {
      let d = new Date()
      this.time = d.toLocaleTimeString('en-CA', this.timeOpts)
    }
  }
}
</script>



