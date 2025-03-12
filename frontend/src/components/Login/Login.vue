/*Copyright 2015 Province of British Columbia Licensed under the Apache License,
Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or
agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. See the License for the specific language governing permissions and
limitations under the License.*/

<template>
  <b-col id="login-form">
    <div v-show="!this.$store.state.isLoggedIn">
      <b-button
        @click="login()"
        id="login-button"
        style="padding-top: 10px"
        class="btn btn-primary"
        >Login</b-button
      >
    </div>

    <div
      v-show="this.$store.state.isLoggedIn"
      style="
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
      "
    >
      <div>
        <div
          v-if="!$route.meta.hideCitizenWaiting && citizenSBType"
          class="citizen_waiting"
        >
          Citizens Waiting: {{ queueLength }}
        </div>
      </div>
      <div style="margin-right: 22px; margin-top: 9px">
        <label id="break-switch" for="break_toggle">
          <input type="checkbox" id="break_toggle" v-model="breakToggle" />
          <span class="circle1"></span>
          <span class="circle2"></span>
        </label>
        <p class="switch-p">
          {{
            user.csr_state_id === csr_states["Break"] ? "On Break" : "Active"
          }}
        </p>
      </div>
      <div id="select-wrapper" style="padding-right: 20px" v-if="reception">
        <select
          id="counter-selection-csr"
          class="custom-select"
          v-model="counterSelection"
        >
          <option value="receptionist">Receptionist</option>
          <option
            v-for="counter in user.office.counters"
            :value="counter.counter_id"
            :key="counter.counter_id"
          >
            {{ counter.counter_name }}
          </option>
        </select>
      </div>
      <div style="padding-right: 20px">
        <div v-if="!showOfficeSwitcher" class="navbar-label navbar-user"
          >User: {{ this.$store.state.user.username }}</div
        >
        <div>
          <template v-if="!showOfficeSwitcher">
            <div class="navbar-label">
              <span
                @click="setOfficeSwitcher(!showOfficeSwitcher)"
                class="clickable"
                >Office: {{ this.$store.state.user.office.office_name }}</span
              >
            </div>
          </template>
          <template v-else>
            <vue-bootstrap-typeahead
              v-model="officeQuery"
              :data="this.offices"
              :serializer="x => x.office_name"
              placeholder="Enter an office"
              @hit="changeOffice"
            >
              <template slot="append">
                <b-button variant="danger" @click="cancelOfficeSwitcher"
                  >Cancel</b-button
                >
              </template>
            </vue-bootstrap-typeahead>
          </template>
        </div>
      </div>
      <div style="padding-top: 5px">
        <b-button
          v-show="this.$store.state.isLoggedIn"
          @click="logout()"
          id="logout-button"
          class="btn btn-primary"
          >Logout</b-button
        >
      </div>
    </div>
  </b-col>
</template>

<script lang="ts">
import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'
import { Action, Getter, Mutation, State } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'
import config from '../../../config'
import _ from 'lodash'

@Component({
  components: {
    VueBootstrapTypeahead
  }
})
export default class Login extends Vue {
  @State('user') private user!: any;
  @State('csr_states') private csr_states!: any;
  @State('showOfficeSwitcher') private showOfficeSwitcher!: boolean;
  @State('offices') private offices!: any;

  @Getter('role_code') private role_code!: any;
  @Getter('quick_trans_status') private quick_trans_status!: any;
  @Getter('reception') private reception!: any;
  @Getter('receptionist_status') private receptionist_status!: any;
  @Getter('citizens_queue') private citizens_queue!: any;

  @Action('updateCSRCounterTypeState') public updateCSRCounterTypeState: any;
  @Action('updateCSRState') public updateCSRState: any;
  @Action('updateCSROffice') public updateCSROffice: any;
  @Action('getOffices') public getOffices: any;

  @Mutation('setQuickTransactionState') public setQuickTransactionState: any;
  @Mutation('setReceptionistState') public setReceptionistState: any;
  @Mutation('setCSRState') public setCSRState: any;
  @Mutation('setUserCSRStateName') public setUserCSRStateName: any;
  @Mutation('setCounterStatusState') public setCounterStatusState: any;
  @Mutation('setOfficeSwitcher') public setOfficeSwitcher: any;

