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
  <videoPlayer
    class="video-player-box"
    ref="videoPlayer"
    :options="playerOptions"
    :playsinline="true"
    @statechanged="playerStateChanged($event)"
  ></videoPlayer>
</template>

<script lang="ts">
// /* eslint-disable */
import 'video.js/dist/video-js.css'

import { Component, Prop, Vue } from 'vue-property-decorator'
import Axios from '@/utils/axios'

import { videoPlayer } from 'vue-video-player'

const defaultVideoFile = '/static/videos/sbc.mp4'
const localVideoFile = 'http://localhost/videos/video.mp4'

@Component({
  components: {
    videoPlayer
  }
})
export default class Video extends Vue {
  @Prop({ default: '' })
  private office_number!: any

  private playerOptions: any = {
    autoplay: 'true',
    loop: 'true',
    controls: false,
    muted: true,
    sources: [{
      type: 'video/mp4',
      src: this.videoPath
    }],
    fluid: true
  }

  private playing: boolean = false

  get videoPath () {
    if (this.getParameterByName('localvideo') == '1') {
      return localVideoFile
    } else {
      return defaultVideoFile
    }
  }

  getOfficeVideoUrl () {
    // eslint-disable-next-line eqeqeq
    if (this.getParameterByName('localvideo') == 1) {
      this.playerOptions.sources[0].src = localVideoFile
    } else {
      const url = '/videofiles/' + this.office_number.toString()
      Axios.get(url)
        .then(resp => {
          if (resp.data.code === 501) {
            this.playerOptions.sources[0].src = defaultVideoFile
          } else {
            this.playerOptions.sources[0].src = resp.data.videourl
          }
        })
        .catch(() => {
          this.playerOptions.sources[0].src = defaultVideoFile
        })
    }
  }

  playerStateChanged (playerCurrentState) {
    if (playerCurrentState && playerCurrentState.playing) {
      this.playing = true
    } else if (playerCurrentState && playerCurrentState.error && this.playing) {
      // This probably means that the video has been updated, try to refresh the page
      setTimeout(() => { window.location.reload() }, 5000)
    }
  }

  getParameterByName (name, url = window.location.href): any {
    // eslint-disable-next-line no-useless-escape
    name = name.replace(/[\[\]]/g, '\\$&')
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'); var results = regex.exec(url)
    if (!results) return null
    if (!results[2]) return ''
    return decodeURIComponent(results[2].replace(/\+/g, ' '))
  }

  beforeMount () {
    this.getOfficeVideoUrl()
  }
}
</script>

<style scoped>
.vjs-loading-spinner {
  display: none !important;
}
</style>
