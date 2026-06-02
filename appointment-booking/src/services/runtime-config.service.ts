import type { RuntimeConfig } from '@/models/runtime-config'

const DEFAULT_TIMEOUT_MS = 10000
const RUNTIME_CONFIG_URL = '/config/configuration.json'

function fromEnvironment(): RuntimeConfig {
  return {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api/v1',
    requestTimeoutMs: Number(import.meta.env.VITE_REQUEST_TIMEOUT_MS || DEFAULT_TIMEOUT_MS),
  }
}

export async function loadRuntimeConfig(): Promise<RuntimeConfig> {
  try {
    const response = await fetch(RUNTIME_CONFIG_URL, { cache: 'no-store' })
    if (!response.ok) {
      return fromEnvironment()
    }

    const json = (await response.json()) as Partial<RuntimeConfig> & { VUE_APP_ROOT_API?: string }
    const fallback = fromEnvironment()

    return {
      apiBaseUrl: json.VUE_APP_ROOT_API ?? fallback.apiBaseUrl,
      requestTimeoutMs: Number(json.requestTimeoutMs || fallback.requestTimeoutMs),
    }
  } catch {
    return fromEnvironment()
  }
}
