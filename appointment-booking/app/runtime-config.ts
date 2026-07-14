// Loads runtime configuration from /config/configuration.json.
// Each environment has its own ConfigMap with the same filename but different values.

type RuntimeConfig = {
  // Shared with existing appointment-frontend ConfigMaps (legacy Vue env key name).
  VUE_APP_ROOT_API?: string
}

const DEFAULT_API_BASE_URL = '/api/v1'

let cachedApiBaseUrl: string | null = null
let inFlightApiBaseUrl: Promise<string> | null = null

function normalizeApiBaseUrl(value: string | undefined): string {
  return value?.trim().replace(/\/$/, '') || DEFAULT_API_BASE_URL
}

export async function getApiBaseUrl(): Promise<string> {
  if (cachedApiBaseUrl !== null) return cachedApiBaseUrl
  if (inFlightApiBaseUrl) return inFlightApiBaseUrl

  inFlightApiBaseUrl = (async () => {
    // Only fetch from the browser — relative URLs have no base on the server.
    if (typeof window !== 'undefined') {
      try {
        const res = await fetch('/config/configuration.json', { cache: 'no-store' })
        if (res.ok) {
          const config = (await res.json()) as RuntimeConfig
          cachedApiBaseUrl = normalizeApiBaseUrl(config.VUE_APP_ROOT_API)
          return cachedApiBaseUrl
        }
      } catch {
        // Config file missing or unreachable — fall through to default.
      }
    }

    cachedApiBaseUrl = DEFAULT_API_BASE_URL
    return cachedApiBaseUrl
  })().finally(() => {
    inFlightApiBaseUrl = null
  })

  return inFlightApiBaseUrl
}
