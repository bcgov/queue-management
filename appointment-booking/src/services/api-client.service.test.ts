import { describe, expect, it, vi, afterEach } from 'vitest'
import { ApiClient } from './api-client.service'

const config = {
  apiBaseUrl: '/api/v1',
  requestTimeoutMs: 50,
}

describe('ApiClient', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.useRealTimers()
  })

  it('throws ApiClientError with status for non-2xx responses', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ message: 'broken' }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
        },
      }),
    )

    const apiClient = new ApiClient(config)

    await expect(apiClient.get('/offices/')).rejects.toMatchObject({
      name: 'ApiClientError',
      status: 500,
    })

    expect(fetchSpy).toHaveBeenCalledOnce()
  })

  it('throws timeout error when request exceeds configured timeout', async () => {
    vi.useFakeTimers()

    vi.spyOn(globalThis, 'fetch').mockImplementation(
      (_, init?: RequestInit): Promise<Response> =>
        new Promise((_, reject) => {
          init?.signal?.addEventListener('abort', () => {
            const abortError = new Error('Aborted')
            abortError.name = 'AbortError'
            reject(abortError)
          })
        }),
    )

    const apiClient = new ApiClient({ ...config, requestTimeoutMs: 10 })
    const request = apiClient.get('/offices/')
    const rejection = expect(request).rejects.toMatchObject({
      name: 'ApiClientError',
      message: 'Request timed out',
      status: 0,
    })

    await vi.advanceTimersByTimeAsync(11)
    await rejection
  })
})
