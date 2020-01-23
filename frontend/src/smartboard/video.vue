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

  const defaultVideoFile = '/static/videos/sbc.mp4';

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
      console.log("==> Video.vue: In beforeMount()")
      this.getOfficeVideoUrl()
    },
    data() {
      function getParameterByName(name, url) {
        console.log("==> Video.vue: In getParameterByName()");
        console.log("    --> name:         " + name);
        console.log("    --> url:          " + url);
        url = window.location.href;
        console.log("    --> updated url:  " + url);
        name = name.replace(/[\[\]]/g, '\\$&');
        console.log("    --> updated name: " + name);
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'), results = regex.exec(url);
        console.log("    --> results:");
        console.log(results);
        if (!results) return null;
        if (!results[2]) return '';
        console.log("    --> decodeURIComponent: " + decodeURIComponent(results[2].replace(/\+/g, ' ')));
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
      }

      var videoPath = this.defaultVideoFile;
      var test = getParameterByName("localvideo")
      console.log("==> In video.vue, localvideo = " + test.toString())
      if (getParameterByName("localvideo") == "1") {
        console.log("    --> localvideo was 1")
        videoPath = "http://localhost/videos/video.mp4";
      }

      console.log("    --> videoPath: " + videoPath)

      return {
        playerOptions: {
          autoplay: 'true',
          loop: 'true',
          controls: false,
          muted: true,
          sources: [{
            type: 'video/mp4',
            src: 'http://localhost/videos/video.mp4'
          }],
          fluid: true
        },
        playing: false
      }
    },
    methods: {
      getOfficeVideoUrl() {
        console.log("==> Video.vue: getOfficeVideoUrl()");
        let url = '/videofiles/' + this.office_number.toString();
        console.log("    --> url: " + url);
        Axios.get(url)
          .then( resp => {
            this.playerOptions.sources[0].src = resp.data.videourl;
            console.log("    --> resp.data.videourl: " + resp.data.videourl);
          })
          .catch(() => {
            this.playerOptions.sources[0].src = this.defaultVideoFile;
          })
        console.log("    --> this.playerOptions.sources")
        console.log(this.playerOptions.sources)
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
