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
    name: 'BoardSocket',
    created() {
      this.$root.$on('boardConnect', (data) => {
        this.connect(data)
      })
    },

    data() {
      return {
        reconnectInterval: null,
        data: '',
        office_id: ''
      }
    },

    methods: {
      connect(data) {
        this.office_id = data
        socket = io(process.env.SOCKET_URL, {
          path: '/api/v1/socket.io'
        })
        socket.on('connect',()=>{this.onConnect()})
        socket.on('disconnect',()=>{this.onDisconnect()})
        console.log('boardSocket attempting to connect')
        this.addListeners()
      },
      join() {
        console.log(socket.connected)
        socket.emit(
          'joinSmartboardRoom',
          {office_id: this.office_id},
          () => {console.log('socket emit: "joinSmartboardRoom"')}
        )
      },
      close() {
        socket.close()
        console.log('socket session closed')
      },
//LISTENERS
      addListeners() {
        socket.on(
          'reconnecting',
          () => { this.onReconnecting() }
        )
        socket.on(
          'joinSmartboardRoomSuccess',
          () => { this.onJoinRoom(true) }
        )
        socket.on(
          'joinSmartboardRoomFail',
          () => { this.onJoinRoom(false) }
        )
        socket.on(
          'citizen_invited',
           () =>{ this.onUpdateBoard() }
        )
      },
//LISTENER METHODS
      onConnect() {
        console.log('boardSocket connected')
        clearInterval(this.reconnectInterval)
        this.join()
      },
      onDisconnect() {
        console.log('boardSocket disconnected')
        this.reconnectInterval = setInterval( () => {
          console.log("boardSocket Reconnecting")
          socket.open(process.env.SOCKET_URL)
        }, 1000)
      },
      onReconnecting() {
        console.log('boardSocket reconnecting')
      },
      onJoinRoom(success) {
        if (success) {
          console.log('boardSocket received: "joinSmartboardRoomSuccess"')
        } else if (!success) {
          console.log('boardSocket received: "joinSmartboardRoomFail"')
        }
      },
      onUpdateBoard() {
        this.$root.$emit('addToBoard')
        console.log('socket received: "onUpdateBoard"')
      }
    }
  }
</script>


