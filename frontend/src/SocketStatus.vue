<template>
  <h6>
    Socket Connection: 
    <b-badge :variant="buttonStyle"> 
      {{ socketMessage }} 
    </b-badge>
  </h6>
</template>

<script>
  export default { 
    name: 'SocketStatus',
    props: [ 'buttonStyle', 'socketMessage' ]
  }
</script>


