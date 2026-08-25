import { getApiBaseUrl } from '../runtime-config'

// Mapped office for the booking locations step.
// appointmentsDisabled / isBookable are derived — the API does not send them.
export type ServiceLocation = {
  id: number
  name: string
  address: string
  latitude: number | null
  longitude: number | null
  appointmentMessage: string
  nextAppointmentDate: string | null
  appointmentsDisabled: boolean
  isBookable: boolean
}

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
  next_appointment_date: string | null
}

type ApiOfficesResponse = {
  offices: ApiOffice[]
}

// API sends "Status.SHOW" or "SHOW". HIDE (and unknown) are omitted from the list.
function readOnlineStatus(value: string | null): 'SHOW' | 'DISABLE' | null {
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

// Fetch offices for a selected service. Keeps SHOW and DISABLE; omits HIDE/deleted.
// Throws on fetch/HTTP/parse failure so the page can tell error apart from empty [].
export async function getServiceLocations(serviceId: number): Promise<ServiceLocation[]> {
  const url = `${await getApiBaseUrl()}/offices?service_id=${serviceId}`

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

  const locations: ServiceLocation[] = []

  for (const row of body.offices ?? []) {
    if (row.deleted) {
      continue
    }

    const status = readOnlineStatus(row.online_status)
    if (!status) {
      continue
    }

    const nextAppointmentDate = row.next_appointment_date ?? null
    const appointmentsDisabled = status === 'DISABLE' || !row.appointments_enabled_ind

    locations.push({
      id: row.office_id,
      name: row.office_name.trim(),
      address: row.civic_address?.trim() || '',
      latitude: row.latitude,
      longitude: row.longitude,
      appointmentMessage: row.office_appointment_message?.trim() || '',
      nextAppointmentDate,
      appointmentsDisabled,
      isBookable: !appointmentsDisabled && nextAppointmentDate !== null,
    })
  }

  return locations
}
