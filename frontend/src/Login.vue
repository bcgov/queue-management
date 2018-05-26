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
            username: response.data.username,
            office_id: response.data.office_id
          })
        })
    }
  }
}
</script>
