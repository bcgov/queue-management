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
  <div style="display: flex; height: 75%; width: 100%; justify-content: center">
    <div class="board-noticket-video">
      <div class="board-video-div">
        <Video :office_number="smartboardData.office_number" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
// /* eslint-disable */
import { Component, Prop, Vue } from 'vue-property-decorator'
import Video from './video.vue'

@Component({
  components: {
    Video
  }
})
export default class NonReception extends Vue {
  @Prop({ default: '' })
  private smartboardData!: any
}
</script>
