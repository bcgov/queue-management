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

  <SocketStatus v-if="this.$store.state.isLoggedIn" :button-style="buttonStyle" :socket-message="socketMessage" />

</template>

<script>
  import SocketStatus from './socketstatus'
  var io = require('socket.io-client')
  var socket

  export default {
    name: 'Socket',
    data() {
      return {
        socketConnected: false,
        buttonStyle: 'danger',
        socketMessage: 'disconnected'
      }
    },
    mounted() {
      this.connect()
      socket.on('connect',()=>{this.onConnect()})
      socket.on('disconnect',()=>{this.onDisconnect()})
      socket.on('reconnecting',()=>{this.onReconnecting()})
      socket.on('update_customer_list',()=>{
        this.$store.dispatch('getAllClients')
      })
    },
    methods: {
      connect() {
        socket = io(process.env.SOCKET_URL)
        this.socketMessage = 'establishing'
        this.buttonStyle = 'info'
      },
      join() {
        socket.emit('joinRoom',{count:0}, ()=>{console.log('socket emit: "joinRoom"')}
        )
        socket.on('joinRoomSuccess',
          ()=>{console.log('socket: "joinRoomSuccess"')}
        )
        socket.on('joinRoomFail',
         ()=>{console.log('socket: "joinRoomFailed"')}
        )
      },
      onConnect() {
        this.socketConnected = true
        this.buttonStyle = 'success'
        this.socketMessage = 'connected'
        this.join()
      },
      onDisconnect() {
        this.socketConnected = false
        this.buttonStyle = 'danger'
        this.socketMessage = 'disconnected'
        socket = io(process.env.API_URL)
      },
      onReconnecting() {
        this.socketConnected = false
        this.buttonStyle = 'warning'
        this.socketMessage = 'connecting'
      }
    },
    components: { SocketStatus }
  }
</script>


