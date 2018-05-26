<template>
  <SocketStatus v-if="this.$store.state.isLoggedIn" :button-style="buttonStyle" :socket-message="socketMessage" />
</template>

<script>
  import SocketStatus from './SocketStatus'

  export default { 
    name: 'Socket',
    data() {
      return {
        socketConnected: false,
        buttonStyle: 'danger',
        socketMessage: 'disconnected',
      }
    },
    sockets: { 
      connect() {
        this.socketConnected = true,
        this.buttonStyle = 'success',
        this.socketMessage = 'connected'
        this.$socket.emit('join', () => {
          console.log('line 23 reached')
          this.createJoinListener()
        })
      },
      disconnect() {
        this.socketConnected = false,
        this.buttonStyle = 'danger',
        this.socketMessage = 'disconnected'
      },
      reconnecting() {
        this.socketConnected = false,
        this.buttonStyle = 'warning',
        this.socketMessage = 'connecting'
      }
    },
    methods: {
      pingServer(val) {
        this.$socket.emit('PING')
      },
      myEvent(socket) {
        socket.emit("my event", {count: 1}, (data)=>{
          console.log(data)
        })
      },
      createJoinListener() {
        console.log('line 48 reached')
        this.$options.sockets.joined = data => {
          console.log('line 50')
        }
        this.$options.sockets.join_fail = data => {
          console.log('line 53')
        }
      }
    },
    components: { SocketStatus }
  } 
</script>


