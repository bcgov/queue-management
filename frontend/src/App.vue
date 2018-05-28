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
  <b-container>
    <b-row align-v="end">
      <b-col cols="9">
        <h1>
          <img src='./assets/bcid.jpg'/>
          Queue Management
        </h1>
        <Socket/>
      </b-col>
      <b-col cols="3">
        <Login></Login>
<<<<<<< HEAD
      </b-col>
    </b-row>
      <Controls v-if="this.$store.state.isLoggedIn"/>
  </b-container>
</template>

<script>
  import Login from './login';
  import Socket from './socket'
  import Controls from './controls'

  export default {
    name: 'App',
    components: {
      Login,
      Socket,
      Controls
=======
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
>>>>>>> upstream/proof-of-concept
    }
  }

</script>


