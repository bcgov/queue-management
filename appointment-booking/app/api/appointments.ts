import { getApiBaseUrl } from '../runtime-config'
import { getAccessToken } from '../auth/token-refresh'

type AppointmentApiErrorBody = {
  code?: unknown
  message?: unknown
}

// Upcoming confirmed appointments for the signed-in public user (GET /users/appointments/).
export type UserAppointment = {
  appointment_id: number
  office_id: number
  service_id: number | null
  start_time: string | null
  end_time: string | null
  local_start_time: string | null
  local_end_time: string | null
  office: {
    office_name: string
    civic_address: string | null
  } | null
  service: {
    service_name: string
    external_service_name: string | null
  } | null
}

// Map known API rejection codes to clear citizen-facing copy. Falls back to the
// API message, then to the caller fallback (hold vs book).
function bookingErrorMessage(body: AppointmentApiErrorBody | null, fallback: string): string {
  const code = typeof body?.code === 'string' ? body.code : null
  if (code === 'MAX_NO_OF_APPOINTMENTS_REACHED') {
    return 'You already have an appointment on this date. Please modify or cancel your existing appointment before booking another.'
  }
  if (code === 'CONFLICT_APPOINTMENT') {
    return 'That time is no longer available. Please pick another time.'
  }
  const message = typeof body?.message === 'string' ? body.message.trim() : ''
  return message || fallback
}

async function throwBookingHttpError(res: Response, fallback: string): Promise<never> {
  const body = (await res.json().catch(() => null)) as AppointmentApiErrorBody | null
  throw new Error(bookingErrorMessage(body, fallback))
}

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
    await throwBookingHttpError(res, 'Unable to hold this time slot')
  }

  const created = (await res.json()) as { appointment?: { appointment_id?: number } }
  const appointmentId = created.appointment?.appointment_id
  if (!appointmentId) {
    throw new Error('Unable to hold this time slot')
  }

  return appointmentId
}

// Book the held timeslot. Deletes the draft server-side when appointment_draft_id is sent.
// Returns the confirmed appointment id (reference number for the confirmation page).
export async function createAppointment(body: {
  office_id: number
  service_id: number
  start_time: string
  end_time: string
  appointment_draft_id: number
}): Promise<number> {
  const token = await getAccessToken()

  const baseUrl = await getApiBaseUrl()
  const res = await fetch(`${baseUrl}/appointments/`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    await throwBookingHttpError(res, 'Unable to book this appointment')
  }

  const created = (await res.json()) as { appointment?: { appointment_id?: number } }
  const appointmentId = created.appointment?.appointment_id
  if (!appointmentId) {
    throw new Error('Unable to book this appointment')
  }

  return appointmentId
}

// Update an existing confirmed appointment (reschedule). Deletes the draft when
// appointment_draft_id is sent.
export async function updateAppointment(
  appointmentId: number,
  body: {
    office_id: number
    service_id: number
    start_time: string
    end_time: string
    appointment_draft_id: number
  },
): Promise<void> {
  const token = await getAccessToken()

  const baseUrl = await getApiBaseUrl()
  const res = await fetch(`${baseUrl}/appointments/${appointmentId}/`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    await throwBookingHttpError(res, 'Unable to update this appointment')
  }
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

// Future, not-checked-in appointments for the current public user.
export async function getUserAppointments(): Promise<UserAppointment[]> {
  const token = await getAccessToken()

  const baseUrl = await getApiBaseUrl()
  const res = await fetch(`${baseUrl}/users/appointments/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!res.ok) {
    throw new Error(`Failed to load appointments (${res.status})`)
  }

  const body = (await res.json()) as { appointments?: UserAppointment[] }
  return Array.isArray(body.appointments) ? body.appointments : []
}
