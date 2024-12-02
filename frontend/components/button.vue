<template>
<button
   @click="login"
   class="p-sm m-huge  rounded-md bg-surface-primary text-white border-bcdsBlue border shadow-xs"
>
<span class="mr-2 max-w-28">Login</span>
</button>
</template>

<script lang="ts" setup>
import { useKeycloakStore } from '@/stores/keycloak'

const keycloakStore = useKeycloakStore()

const login = async () => {
  console.log("1. Login invoked")
  await keycloakStore.login()
}
</script>
