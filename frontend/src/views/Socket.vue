  <!-- /*  Copyright 2015 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. */ -->

<template>
  <div></div>
  <!-- no template -->
</template>

<script lang="ts">
import { Action, namespace } from 'vuex-class'
import { Component, Vue } from 'vue-property-decorator'

// import { mapActions } from 'vuex'
import config from './../../config'
import configMap from '@/utils/config-helper'

const io = require('socket.io-client')
let socket

const appointmentsModule = namespace('appointmentsModule')

@Component
export default class Socket extends Vue {
  @Action('screenIncomingCitizen') public screenIncomingCitizen: any

  @appointmentsModule.Action('updateAppointments') public updateAppointments: any
  public socketTimeout : number = 3000
  public socketDelayMax : number = 100
  public reconnectInterval: any = null

  mounted () {
    this.$root.$on('socketConnect', () => {
      this.connect()
    })

    this.$root.$on('socketDisconnect', () => {
      this.close()
    })
  }

  connect () {
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
    console.log('Socket attempting to connect')
    this.addListeners()
  }

  addListeners () {
    socket.on('reconnecting', () => { this.onReconnecting() })
    socket.on('joinRoomSuccess', () => { this.onJoinRoom(true) })
    socket.on('joinRoomFail', () => { this.onJoinRoom(false) })
    socket.on('get_Csr_State_IDs', () => { this.getCsrStateIDs() })
    socket.on('update_customer_list', () => { this.onUpdateCustomerList() })
    socket.on('update_active_citizen', (citizen) => { this.onUpdateActiveCitizen(citizen) })
    socket.on('csr_update', (data) => { this.onCSRUpdate(data) })
    socket.on('clear_csr_cache', (data) => { this.onClearCsrCache(data) })
    socket.on('update_offices_cache', () => { this.onUpdateOfficesCache() })


    socket.on('appointment_create', (appointment) => {
      this.onUpdateAppointment(appointment, 'create')
    })

    socket.on('appointment_update', (appointment) => {
      this.onUpdateAppointment(appointment, 'update')
    })

    socket.on('appointment_delete', (appointment) => {
      this.onUpdateAppointment(appointment, 'delete')
    })

  }

  join () {
    // console.log('==> In Socket.vue.join, socket.io.engine.id is: ' + socket.io.engine.id.toString())
    socket.emit('joinRoom', { count: 0 }, () => { console.log('socket emit: "joinRoom"') }
    )
  }

  onCSRUpdate (data) {
    console.log('socket received: "csr_update"')
    if (this.$store.state.user.role.role_code === 'GA') {
      console.log('--> person is a GA -> calling getCsrs routine')
      this.$store.dispatch('getCsrs')
    }
  }

  onConnect () {
    console.log('socket connected')
    clearInterval(this.reconnectInterval)
    this.join()
  }

  onDisconnect () {
    console.log('socket disconnected')
    // Try to reconnect every second
    this.reconnectInterval = setInterval(() => {
      console.log('Reconnecting')
      socket.open(config.SOCKET_URL)
    }, 1000)
  }

  onReconnecting () {
    console.log('socket reconnecting')
  }

  onJoinRoom (success) {
    if (success) {
      console.log('socket received: "joinRoomSuccess"')
    } else if (!success) {
      console.log('socket received: "joinRoomFailed"')
    }
  }

  onUpdateActiveCitizen (citizen) {
    console.log('socket received: "update_active_citizen" ')
    this.screenIncomingCitizen({ citizen, route: this.$route })
  }


  onUpdateAppointment (appointment, action) {
    this.updateAppointments({ appointment, action })
  }

  onUpdateCustomerList () {
    console.log('socket received: "updateCustomerList"')
    this.$store.dispatch('getAllCitizens')
  }

  onClearCsrCache (data) {
    console.log('socket received: "clear_csr_cache"')
    socket.emit('clear_csr_user_id', data.id)
  }

  getCsrStateIDs () {
    console.log('socket received: "getCsrStateIDs"')
    this.$store.dispatch('getCsrStateIDs')
  }

  onUpdateOfficesCache () {
    console.log('socket received: "update_offices_cache"')
    socket.emit('sync_offices_cache')
  }

  close () {
    socket.close()
    console.log('socket session closed')
  }
}
</script>
