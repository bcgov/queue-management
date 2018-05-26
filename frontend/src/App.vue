<template>
  <b-container>
    <b-row>
      <b-col cols="10">
        <img src='./assets/bcid.jpg'/>
        <h1>Queue Management</h1>
        <Socket/>
      
      </b-col>
      <b-col cols="2">
        <Login></Login>
      </b-col>
    </b-row>
      <Controls v-if="this.$store.state.isLoggedIn"/>
  </b-container>
</template>

<script>
  import Login from './Login';
  import Socket from './Socket'
  import Controls from './Controls'
  import ClientTable from './ClientTable'
  import ClientInput from './ClientInput'

  export default {
    name: 'app',
    components: {
      Login,
      Socket,
      Controls
    }
  }

</script>


