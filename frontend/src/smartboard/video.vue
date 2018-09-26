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
  <videoPlayer class="video-player-box"
               ref="videoPlayer"
               :options="playerOptions"
               :playsinline="true"
               @statechanged="playerStateChanged($event)">
  </videoPlayer>
</template>

<script>
  import 'video.js/dist/video-js.css'
  import { videoPlayer } from 'vue-video-player'

  export default {
    name: 'Video',
    components: {
      videoPlayer
    },
    data() {
      return {
        playerOptions: {
          autoplay: 'true',
          loop: 'true',
          controls: false,
          muted: true,
          sources: [{
            type: 'video/mp4',
            src: '/static/videos/sbc.mp4'
          }],
          fluid: true
        },
        playing: false
      }
    },
    methods: {
      playerStateChanged(playerCurrentState) {
        if (playerCurrentState && playerCurrentState.playing) {
          this.playing = true
        } else if (playerCurrentState && playerCurrentState.error && this.playing) {
          //This probably means that the video has been updated, try to refresh the page
          setTimeout(() => { window.location.reload(true);}, 5000);
        }
      }
    }
  }
</script>
