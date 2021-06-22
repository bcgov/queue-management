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
  <div id="LOGIN" v-if="!user.username && isLoggedIn">
    <b-alert
      variant="warning"
      dismissible
      :show="loginDismissCount"
      style="justify-content: center; top: 70px; font-size:1rem; border-radius: 0px; z-index: 1041"
      @dismissed="onDismissedLogin"
    >{{ loginAlertMessage }}</b-alert>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Mutation, State } from 'vuex-class'

@Component({})
export default class LoginWarning extends Vue {
  @State('loginAlertMessage') private loginAlertMessage!: any
  @State('loginDismissCount') private loginDismissCount!: boolean
  @State('user') private user!: any
  @State('isLoggedIn') private isLoggedIn!: any

  @Mutation('loginDismissCountDown') public loginDismissCountDown: any

  onDismissedLogin () {
    this.loginDismissCountDown(999)
  }
}

</script>
