<template>
  <div id="app" class="container">
    <div class="row">
      <div class="col-lg-8">
        <h1>Queue Management</h1>
      </div>
      <div class="col-lg-4">
        <Login></Login>
      </div>
    </div>
  </div>
</template>

<script>
import Login from './Login';

export default {
  name: 'app',
  components: {
    Login
  },
  data() {
    return {
      isConnected: false,
      isLoggedIn: false,
      socketMessage: 'heh',
      name: ''
    }
  },
  sockets: {
    connect() {
      this.isConnected = true;
      console.log('socket connected');
    },
    customEmit(val) {
      console.log('this method fired by socket server. eg: io.emit("customEmit", data)');
    },
    messageChannel(data) {
      this.socketMessage = data;
    }
  },
  methods: {
    sendLogIn() {
      this.$store.commit('logIn')
    },
    pingServer(val) {
      this.$socket.emit('PING')
    },
    buttonClick() {
      let url  = 'http://qsystem-dev.apps.olivewoodsoftware.com/api/v1/users/me/'
      this.$axios.get(url)
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
