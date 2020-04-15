<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script lang="ts">
// Libraries
import { Component, Vue } from 'vue-property-decorator'

// Components
import { HelloWorld } from '@/components/Home'

@Component({
  components: {
    HelloWorld
  }
})
export default class Home extends Vue {}
</script>
