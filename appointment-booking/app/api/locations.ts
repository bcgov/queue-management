import { getApiBaseUrl } from '../runtime-config'

// Location type used by the booking flow after mapping from the offices API.
export type Location = {
  id: number
  name: string
  address: string
  latitude: number | null
  longitude: number | null
  appointmentMessage: string
}

// API response row from GET /api/v1/offices/.
type ApiOffice = {
  office_id: number
  office_name: string
  civic_address: string | null
  latitude: number | null
  longitude: number | null
  appointments_enabled_ind: number
  online_status: string | null
  deleted: string | null
  office_appointment_message: string | null
}

type ApiOfficesResponse = {
  offices: ApiOffice[]
}

// Fetch bookable offices for the booking locations step.
// Throws on fetch/HTTP/parse failure so the page can tell error apart from empty [].
export async function getBookingLocations(): Promise<Location[]> {
  const url = `${await getApiBaseUrl()}/offices/`

  let body: ApiOfficesResponse
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('Failed to load locations')
    }
    body = (await response.json()) as ApiOfficesResponse
  } catch {
    throw new Error('Failed to load locations')
  }

  const locations: Location[] = []

  for (const row of body.offices ?? []) {
    const status = row.online_status ?? ''
    const isShow = status === 'SHOW' || status.endsWith('.SHOW')
    if (row.deleted || !row.appointments_enabled_ind || !isShow) {
      continue
    }

    locations.push({
      id: row.office_id,
      name: row.office_name.trim(),
      address: row.civic_address?.trim() || '',
      latitude: row.latitude,
      longitude: row.longitude,
      appointmentMessage: row.office_appointment_message?.trim() || '',
    })
  }

  return locations
}
