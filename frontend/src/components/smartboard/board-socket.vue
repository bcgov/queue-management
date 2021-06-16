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

<template></template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import config from '../../../config'
import configMap from '@/utils/config-helper'

const io = require('socket.io-client')
let socket

@Component({})
export default class BoardSocket extends Vue {
  @Prop({ default: '' })
  private smartboardData!: any

  private reconnectInterval: any = null
  public socketTimeout : number = 20000
  public socketDelayMax : number = 5000
  

  connect (data) {
    this.socketTimeout = configMap.getSocketTimeout()
    this.socketDelayMax = configMap.getSocketDelayMax()
    console.log('Socket Timeout value = ',this.socketTimeout)
    console.log('Socket Reconnection Delay Max value = ',this.socketDelayMax)
    
    socket = io(config.SOCKET_URL, {
      timeout: this.socketTimeout,
      reconnectionDelayMax: this.socketDelayMax,
      path: '/api/v1/socket.io',
      transports: ['websocket']
    })
    socket.on('connect', () => { this.onConnect() })
    socket.on('disconnect', () => { this.onDisconnect() })
    console.log('boardSocket attempting to connect')
    this.addListeners()
  }

  join () {
    socket.emit(
      'joinSmartboardRoom',
      { office_id: this.smartboardData.office_number },
      () => { console.log('socket emit: "joinSmartboardRoom"') }
    )
  }

  close () {
    socket.close()
    console.log('socket session closed')
  }

  // LISTENERS
  addListeners () {
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
      () => { this.onUpdateBoard() }
    )
    socket.on(
      'digital_signage_msg_update',
      () => { this.onDigitalSignageMsgUpdate() }
    )
  }

  // LISTENER METHODS
  onConnect () {
    console.log('boardSocket connected')
    // console.log('==> In board-socket.vue, onConnect, socket.io.engine.id is: ' + socket.io.engine.id.toString())
    console.log('==> In board-socket.vue, onConnect, socket.io.engine.id is: ' + socket.io.engine.id)
    clearInterval(this.reconnectInterval)
    this.join()
  }

  onDisconnect () {
    console.log('boardSocket disconnected')
    this.reconnectInterval = setInterval(() => {
      console.log('boardSocket Reconnecting')
      socket.open(config.SOCKET_URL)
    }, 1000)
  }

  onReconnecting () {
    console.log('boardSocket reconnecting')
  }

  onJoinRoom (success) {
    if (success) {
      console.log('boardSocket received: "joinSmartboardRoomSuccess"')
    } else if (!success) {
      console.log('boardSocket received: "joinSmartboardRoomFail"')
    }
  }

  onUpdateBoard () {
    this.$root.$emit('addToBoard')
    console.log('socket received: "onUpdateBoard"')
  }

  onDigitalSignageMsgUpdate () {
    this.$root.$emit('onDigitalSignageMsgUpdate')
    console.log('socket received: "onDigitalSignageMsgUpdate"')
  }

  created () {
    this.$root.$on('boardConnect', (data) => {
      this.connect(data)
    })
  }
}
</script>
