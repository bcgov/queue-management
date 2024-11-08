<!--
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
  -->

<template>
  <div>
    <template v-if="iframeLogedIn">
      <iframe :src="url" ref="iframe1" width="100%" :style="frameStyle" title="Admin" />
    </template>
    <template v-else>
      <div class="loader" style="margin-top: 250px" />
    </template>
  </div>
</template>

<script lang="ts">
import { Action, Getter, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'
import config from './../../config'

@Component({})
export default class Admin extends Vue {
  @Getter('admin_navigation_nonblank') private admin_navigation_nonblank!: false;
  @State('iframeLogedIn') private iframeLogedIn!: false;
  @State('adminNavigation') private adminNavigation!: false;
  @State('user') private user!: false;
  @Action('loginIframe') private loginIframe: any;

  get viewPort () {
    const h = window.innerHeight - 100
    const w = window.innerWidth
    return { h, w }
  }

  get frameHeight () {
    return this.viewPort.h - 80
  }

  get frameStyle () {
    return {
      height: this.frameHeight + 'px'
    }
  }

  get url () {
    //  The default admin edit URL is for GA csr view.
    console.log("This is the iframe Value whrn url(): " + this.iframeLogedIn)
    console.log('This is the number navigation used: ' + this.admin_navigation_nonblank)
    return config.SOCKET_URL + '/admin/' + this.admin_navigation_nonblank + '/'
  }

  created () {
    this.loginIframe()
    console.log("This is the iframe Value: " + this.iframeLogedIn)
  }
}

</script>

<style scoped>
.loader {
  position: relative;
  text-align: center;
  margin: 15px auto 35px auto;
  z-index: 9999;
  display: block;
  width: 80px;
  height: 80px;
  border: 10px solid rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  border-top-color: #000;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}
@keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}

@-webkit-keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}
</style>
