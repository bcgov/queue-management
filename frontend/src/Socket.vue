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

  <SocketStatus :button-style="buttonStyle" :socket-message="socketMessage" />

</template>

<script>
  import SocketStatus from './SocketStatus'
  var io = require('socket.io-client')
  var socket

  export default {
    name: 'Socket',
    data() {
      return {
        buttonStyle: 'danger',
        socketMessage: 'disconnected',
        preventReconnect: false
      }
    },
    mounted() {
      this.$root.$on('socketConnect', () => {
        this.connect()
      })

      this.$root.$on('socketDisconnect', () => {
        this.close()
      })
    },
    methods: {
      connect() {
        this.preventReconnect = false
        socket = io(process.env.SOCKET_URL, {
          path: '/api/v1/socket.io'
        })
        socket.on('connect',()=>{this.onConnect()})
        socket.on('disconnect',()=>{this.onDisconnect()})
        console.log('socket attempting to connect')
        this.addListeners()
      },
      addListeners() {
        socket.on('reconnecting',()=>{this.onReconnecting()})
        socket.on('joinRoomSuccess',()=>{this.onJoinRoom(true)})
        socket.on('joinRoomFail',()=>{this.onJoinRoom(false)})
        socket.on('update_customer_list',()=>{this.onUpdateCustomerList()})
        console.log('socket: listeners added')
      },
      join() {
        console.log(socket.connected)

        socket.emit('joinRoom',{count:0}, ()=>{console.log('socket emit: "joinRoom"')}
        )
      },
      onConnect() {
        this.buttonStyle = 'success'
        this.socketMessage = 'connected'
        console.log('socket connected')
        this.join()
      },
      onDisconnect() {
        this.buttonStyle = 'danger'
        this.socketMessage = 'disconnected'
        console.log('socket disconnected')
        if (!this.preventReconnect) {
          socket.open(process.env.SOCKET_URL)
        }
      },
      onReconnecting() {
        this.buttonStyle = 'warning'
        this.socketMessage = 'connecting'
        console.log('socket reconnecting')
      },
      onJoinRoom(success) {
        if (success) {
          console.log('socket received: "joinRoomSuccess"')
        } else if (!success) {
          console.log('socket received: "joinRoomFailed"')
        }
      },
      onUpdateCustomerList() {
          console.log('socket received: "updatecustomerlist"')
          this.$store.dispatch('getAllCitizens')
      },
      close() {
        this.preventReconnect = true
        socket.close()
        console.log('socket session closed')
      }
    },
    components: { SocketStatus }
  }
</script>


