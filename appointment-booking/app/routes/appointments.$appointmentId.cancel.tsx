// /appointments/:appointmentId/cancel — confirm before deleting a confirmed appointment.
import { useEffect, useState } from 'react'
import { Button, InlineAlert, Text } from '@bcgov/design-system-react-components'
import { useNavigate, useParams } from 'react-router'

import { deleteAppointment, getUserAppointments, type UserAppointment } from '~/api/appointments'
import { useAuth } from '~/auth/auth-context'
import { addJsonToSession } from '~/auth/session'
import { SessionKeys } from '~/auth/session-keys'
import { toCancellationSnapshot } from '~/booking/appointment-display'
import { AppointmentSummaryCallout } from '~/components/AppointmentSummaryCallout'

export function meta() {
  return [{ title: 'Cancel Appointment' }]
}

export default function CancelAppointmentPage() {
  const navigate = useNavigate()
  const appointmentId = Number(useParams().appointmentId)
  const { isReady: isAuthReady, isAuthenticated } = useAuth()
  const [appointment, setAppointment] = useState<UserAppointment | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [loadFailed, setLoadFailed] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [cancelError, setCancelError] = useState(false)

  useEffect(() => {
    if (!isAuthReady || isAuthenticated) return
    if (Number.isFinite(appointmentId) && appointmentId > 0) {
      addJsonToSession(SessionKeys.LoginReturnTo, `/appointments/${appointmentId}/cancel`)
    }
    navigate('/login', { replace: true })
  }, [appointmentId, isAuthReady, isAuthenticated, navigate])

  useEffect(() => {
    if (!isAuthReady || !isAuthenticated) return

    let cancelled = false
    // Defer setState so the effect body does not update React state synchronously.
    const startId = window.setTimeout(() => {
      if (cancelled) return

      setIsLoading(true)
      setLoadFailed(false)

      if (!Number.isFinite(appointmentId) || appointmentId <= 0) {
        setAppointment(null)
        setLoadFailed(true)
        setIsLoading(false)
        return
      }

      getUserAppointments()
        .then((appointments) => {
          if (cancelled) return
          const found = appointments.find((row) => row.appointment_id === appointmentId) || null
          setAppointment(found)
          setLoadFailed(!found)
        })
        .catch(() => {
          if (!cancelled) {
            setAppointment(null)
            setLoadFailed(true)
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
  }, [appointmentId, isAuthReady, isAuthenticated])

  async function handleConfirmCancel() {
    if (!appointment || isSubmitting) return

    const snapshot = toCancellationSnapshot(appointment)
    if (!snapshot) {
      setCancelError(true)
      return
    }

    setIsSubmitting(true)
    setCancelError(false)

    try {
      await deleteAppointment(appointment.appointment_id)
      addJsonToSession(SessionKeys.BookingConfirmation, snapshot)
      navigate('/confirmation', { replace: true })
    } catch {
      setCancelError(true)
      setIsSubmitting(false)
    }
  }

  if (!isAuthReady || !isAuthenticated || isLoading) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading…</Text>
      </div>
    )
  }

  if (loadFailed || !appointment) {
    return (
      <div className="appointments-page">
        <InlineAlert variant="warning" title="Unable to cancel appointment">
          This appointment could not be found, or it is no longer available to cancel.
        </InlineAlert>
        <div className="booking-nav-row">
          <Button type="button" onPress={() => navigate('/appointments')}>
            My appointments
          </Button>
        </div>
      </div>
    )
  }

  const snapshot = toCancellationSnapshot(appointment)

  return (
    <div className="appointments-page">
      <h1>Cancel appointment</h1>
      <p className="appointments-modify-note">
        Confirm that you want to cancel this appointment. The time slot will become available for
        others to book.
      </p>

      {snapshot ? (
        <AppointmentSummaryCallout {...snapshot} />
      ) : (
        <InlineAlert variant="danger" title="Unable to show appointment details">
          Please go back and try again.
        </InlineAlert>
      )}

      {cancelError ? (
        <InlineAlert variant="danger" title="Unable to cancel appointment">
          Please try again.
        </InlineAlert>
      ) : null}

      <div className="booking-nav-row">
        <Button
          type="button"
          variant="secondary"
          isDisabled={isSubmitting}
          onPress={() => navigate('/appointments')}
        >
          Keep appointment
        </Button>
        <Button
          type="button"
          variant="primary"
          danger
          isDisabled={isSubmitting || !snapshot}
          onPress={() => {
            void handleConfirmCancel()
          }}
        >
          {isSubmitting ? 'Cancelling…' : 'Confirm cancel'}
        </Button>
      </div>
    </div>
  )
}
