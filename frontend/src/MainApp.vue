<template>
  <div>
    <router-view />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
// import App from './view/App.vue'

@Component({
  components: {}
})
export default class MainApp extends Vue { }
</script>
