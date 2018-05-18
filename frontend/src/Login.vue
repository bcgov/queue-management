<template>
  <div v-if="!this.$store.state.isLoggedIn">
    <b-form-input v-model="username"
                  type="text"
                  placeholder="Enter your name"/>
    <b-form-input v-model="password"
                  type="password"
                  placeholder="password"/>
    <b-button @click="postLogin()">Login</b-button>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    postLogin() {
      let url = 'http://qsystem-dev.apps.olivewoodsoftware.com/login/'
      let data = {
        username: this.username,
        password: this.password
      }
      this.$axios.post(url, data)
        .then( () => {
          this.$store.commit('logIn')
        })
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
