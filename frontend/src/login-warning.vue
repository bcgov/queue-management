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
    <b-alert variant="warning"
             dismissible
             :show=loginDismissCount
             style="h-align: center; top: 70px; font-size:1rem; border-radius: 0px; z-index: 1041"
             @dismissed="onDismissedLogin">
             {{ loginAlertMessage }}
    </b-alert>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
export default {
  name: 'LoginWarning',
  computed: {
    ...mapState([ 'loginAlertMessage', 'loginDismissCount', 'user', 'isLoggedIn' ])
  },
  methods: {
    ...mapMutations(['loginDismissCountDown']),

    onDismissedLogin() {
      this.loginDismissCountDown(999)
    }
  }
}
</script>
