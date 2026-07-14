// Loads runtime configuration from /config/configuration.json.
// Each environment has its own ConfigMap with the same filename but different values.

let cachedApiBaseUrl: string | null = null

export async function getApiBaseUrl(): Promise<string> {
  if (cachedApiBaseUrl !== null) return cachedApiBaseUrl

  // Only fetch from the browser — relative URLs have no base on the server.
  if (typeof window !== 'undefined') {
    try {
      const res = await fetch('/config/configuration.json', { cache: 'no-store' })
      if (res.ok) {
        const config = await res.json()
        cachedApiBaseUrl = String(config.VUE_APP_ROOT_API ?? '').trim().replace(/\/$/, '') || '/api/v1'
        return cachedApiBaseUrl
      }
    } catch {
      // Config file missing or unreachable — fall through to default.
    }
  }

  cachedApiBaseUrl = '/api/v1'
  return cachedApiBaseUrl
}
