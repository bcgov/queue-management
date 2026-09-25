// Read-only list of the user's upcoming appointments.
import { useEffect, useState } from 'react'
import { Button, InlineAlert, Text } from '@bcgov/design-system-react-components'
import { useNavigate } from 'react-router'

import { getUserAppointments, type UserAppointment } from '~/api/appointments'
import { useAuth } from '~/auth/auth-context'
import { formatDate, formatTimeRange } from '~/booking/format-slot'

export function meta() {
  return [{ title: 'My Appointments' }]
}

// local_* values are office wall clock without offset, e.g. 2026-09-25T14:30:00
function parseLocalDateTime(value: string | null): { date: string; time: string } | null {
  if (!value) return null
  const match = /^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})/.exec(value)
  if (!match) return null
  return { date: match[1], time: match[2] }
}

function serviceLabel(appointment: UserAppointment): string {
  return (
    appointment.service?.external_service_name?.trim() ||
    appointment.service?.service_name?.trim() ||
    'Service'
  )
}

export default function AppointmentsPage() {
  const navigate = useNavigate()
  const { isReady: isAuthReady, isAuthenticated } = useAuth()
  const [appointments, setAppointments] = useState<UserAppointment[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)

  useEffect(() => {
    if (!isAuthReady || !isAuthenticated) return

    let cancelled = false

    // Defer setState so the effect body does not update React state synchronously.
    const startId = window.setTimeout(() => {
      if (cancelled) return

      setIsLoading(true)
      setLoadError(false)

      getUserAppointments()
        .then((loaded) => {
          if (cancelled) return
          const sorted = [...loaded].sort((a, b) => {
            const aKey = a.local_start_time || a.start_time || ''
            const bKey = b.local_start_time || b.start_time || ''
            return aKey.localeCompare(bKey)
          })
          setAppointments(sorted)
        })
        .catch(() => {
          if (!cancelled) {
            setAppointments([])
            setLoadError(true)
          }
        })
        .finally(() => {
          if (!cancelled) setIsLoading(false)
        })
    }, 0)

    return () => {
      cancelled = true
      window.clearTimeout(startId)
    }
  }, [isAuthReady, isAuthenticated])

  if (!isAuthReady) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading…</Text>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="appointments-page">
        <InlineAlert variant="warning" title="Login to continue">
          Please login to view your appointments.
        </InlineAlert>
      </div>
    )
  }

  return (
    <div className="appointments-page">
      <h1>My Appointments</h1>

      {isLoading ? (
        <div role="status" aria-live="polite">
          <Text>Loading appointments…</Text>
        </div>
      ) : null}

      {!isLoading && loadError ? (
        <InlineAlert variant="danger" title="Unable to load appointments">
          Please try again.
        </InlineAlert>
      ) : null}

      {!isLoading && !loadError && appointments.length === 0 ? (
        <InlineAlert variant="info" title="No upcoming appointments" />
      ) : null}

      {!isLoading && !loadError && appointments.length > 0 ? (
        <ul className="appointments-list">
          {appointments.map((appointment) => {
            const start = parseLocalDateTime(appointment.local_start_time)
            const end = parseLocalDateTime(appointment.local_end_time)
            const location = appointment.office?.office_name?.trim() || 'Location'
            const address = appointment.office?.civic_address?.trim()

            return (
              <li key={appointment.appointment_id} className="appointments-row">
                <div className="appointments-row-main">
                  <p className="appointments-row-service">{serviceLabel(appointment)}</p>
                  <p className="appointments-row-location">
                    {location}
                    {address ? ` · ${address}` : ''}
                  </p>
                </div>
                <div className="appointments-row-when">
                  {start ? <p className="appointments-row-date">{formatDate(start.date)}</p> : null}
                  {start && end ? (
                    <p className="appointments-row-time">{formatTimeRange(start.time, end.time)}</p>
                  ) : null}
                </div>
              </li>
            )
          })}
        </ul>
      ) : null}

      {!isLoading ? (
        <div className="appointments-footer">
          <Button type="button" variant="primary" onPress={() => navigate('/services')}>
            Book a new appointment
          </Button>
        </div>
      ) : null}
    </div>
  )
}
