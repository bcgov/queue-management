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
                class="btn btn-primary">Login</b-button>
    </div>

    <div v-show="this.$store.state.isLoggedIn"
         style="display: flex; flex-direction: row; justify-content: space-between; align-items: center;">
      <div>
        <div v-if="!$route.meta.hideCitizenWaiting && citizenSBType"
             class="citizen_waiting">
          Citizens Waiting: {{ queueLength }}
        </div>
      </div>
      <div style="margin-right: 22px;margin-top: 9px;">
        <label id="break-switch">
          <input type="checkbox" v-model="break_toggle">
          <span class="circle1"></span>
          <span class="circle2"></span>
        </label>
        <p class="switch-p">{{user.csr_state_id === csr_states['Break'] ? 'On Break' : 'Active' }}</p>
      </div>
      <div id="select-wrapper" style="padding-right: 20px" v-if="reception">
        <select id="counter-selection-csr" class="custom-select" v-model="counter_selection">
            <option value='receptionist'>Receptionist</option>
            <option v-for="counter in user.office.counters"
                  :value="counter.counter_id"
                  :key="counter.counter_id">
            {{counter.counter_name}}
          </option>
        </select>
      </div>
      <div style="padding-right: 20px">
        <label class="navbar-label navbar-user">User: {{ this.$store.state.user.username }}</label>
        <label class="navbar-label">Office: {{ this.$store.state.user.office.office_name }}</label>
      </div>
      <div style="padding-top: 5px">
        <b-button v-show="this.$store.state.isLoggedIn"
                  @click="logout()"
                  id="logout-button"
                  class="btn btn-primary">Logout</b-button>
      </div>
    </div>
  </b-col>
</template>

