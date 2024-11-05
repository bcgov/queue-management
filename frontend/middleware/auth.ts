import { defineNuxtRouteMiddleware, useRouter } from 'nuxt/app'
import { useKeycloakStore } from '@/stores/keycloak'

export default defineNuxtRouteMiddleware(async () => {
  const keycloakStore = useKeycloakStore()
  await keycloakStore.initKeycloak()

  if (!keycloakStore.authenticated) {
    const router = useRouter()
    return router.push('/')
  }
})