  $keycloak: any;
  officeQuery = '';

  get counterSelection () {
    if (this.receptionist_status === true) {
      return 'receptionist'
    } else {
      return this.user.counter_id
    }
  }

  set counterSelection (value) {
    if (value === 'receptionist') {
      this.setReceptionistState(true)
    } else {
      this.setCounterStatusState(value)
      this.setReceptionistState(false)
    }
    this.updateCSRCounterTypeState()
  }

  get breakToggle () {
    const csrStatus = this.user.csr_state.csr_state_name

    if (csrStatus === 'Break') {
      return false
    } else {
      return true
    }
  }

  set breakToggle (value) {
    const breakID = this.csr_states.Break
    const loginID = this.csr_states.Login
    let id
    let name

    if (value) {
      id = loginID
      name = 'Login'
    } else {
      id = breakID
      name = 'Break'
    }

    this.setCSRState(id)
    this.setUserCSRStateName(name)
    this.updateCSRState()
  }

  get queueLength () {
    return this.citizens_queue.length
  }

  get citizenSBType () {
    if (this.user.office.sb.sb_type !== 'nocallonsmartboard') {
      return true
    } else {
      return false
    }
  }

  initSessionStorage () {
    if (sessionStorage.getItem('token')) {
      const tokenExp: any = sessionStorage.getItem('tokenExp')
      const timeUntilExp = Math.round(tokenExp - new Date().getTime() / 1000)
      if (timeUntilExp > 30) {
        this.$keycloak
          .init({
            responseMode: 'fragment',
            flow: 'standard',
            refreshToken: sessionStorage.getItem('refreshToken'),
            token: sessionStorage.getItem('token'),
            tokenExp: sessionStorage.getItem('tokenExp')
          })
          .then(() => {
            // Set a timer to auto-refresh the token
            setInterval(() => {
              this.refreshToken(config.REFRESH_TOKEN_SECONDS_LEFT)
            }, 60 * 1000)
            this.setTokenToSessionStorage()
            this.$store.commit('setBearer', sessionStorage.getItem('token'))
          })
          .catch(() => {
            this.init()
          })
      } else {
        this.init()
      }
    } else if (!sessionStorage.getItem('token')) {
      this.init()
    }
  }

  init () {
    this.$keycloak
      .init({
        responseMode: 'fragment',
        flow: 'standard',
        onLoad: 'check-sso'
      })
      .success(() => {
        setInterval(() => {
          this.refreshToken(config.REFRESH_TOKEN_SECONDS_LEFT)
        }, 60 * 1000)
      })
  }

  setupKeycloakCallbacks () {
    // authenticated
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
  }

  setTokenToSessionStorage () {
    const tokenParsed = this.$keycloak.tokenParsed
    const token = this.$keycloak.token
    const refreshToken = this.$keycloak.refreshToken
    const tokenExpiry = tokenParsed.exp

    if (sessionStorage.getItem('token')) {
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('tokenExp')
      sessionStorage.removeItem('refreshToken')
    }
    sessionStorage.setItem('token', token)
    document.cookie = 'oidc-jwt=' + this.$keycloak.token
    sessionStorage.setItem('tokenExp', tokenExpiry)
    sessionStorage.setItem('refreshToken', refreshToken)
  }

  login () {
    // this.$keycloak.login({ idpHint: 'idir', scope: 'offline_access' })
    this.$keycloak.login({ idpHint: 'idir' })
  }

  logoutTokenExpired () {
    console.log('==> In logoutTokenExpired')
    this.clearStorage()
    // this.init()
    location.href = '/queue'
  }

  logout () {
    this.$keycloak.logout({ redirectUri: window.location.origin + '/queue' })
    this.clearStorage()
  }

  clearStorage () {
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('tokenExp')
    sessionStorage.removeItem('refreshToken')
  }

