import { render, screen, waitFor } from '@testing-library/react'
import type { ReactNode } from 'react'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import App from './App'

vi.mock('@/components/common', () => ({
  Layout: ({ children }: { children: ReactNode }) => <div>{children}</div>,
  Page: ({ children, title }: { children: ReactNode; title: string }) => (
    <section>
      <h1>{title}</h1>
      {children}
    </section>
  ),
}))

const loadRuntimeConfigMock = vi.fn()
const getOfficesMock = vi.fn()

vi.mock('@/services/runtime-config.service', () => ({
  loadRuntimeConfig: () => loadRuntimeConfigMock(),
}))

vi.mock('@/services/booking-api.service', () => ({
  getOffices: () => getOfficesMock(),
}))

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows successful API bootstrap state', async () => {
    loadRuntimeConfigMock.mockResolvedValue({
      apiBaseUrl: '/api/v1',
      requestTimeoutMs: 10000,
    })
    getOfficesMock.mockResolvedValue({ offices: [], errors: {} })

    render(<App />)

    expect(screen.getByRole('heading', { name: 'Appointment Booking' })).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.getByText('API base URL: /api/v1')).toBeInTheDocument()
      expect(screen.getByText('Booking API connection established.')).toBeInTheDocument()
    })
  })
})
