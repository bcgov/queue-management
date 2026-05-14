import type { RuntimeConfig } from '@/models/runtime-config'

interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown
  timeoutMs?: number
}

export class ApiClientError extends Error {
  status: number
  details?: unknown

  constructor(message: string, status = 0, details?: unknown) {
    super(message)
    this.name = 'ApiClientError'
    this.status = status
    this.details = details
  }
}

export class ApiClient {
  private baseUrl: string
  private timeoutMs: number

  constructor(config: RuntimeConfig) {
    this.baseUrl = config.apiBaseUrl.replace(/\/$/, '')
    this.timeoutMs = config.requestTimeoutMs
  }

  async get<T>(path: string, options: Omit<RequestOptions, 'method'> = {}): Promise<T> {
    return this.request<T>(path, { ...options, method: 'GET' })
  }

  private async request<T>(path: string, options: RequestOptions): Promise<T> {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), options.timeoutMs || this.timeoutMs)

    const normalizedPath = path.startsWith('/') ? path : `/${path}`
    const url = `${this.baseUrl}${normalizedPath}`

    try {
      const response = await fetch(url, {
        ...options,
        body: options.body ? JSON.stringify(options.body) : undefined,
        headers: {
          'Content-Type': 'application/json',
          ...(options.headers || {}),
        },
        signal: controller.signal,
      })

      if (!response.ok) {
        let details: unknown
        try {
          details = await response.json()
        } catch {
          details = await response.text()
        }

        throw new ApiClientError(`Request failed (${response.status})`, response.status, details)
      }

      return (await response.json()) as T
    } catch (error) {
      if (error instanceof ApiClientError) {
        throw error
      }

      if (error instanceof Error && error.name === 'AbortError') {
        throw new ApiClientError('Request timed out')
      }

      throw new ApiClientError('Network error')
    } finally {
      clearTimeout(timeout)
    }
  }
}
