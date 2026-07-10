// Service type used by the frontend after mapping from the API.
export type OnlineAvailability = 'SHOW' | 'DISABLE'

export type Service = {
  id: number
  name: string
  onlineAvailability: OnlineAvailability
  isOnlineBookable: boolean
}

// API response row from GET /api/v1/services/.
type ApiService = {
  service_id: number
  service_name: string
  external_service_name: string | null
  actual_service_ind: number
  display_dashboard_ind: number
  online_availability: string | null
  deleted: string | null
}

type ApiServicesResponse = {
  services: ApiService[]
  errors: Record<string, unknown>
}

function apiBaseUrl() {
  // VITE_Q_API_URL should include /api/v1, e.g. http://localhost:5000/api/v1
  const fromEnv = import.meta.env.VITE_Q_API_URL
  if (fromEnv) {
    return fromEnv.replace(/\/$/, '')
  }
  return '/api/v1'
}

// API sends values like "Availability.SHOW" or sometimes just "SHOW".
function readAvailability(value: string | null): OnlineAvailability | null {
  if (!value) {
    return null
  }

  if (value === 'HIDE' || value.endsWith('.HIDE')) {
    return null
  }

  if (value === 'SHOW' || value.endsWith('.SHOW')) {
    return 'SHOW'
  }

  if (value === 'DISABLE' || value.endsWith('.DISABLE')) {
    return 'DISABLE'
  }

  return null
}

function keepForPublicList(row: ApiService): OnlineAvailability | null {
  // Public service filter rules.
  if (row.actual_service_ind !== 1) {
    return null
  }

  if (row.display_dashboard_ind !== 1) {
    return null
  }

  if (row.deleted) {
    return null // skip deleted services; global /services/ still returns them
  }

  const availability = readAvailability(row.online_availability)
  if (availability === 'SHOW' || availability === 'DISABLE') {
    return availability
  }

  return null
}

function mapRow(row: ApiService, availability: OnlineAvailability): Service {
  // Frontend label: external_service_name, or service_name as fallback.
  const name = row.external_service_name?.trim() || row.service_name

  return {
    id: row.service_id,
    name,
    onlineAvailability: availability,
    isOnlineBookable: availability === 'SHOW',
  }
}

// Fetch from the API and filter here, not in the UI.
export async function getPublicServices(): Promise<Service[]> {
  const url = `${apiBaseUrl()}/services/`
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error(`Could not load services (${response.status})`)
  }

  const body = (await response.json()) as ApiServicesResponse
  const rows = body.services ?? []
  const services: Service[] = []

  for (const row of rows) {
    const availability = keepForPublicList(row)
    if (!availability) {
      continue
    }
    services.push(mapRow(row, availability))
  }

  return services
}
