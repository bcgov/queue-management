<template>
  <div id="app" class="container">
    <div class="row">
      <div class="col-lg-8">
        <h1>Queue Management</h1>
      </div>
      <div class="col-lg-4">
        <Login></Login>
        <b-button @click="sendJoinRoomEvent()"
              id="login-button">Join Room</b-button>
        <b-button @click="sendMyEvent()"
              id="login-button">Send Event</b-button>
        <b-button @click="pingRoom()"
              id="login-button">Ping Room</b-button>
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
    disconnect() {
      console.log("Disconnected")
    },
    joinRoomSuccess() {
      console.log("Success")
    },
    joinRoomFail() {
      console.log("Fail")
    },
    myResponse() {
      console.log("Does this work")
    },
    update_customer_list() {
      console.log("Received update customer")
    },
    ping_room() {
    console.log("ping_room")
    }
  },
  methods: {
    sendJoinRoomEvent() {
      this.$socket.emit('joinRoom', {data: 'This is a test every 3s', count: 0, "office_id": "vancouver" })
    },
    sendMyEvent() {
      this.$socket.emit('myEvent', {data: 'This is a test every 3s', count: 0, "office_id": "vancouver" })
    },
    pingRoom() {
      this.$socket.emit('pingRoom', {data: 'This is a ping test' })
    },
    sendLogIn() {
      this.$store.commit('logIn')
    },
    pingServer(val) {
      this.$socket.emit('PING')
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
