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
</template>

<script>
  var io = require('socket.io-client')
  var socket

  export default {
    name: 'Socket',
    data() {
      return {
        reconnectInterval: null
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
        console.log('socket connected')
        clearInterval(this.reconnectInterval)
        this.join()
      },
      onDisconnect() {
        console.log('socket disconnected')

        // Try to reconnect every second
        this.reconnectInterval = setInterval( () => {
          console.log("Reconnecting")
          socket.open(process.env.SOCKET_URL)
        }, 1000);
      },
      onReconnecting() {
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
          console.log('socket received: "updateCustomerList"')
          this.$store.dispatch('getAllCitizens')
      },
      close() {
        socket.close()
        console.log('socket session closed')
      }
    },
    components: { }
  }
</script>


