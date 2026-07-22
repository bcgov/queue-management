// Loads runtime configuration from /config/configuration.json.
// Each environment has its own ConfigMap with the same filename but different values.

type RuntimeConfig = {
  VUE_APP_ROOT_API?: string
  KEYCLOAK_CONFIG_URL?: string
  BC_SERVICES_CARD_URL?: string
}

const DEFAULT_API_BASE_URL = '/api/v1'
const DEFAULT_KEYCLOAK_CONFIG_URL = '/config/kc/keycloak-public.json'

let cachedConfig: RuntimeConfig | null = null
let inFlightConfig: Promise<RuntimeConfig> | null = null
let cachedApiBaseUrl: string | null = null

function normalizeApiBaseUrl(value: string | undefined): string {
  return value?.trim().replace(/\/$/, '') || DEFAULT_API_BASE_URL
}

async function loadRuntimeConfig(): Promise<RuntimeConfig> {
  if (cachedConfig !== null) return cachedConfig
  if (inFlightConfig) return inFlightConfig

  inFlightConfig = (async () => {
    // Only fetch from the browser — relative URLs have no base on the server.
    if (typeof window !== 'undefined') {
      try {
        const res = await fetch('/config/configuration.json', { cache: 'no-store' })
        if (res.ok) {
          cachedConfig = (await res.json()) as RuntimeConfig
          return cachedConfig
        }
      } catch {
        // Config file missing or unreachable — fall through to default.
      }
    }

    cachedConfig = {}
    return cachedConfig
  })().finally(() => {
    inFlightConfig = null
  })

  return inFlightConfig
}

export async function getApiBaseUrl(): Promise<string> {
  if (cachedApiBaseUrl !== null) return cachedApiBaseUrl
  const config = await loadRuntimeConfig()
  cachedApiBaseUrl = normalizeApiBaseUrl(config.VUE_APP_ROOT_API)
  return cachedApiBaseUrl
}

export async function getKeycloakConfigUrl(): Promise<string> {
  const config = await loadRuntimeConfig()
  return config.KEYCLOAK_CONFIG_URL?.trim() || DEFAULT_KEYCLOAK_CONFIG_URL
}

export async function getBCServicesCardUrl(): Promise<string> {
  const config = await loadRuntimeConfig()
  return config.BC_SERVICES_CARD_URL?.trim() || ''
}