  setBreakClickEvent () {
    // Click anywhere on screen to end "Break"
    // Prevent double-click on IE11  by delaying listener
    // As it's pure DOM, no need to worry about $nextTick
    setTimeout(() => {
      document.body.addEventListener('click', this.stopBreak)
    }, 100)
    const breakSwitch = document.getElementById('break-switch')
    if (breakSwitch !== null) {
      breakSwitch.style.pointerEvents = 'none' // Prevent double click event
    }
  }

  stopBreak () {
    const loginStateID = this.csr_states.Login
    this.setCSRState(loginStateID)
    this.setUserCSRStateName('Login')
    this.updateCSRState()
  }

  refreshToken (minValidity: any) {
    const secondsLeft = Math.round(
      this.$keycloak.tokenParsed.exp +
        this.$keycloak.timeSkew -
        new Date().getTime() / 1000
    )
    console.log(
      '==> Updating token.  Currently valid for ' + secondsLeft + ' seconds'
    )
    this.$keycloak
      .updateToken(minValidity)
      .success((refreshed: any) => {
        if (refreshed) {
          console.log('Token refreshed and is below')
          console.log(this.$keycloak.tokenParsed)
          console.log('Refresh token is below')
          console.log(this.$keycloak.refreshTokenParsed)
        } else {
          console.log('Token not refreshed')
        }
        const successSecondsLeft = Math.round(
          this.$keycloak.tokenParsed.exp +
            this.$keycloak.timeSkew -
            new Date().getTime() / 1000
        )
        console.log(
          '    --> After refresh.  Token now valid for ' +
            successSecondsLeft +
            ' seconds'
        )
      })
      .error((error: any) => {
        console.log('Failed to refresh token')
        console.log(error)
        const errorSecondsLeft = Math.round(
          this.$keycloak.tokenParsed.exp +
            this.$keycloak.timeSkew -
            new Date().getTime() / 1000
        )
        console.log(
          '    --> After refresh.  Token now valid for ' +
            errorSecondsLeft +
            ' seconds'
        )
        if (errorSecondsLeft < 90) {
          this.logoutTokenExpired()
        }
      })
  }

  created () {
    this.setupKeycloakCallbacks()
    _.defer(this.initSessionStorage)
    // use 'force' to avoid race condition, as user may not be set yet
    this.getOffices('force')
  }

  updated () {
    const csrStatus = this.user.csr_state.csr_state_name

    if (csrStatus === 'Break') {
      this.setBreakClickEvent()
    } else {
      document.body.removeEventListener('click', this.stopBreak)
      const breakSwitch = document.getElementById('break-switch')
      if (breakSwitch !== null) {
        breakSwitch.style.pointerEvents = 'all'
      }

      // document.getElementById('break-switch').style.pointerEvents = 'all'
    }
  }

  cancelOfficeSwitcher () {
    this.setOfficeSwitcher(false)
  }

  changeOffice (newOffice) {
    this.updateCSROffice(newOffice)
      .then(() => {
        console.log('Done updateCSROffice() then in Login.vue')
        this.setOfficeSwitcher(false)
        // Auto-refresh to reload all new data now that office has changed
        window.location.reload()
      })
      .catch(err => {
        let message = 'Something went wrong'
        if (
          err &&
          err.response &&
          err.response.data &&
          err.response.data.message
        ) {
          message = err.response.data.message
        }
        alert('Unable to change offices: ' + message)
        console.error('Unable to change offices: ' + message, { err })
        this.setOfficeSwitcher(false)
      })
  }
}
</script>

<style>
.custom-control-label::after,
.custom-control-label::before {
  top: 3px;
}

.navbar-label {
  color: white;
  margin-bottom: 0px;
  float: left;
  clear: both;
}

.navbar-brand {
  font-size: 0.85rem;
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
  -webkit-transition: 0.2s;
  transition: 0.2s;
  position: absolute;
  border-radius: 50%;
  top: 4px;
  left: 4px;
}

.circle2 {
  width: 25px;
  height: 25px;
  background-color: red;
  -webkit-transition: 0.2s;
  transition: 0.2s;
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

.clickable {
  cursor: pointer;
  transition: 0.1s;
}
.clickable:hover {
  color: #c7ddef;
  border-bottom: 1px dashed white;
}
</style>
