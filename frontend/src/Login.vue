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
  <b-col id="login-form">
    <div v-show="!this.$store.state.isLoggedIn">
      <b-button @click="login()"
                id="login-button"
                style="padding-top: 10px"
                class="btn btn-link">Login</b-button>
    </div>

    <div v-show="this.$store.state.isLoggedIn"
         style="display: flex; flex-direction: row; justify-content: space-between">
      <div style="padding-right: 20px">
        <b-form-checkbox :checked="quick_trans_status"
                         class="navbar-label">Quick Txn</b-form-checkbox>
      </div>
      <div style="padding-right: 20px">
        <label class="navbar-label">User: {{ this.$store.state.user.username }}</label>
        <label class="navbar-label">Office: {{ this.$store.state.user.office.office_name }}</label>
      </div>
      <div style="padding-top: 5px">
        <b-button v-show="this.$store.state.isLoggedIn"
                  @click="logout()"
                  id="logout-button"
                  class="btn btn-secondary">Logout</b-button>
      </div>
    </div>
  </b-col>
</template>

<script>
import _ from 'lodash'
import { mapGetters } from 'vuex'

  export default {
    name: 'Login',
    created() {
      this.setupKeycloakCallbacks()
      _.defer(this.initLocalStorage)
    },
    computed: {
      ...mapGetters(['quick_trans_status'])
    },
    methods: {
      initLocalStorage() {
        if(localStorage.token) {
          console.log('tokens found in localStorage')
          let tokenExp = localStorage.tokenExp
          let timeUntilExp = Math.round(tokenExp - new Date().getTime() / 1000)
          this.$store.commit('setBearer', localStorage.token)
          if (timeUntilExp > 30) {
            this.$keycloak.init(
              {
                responseMode: 'fragment',
                flow: 'standard',
                refreshToken: localStorage.refreshToken,
                token: localStorage.token,
                tokenExp: localStorage.tokenExp
              }
            )
            .success( () => {
              console.log('Init Success w. stored tokens')
              this.refreshToken(9999)
              this.setTokenToLocalStorage()
            })
            .error( () => {
              console.log('Init Error.  Retrying without stored tokens.')
              this.init()
            })
          } else {
            console.log('Init Error.  Retrying without stored tokens.')
            this.init()
          }
        } else if (!localStorage.token) {
          console.log('Could not locate any stored tokens')
          this.init()
        }
      },

      init() {
        this.$keycloak.init(
          {
            responseMode: 'fragment',
            flow: 'standard'
          }
        )
      },

      setupKeycloakCallbacks(authenticated) {
        this.$keycloak.onReady = (authenticated) => {
          if (authenticated) {
            console.log('keycloak: "onReady" and authenticated')
            this.$store.dispatch('logIn', this.$keycloak.token)
          } else if (!authenticated) {
            console.log('keycloak: "onReady" but not authenticated')
          }
        }

        this.$keycloak.onAuthSuccess = () => {
          console.log('keycloak: "onAuthSuccess"')
          this.$store.dispatch('logIn', this.$keycloak.token)
          this.setTokenToLocalStorage()
          this.$root.$emit('socketConnect')
        }

        this.$keycloak.onAuthLogout = () => {
          console.log('keycloak: "onAuthLogout"')
          this.$root.$emit('socketDisconnect')
          this.$store.commit('logOut')
        }

        this.$keycloak.onAuthRefreshSuccess = () => {
          console.log('keycloak: "onAuthRefreshSuccess"')
          this.setTokenToLocalStorage()
        }
      },

      setTokenToLocalStorage() {
        let tokenParsed = this.$keycloak.tokenParsed
        let token = this.$keycloak.token
        let refreshToken = this.$keycloak.refreshToken
        let tokenExpiry = tokenParsed.exp

        if (localStorage.token) {
          localStorage.removeItem("token")
          localStorage.removeItem("tokenExp")
          localStorage.removeItem("refreshToken")
        }
        localStorage.setItem("token", token)
        document.cookie = "oidc-jwt=" + this.$keycloak.token
        localStorage.setItem("tokenExp", tokenExpiry)
        localStorage.setItem("refreshToken", refreshToken)

        console.log('localStorage: acquired new tokens')
      },

      login() {
        this.$keycloak.login()
      },

      logout() {
        this.$keycloak.logout()
        localStorage.removeItem("token")
        localStorage.removeItem("tokenExp")
        localStorage.removeItem("refreshToken")
      },

      refreshToken(minValidity) {
        this.$keycloak.updateToken(minValidity).success(refreshed => {
          if (refreshed) {
            console.log(this.$keycloak.tokenParsed)
          } else {
            console.log('Token not refreshed, valid for ' + Math.round(this.$keycloak.tokenParsed.exp + this.$keycloak.timeSkew - new Date().getTime() / 1000) + ' seconds')
          }
        }).error( () => {
          output('Failed to refresh token')
        })
      }
    }
  }
</script>

<style>
.custom-control-label::after, .custom-control-label::before {
  top: 3px;
}

.navbar-label {
  color: white;
  margin-bottom: 0px;
  float: left;
  clear: both;
}

.navbar-brand {
  font-size: 1rem;
}
</style>
