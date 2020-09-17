<template>
  <div>
    <router-view />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import App from './App.vue'

@Component({
  components: { App }
})
export default class MainApp extends Vue { }
</script>