<script>
import _ from 'lodash'
import { mapActions, mapGetters, mapMutations, mapState } from 'vuex'

  export default {
    name: 'Login',
    created() {
      this.setupKeycloakCallbacks()
      _.defer(this.initSessionStorage)
    },
    computed: {
      ...mapState(['user',
                   'csr_states'
                  ]),
      ...mapGetters(['quick_trans_status',
                     'reception',
                     'receptionist_status',
                     'citizens_queue',
                    ]),
      counter_selection: {
        get() {
          console.log(this.receptionist_status)
          if (this.receptionist_status === true) {
            return 'receptionist'
          } else {
            return this.user.counter_id
          }
        },
        set(value) {
          if(value === 'receptionist'){
            this.setReceptionistState(true)
          } else {
            this.setCounterStatusState(value)
            this.setReceptionistState(false)
          }
          this.updateCSRCounterTypeState()
        }
      },
      break_toggle: {
        get() {
            var csr_status = this.user.csr_state.csr_state_name

            if(csr_status === 'Break'){
                return false
            } else {
                return true
            }
        },
        set(value) {
            var breakID = this.csr_states['Break']
            var loginID = this.csr_states['Login']
            var id;
            var name;

            if(value){
                id = loginID
                name = 'Login'
            } else {
                id = breakID
                name='Break'
            }

            this.setCSRState(id)
            this.setUserCSRStateName(name)
            this.updateCSRState()
        }
      },
      queueLength() {
        return this.citizens_queue.length
      },
      citizenSBType() {
        if(this.user.office.sb.sb_type !== 'nocallonsmartboard'){
          return true
        }
        else {
          return false
        }
      },
    },
    methods: {
      ...mapActions(['updateCSRCounterTypeState', 'updateCSRCounterTypeState', 'updateCSRState']),
      ...mapMutations(['setQuickTransactionState', 'setReceptionistState', 'setCSRState', 'setUserCSRStateName', 'setCounterStatusState']),
      initSessionStorage() {
        if(sessionStorage.getItem('token')) {
          let tokenExp = sessionStorage.getItem('tokenExp')
          let timeUntilExp = Math.round(tokenExp - new Date().getTime() / 1000)
          if (timeUntilExp > 30) {
            this.$keycloak.init({
                responseMode: 'fragment',
                flow: 'standard',
                refreshToken: sessionStorage.getItem('refreshToken'),
                token: sessionStorage.getItem('token'),
                tokenExp: sessionStorage.getItem('tokenExp')
            })
            .success( () => {

              //Set a timer to auto-refresh the token
              setInterval(() => {
                this.refreshToken(process.env.REFRESH_TOKEN_SECONDS_LEFT);
                }, 60*1000)
              this.setTokenToSessionStorage()
              this.$store.commit('setBearer', sessionStorage.getItem('token'))
            })
            .error( () => {
              this.init()
            })
          } else {
            this.init()
          }
        } else if (!sessionStorage.getItem('token')) {
          this.init()
        }
      },

      init() {
        this.$keycloak.init({
            responseMode: 'fragment',
            flow: 'standard'
          }
        ).success( () => {
          setInterval(() => {
            this.refreshToken(process.env.REFRESH_TOKEN_SECONDS_LEFT);
            }, 60*1000)
        })
      },

      setupKeycloakCallbacks(authenticated) {

        this.$keycloak.onAuthSuccess = () => {
          this.$store.dispatch('logIn', this.$keycloak.token)
          this.setTokenToSessionStorage()
          this.$root.$emit('socketConnect')
        }

        this.$keycloak.onAuthLogout = () => {
          this.$root.$emit('socketDisconnect')
          this.$store.commit('setBearer', null)
          this.$store.commit('logOut')
        }

        this.$keycloak.onAuthRefreshSuccess = () => {
          this.setTokenToSessionStorage()
          this.$store.commit('setBearer', this.$keycloak.token)
        }
      },

      setTokenToSessionStorage() {
        let tokenParsed = this.$keycloak.tokenParsed
        let token = this.$keycloak.token
        let refreshToken = this.$keycloak.refreshToken
        let tokenExpiry = tokenParsed.exp

        if (sessionStorage.getItem('token')) {
          sessionStorage.removeItem("token")
          sessionStorage.removeItem("tokenExp")
          sessionStorage.removeItem("refreshToken")
        }
        sessionStorage.setItem("token", token)
        document.cookie = "oidc-jwt=" + this.$keycloak.token
        sessionStorage.setItem("tokenExp", tokenExpiry)
        sessionStorage.setItem("refreshToken", refreshToken)
      },

      login() {
        this.$keycloak.login({idpHint: 'idir', scope: 'offline_access'})
      },

      logoutTokenExpired() {
        console.log("==> In logoutTokenExpired")
        this.clearStorage()
        // this.init()
        location.href = "/queue"
      },

      logout() {
        this.$keycloak.logout()
        this.clearStorage()
      },

      clearStorage() {
        sessionStorage.removeItem("token")
        sessionStorage.removeItem("tokenExp")
        sessionStorage.removeItem("refreshToken")
      },

      setBreakClickEvent(){
        // Click anywhere on screen to end "Break"
        document.body.addEventListener('click', this.stopBreak);
        document.getElementById('break-switch').style.pointerEvents = 'none'; //Prevent double click event
      },

      stopBreak(){
        const loginStateID = this.csr_states['Login'];
        this.setCSRState(loginStateID)
        this.setUserCSRStateName('Login')
        this.updateCSRState()
      },

      refreshToken(minValidity) {
        let secondsLeft = Math.round(this.$keycloak.tokenParsed.exp + this.$keycloak.timeSkew - new Date().getTime() / 1000)
        console.log('==> Updating token.  Currently valid for ' + secondsLeft + ' seconds')
        this.$keycloak.updateToken(minValidity).success(refreshed => {
          if (refreshed) {
            console.log("Token refreshed and is below")
            console.log(this.$keycloak.tokenParsed)
            console.log("Refresh token is below")
            console.log(this.$keycloak.refreshTokenParsed)
          } else {
            console.log('Token not refreshed')
          }
          let secondsLeft = Math.round(this.$keycloak.tokenParsed.exp + this.$keycloak.timeSkew - new Date().getTime() / 1000)
          console.log('    --> After refresh.  Token now valid for ' + secondsLeft + ' seconds')
        }).error( (error) => {
          console.log('Failed to refresh token')
          console.log(error)
          let secondsLeft = Math.round(this.$keycloak.tokenParsed.exp + this.$keycloak.timeSkew - new Date().getTime() / 1000)
          console.log('    --> After refresh.  Token now valid for ' + secondsLeft + ' seconds')
          if (secondsLeft < 90) {
            this.logoutTokenExpired()
          }
        })
      },
    },
    updated(){
        var csr_status = this.user.csr_state.csr_state_name

        if(csr_status === 'Break'){
            this.setBreakClickEvent();
        } else {
          document.body.removeEventListener('click', this.stopBreak)
          document.getElementById('break-switch').style.pointerEvents = 'all';
        }
    },
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
  font-size: .85rem;
}

#break-switch {
    position: relative;
    display: inline-block;
    width: 66px;
    height: 33px;
    border-radius: 16px;
    margin: 0;
    background: white;
    cursor: pointer;
}

#break-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.circle1 {
    width: 25px;
    height: 25px;
    background-color: #6c757d;
    -webkit-transition: .2s;
    transition: .2s;
    position: absolute;
    border-radius: 50%;
    top: 4px;
    left: 4px;
}

.circle2 {
    width: 25px;
    height: 25px;
    background-color: red;
    -webkit-transition: .2s;
    transition: .2s;
    position: absolute;
    border-radius: 50%;
    top: 4px;
    right: 4px;
}

input:checked + .circle1 {
  background-color: lightgreen;
}

input:checked + .circle1 + .circle2 {
    background-color: #6c757d;
}

.switch-p {
    margin: 0;
    text-align: center;
    color: white;
    font-size: 14px;
}
.citizen_waiting {
  padding-top: 5px;
  padding-right: 40px;
  white-space: pre-wrap;
  font-size: 1.25em;
  color: white;
}
</style>
