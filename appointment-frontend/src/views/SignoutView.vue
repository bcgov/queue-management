<template>
  <loading-screen :is-loading="isLoading"></loading-screen>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import KeyCloakService from '../services/keycloak.services'
import LoadingScreen from '@/components/common/LoadingScreen.vue'

@Component({
  methods: {
  },
  components: {
    LoadingScreen
  }
})

export default class SignoutView extends Vue {
  @Prop() redirectUrl: string
  private isLoading = true

  async mounted () {
    this.$store.replaceState({})
    await KeyCloakService.logout(this.redirectUrl ? decodeURIComponent(this.redirectUrl) : undefined)
  }
}
</script>

<style lang="scss" scoped>
// empty block
</style>
