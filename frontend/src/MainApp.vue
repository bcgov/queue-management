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

<style lang="scss">
.task-outer-container .row .v-select .vs__dropdown-toggle {
    width: 100% !important;
    height: 100% !important;
  }
  .service-flow-body {
    padding-right: 0px !important;
    overflow-y: hidden !important;
}
</style>
