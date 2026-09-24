import { getApiBaseUrl } from '../runtime-config'
import { getAccessToken } from '../auth/token-refresh'

// Hold a timeslot so another user cannot book it while this user finishes booking.
// Returns the draft appointment id, which the confirm step will need later.
export async function createDraftAppointment(body: {
  office_id: number
  service_id: number
  start_time: string
  end_time: string
}): Promise<number> {
  const token = await getAccessToken()

  const baseUrl = await getApiBaseUrl()
  const res = await fetch(`${baseUrl}/appointments/draft`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    // Conflict responses include a string message; otherwise use a generic fallback.
    const error = (await res.json().catch(() => null)) as { message?: unknown } | null
    const message = typeof error?.message === 'string' ? error.message : null
    throw new Error(message || 'Unable to hold this time slot')
  }

  const created = (await res.json()) as { appointment?: { appointment_id?: number } }
  const appointmentId = created.appointment?.appointment_id
  if (!appointmentId) {
    throw new Error('Unable to hold this time slot')
  }

  return appointmentId
}

// Release a held timeslot. 404 means the draft already expired or was deleted.
export async function deleteDraftAppointment(appointmentId: number): Promise<void> {
  const token = await getAccessToken()

  const baseUrl = await getApiBaseUrl()
  const res = await fetch(`${baseUrl}/appointments/draft/${appointmentId}/`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!res.ok && res.status !== 404) {
    throw new Error(`Failed to release held time slot (${res.status})`)
  }
}
