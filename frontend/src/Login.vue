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
  <div v-if="!this.$store.state.isLoggedIn"
       id="login-form">
    <b-form-input v-model="username"
                  id="login-username"
                  type="text"
                  placeholder="Username"/>
    <b-form-input v-model="password"
                  id="login-password"
                  type="password"
                  placeholder="Password"/>
    <b-button @click="login()"
              id="login-button">Login</b-button>
  </div>
  <div v-else>
    <h6>Logged in as: {{  this.$store.state.user.name }}</h6>
    <b-button @click="logout()"
              id="logout-button">Logout</b-button>
  </div>
</template>

<script type="text/javascript">
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login() {
      let url = "/login/"
      let data = {
        username: this.username,
        password: this.password
      }

      this.$axios.post(url, data)
        .finally( () => {
          this.verifyLogin()
        })
    },
    logout() {
      let url = "/logout/"
      this.$axios.get(url)
      .then( () => {
        this.$store.commit('logOut')
      })
    },
    verifyLogin() {
      let url  = "/users/me/"
      this.$axios.get(url)
        .then( response => {
          this.$store.commit('logIn')
          this.$store.commit('setUser', {
            name: response.data.username,
            office_id: response.data.office_id
          })
        })
    }
  }
}
</script>
