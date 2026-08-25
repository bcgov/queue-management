import { getApiBaseUrl } from '../runtime-config'

// Service type used by the frontend after mapping from the API.
export type OnlineAvailability = 'SHOW' | 'DISABLE'

export type Service = {
  id: number
  name: string
  onlineAvailability: OnlineAvailability
  isOnlineBookable: boolean
  /** Knowledge-test (DLKT) service; used to hide offices with no DLKT capacity. */
  isDlkt: boolean
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
  is_dlkt?: boolean | null
}

type ApiServicesResponse = {
  services: ApiService[]
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
  return availability
}

function mapRow(row: ApiService, availability: OnlineAvailability): Service {
  // Frontend label: external_service_name, or service_name as fallback.
  const name = row.external_service_name?.trim() || row.service_name.trim()

  return {
    id: row.service_id,
    name,
    onlineAvailability: availability,
    isOnlineBookable: availability === 'SHOW',
    isDlkt: row.is_dlkt === true,
  }
}

// Fetch from the API and filter here, not in the UI.
// Throws on fetch/HTTP/parse failure so the page can tell error apart from empty [].
export async function getPublicServices(): Promise<Service[]> {
  const url = `${await getApiBaseUrl()}/services/`

  let body: ApiServicesResponse
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('Failed to load services')
    }
    body = (await response.json()) as ApiServicesResponse
  } catch {
    throw new Error('Failed to load services')
  }

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
