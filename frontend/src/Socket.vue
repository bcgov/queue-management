<template>
  <div>
  <SocketStatus v-if="this.$store.state.isLoggedIn" :button-style="buttonStyle" :socket-message="socketMessage" />
  <b-button @click="doStuff">yassss!</b-button>
</div>
</template>

<script>
  import SocketStatus from './SocketStatus'
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
    },
    methods: {
      connect() {
        socket = io(process.env.API_URL)
        this.socketMessage = 'establishing'
        this.buttonStyle = 'info'
      },
      join() {
        socket.emit('joinRoom', data=>{console.log(data)})
        socket.on('joined', ()=>{console.log('joined')})
        socket.on('join_fail', ()=>{console.log('failed')})
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
      },
      myEvent() {
        socket.emit('myEvent', {data: 'This is a test every 3s', count: 0}) 
        socket.on('myResponse', data=>{console.log(data)})
      }
    },
    components: { SocketStatus }
  } 
</script>


