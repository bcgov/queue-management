import type { UserAppointment } from '~/api/appointments'
import type { BookingConfirmation } from '~/booking/booking-store'

// local_* values are office wall clock without offset, e.g. 2026-09-25T14:30:00
export function parseLocalDateTime(value: string | null): { date: string; time: string } | null {
  if (!value) return null
  const match = /^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})/.exec(value)
  if (!match) return null
  return { date: match[1], time: match[2] }
}

export function serviceLabel(appointment: UserAppointment): string {
  return (
    appointment.service?.external_service_name?.trim() ||
    appointment.service?.service_name?.trim() ||
    'Service'
  )
}

export function toCancellationSnapshot(appointment: UserAppointment): BookingConfirmation | null {
  const start = parseLocalDateTime(appointment.local_start_time)
  const end = parseLocalDateTime(appointment.local_end_time)
  if (!start || !end) return null

  return {
    kind: 'cancelled',
    serviceName: serviceLabel(appointment),
    locationName: appointment.office?.office_name?.trim() || 'Location',
    locationAddress: appointment.office?.civic_address?.trim() || null,
    date: start.date,
    startTime: start.time,
    endTime: end.time,
  }
}
