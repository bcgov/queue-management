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
      <iframe :src="url"
              ref="iframe1"
              width="100%"
              :style="frameStyle"
              frameborder="0" />
    </template>
    <template v-else>
      <div class="loader" style="margin-top: 250px" />
    </template>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
  export default {
    name: "Admin",
    created() {
      this.loginIframe()
    },
    computed: {
      ...mapState(['iframeLogedIn', 'adminNavigation', 'user']),
      viewPort() {
        let h = window.innerHeight - 100
        let w = window.innerWidth
        return { h, w }
      },
      frameHeight() {
        return this.viewPort.h - 80
      },
      frameStyle() {
        return {
          height: this.frameHeight + 'px',
        }
      },
      url() {
        //  The default admin edit URL is for GA csr view.
        let return_url = process.env.SOCKET_URL + '/admin/csrga/'

        //  Set a default, if the current URL is blank, depending on role.
        if (this.adminNavigation == '') {
          if (this.user && this.user.role && this.user.role.role_code === 'ANALYTICS') {
            return_url = process.env.SOCKET_URL + '/admin/service/'
          }
          if (this.user && this.user.role && this.user.role.role_code === 'SUPPORT') {
            return_url = process.env.SOCKET_URL + '/admin/csr/'
          }
        }
        else {
          return_url = process.env.SOCKET_URL + '/admin/' + this.adminNavigation + '/'
        }
        return return_url
      }
    },
    methods: {
      ...mapActions(['loginIframe']),
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
    border: 10px solid rgba(0, 0, 0, .3);
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
