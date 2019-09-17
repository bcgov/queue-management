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
  import axios from 'axios'
  import 'video.js/dist/video-js.css'
  import { videoPlayer } from 'vue-video-player'

  const Axios = axios.create({
    baseURL: process.env.API_URL,
    withCredentials: true,
    headers: {
      'Accept': 'application/json'
    }
  })

  export default {
    name: 'Video',
    components: {
      videoPlayer
    },
    props: ['office_number'],
    // mounted() {
    //   this.getOfficeVideoUrl()
    // },
    beforeMount() {
      this.getOfficeVideoUrl()
    },
    data() {
      function getParameterByName(name, url) {
        url = window.location.href;
        name = name.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'), results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
      }

      var videoPath = '/static/videos/sbc.mp4';
      if (getParameterByName("localvideo") == "1") {
        videoPath = "http://localhost/videos/video.mp4";
        console.log("==> Video path is: " + videoPath)
      }

      return {
        playerOptions: {
          autoplay: 'true',
          loop: 'true',
          controls: false,
          muted: true,
          sources: [{
            type: 'video/mp4',
            src: videoPath
          }],
          fluid: true
        },
        playing: false
      }
    },
    methods: {
      getOfficeVideoUrl() {
        let url = '/videofiles/' + this.office_number.toString();
        Axios.get(url).then( resp => {
          this.playerOptions.sources[0].src = resp.data.videourl
        })
      },
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
