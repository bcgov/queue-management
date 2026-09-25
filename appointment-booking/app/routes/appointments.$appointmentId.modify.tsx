// /appointments/:appointmentId/modify — seed booking for reschedule, then go to /datetime.
import { useEffect, useState } from 'react'
import { Button, InlineAlert, Text } from '@bcgov/design-system-react-components'
import { useNavigate, useParams } from 'react-router'

import { getUserAppointments, type UserAppointment } from '~/api/appointments'
import type { ServiceLocation } from '~/api/service-locations'
import type { Service } from '~/api/services'
import { useAuth } from '~/auth/auth-context'
import { addJsonToSession } from '~/auth/session'
import { SessionKeys } from '~/auth/session-keys'
import { useBooking } from '~/booking/booking-context'

export function meta() {
  return [{ title: 'Modify Appointment' }]
}

function serviceFromAppointment(appointment: UserAppointment): Service | null {
  if (appointment.service_id == null) return null
  return {
    id: appointment.service_id,
    name:
      appointment.service?.external_service_name?.trim() ||
      appointment.service?.service_name?.trim() ||
      'Service',
    onlineAvailability: 'SHOW',
    isOnlineBookable: true,
    isDlkt: false,
  }
}

function locationFromAppointment(appointment: UserAppointment): ServiceLocation {
  return {
    id: appointment.office_id,
    name: appointment.office?.office_name?.trim() || 'Location',
    address: appointment.office?.civic_address?.trim() || '',
    latitude: null,
    longitude: null,
    appointmentMessage: '',
    nextAppointmentDate: null,
    appointmentsDisabled: false,
    isBookable: true,
  }
}

export default function ModifyAppointmentPage() {
  const navigate = useNavigate()
  const appointmentId = Number(useParams().appointmentId)
  const { isReady: isAuthReady, isAuthenticated } = useAuth()
  const {
    isReady: isBookingReady,
    setSelectedService,
    setSelectedLocation,
    setSelectedSlot,
    setModifyingAppointmentId,
  } = useBooking()
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    if (!isAuthReady || !isBookingReady || isAuthenticated) return
    if (Number.isFinite(appointmentId) && appointmentId > 0) {
      addJsonToSession(SessionKeys.LoginReturnTo, `/appointments/${appointmentId}/modify`)
    }
    navigate('/login', { replace: true })
  }, [appointmentId, isAuthReady, isAuthenticated, isBookingReady, navigate])

  useEffect(() => {
    if (!isAuthReady || !isBookingReady || !isAuthenticated) return

    let cancelled = false
    // Defer setState so the effect body does not update React state synchronously.
    const startId = window.setTimeout(() => {
      if (cancelled) return

      if (!Number.isFinite(appointmentId) || appointmentId <= 0) {
        setFailed(true)
        return
      }

      getUserAppointments()
        .then((appointments) => {
          if (cancelled) return
          const appointment = appointments.find((row) => row.appointment_id === appointmentId)
          const service = appointment ? serviceFromAppointment(appointment) : null
          if (!appointment || !service) {
            setFailed(true)
            return
          }
          setSelectedSlot(null)
          setModifyingAppointmentId(appointment.appointment_id)
          setSelectedService(service)
          setSelectedLocation(locationFromAppointment(appointment))
          navigate('/datetime', { replace: true })
        })
        .catch(() => {
          if (!cancelled) setFailed(true)
        })
    }, 0)

    return () => {
      cancelled = true
      window.clearTimeout(startId)
    }
    // Setters omitted — new identities each render would re-seed.
  }, [appointmentId, isAuthReady, isAuthenticated, isBookingReady, navigate]) // eslint-disable-line react-hooks/exhaustive-deps

  if (!isAuthReady || !isBookingReady || !isAuthenticated) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading…</Text>
      </div>
    )
  }

  if (failed) {
    return (
      <div className="appointments-page">
        <InlineAlert variant="warning" title="Unable to modify appointment">
          This appointment could not be found, or it is no longer available to modify.
        </InlineAlert>
        <div className="booking-nav-row">
          <Button type="button" onPress={() => navigate('/appointments')}>
            My appointments
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="sign-in-panel" role="status" aria-live="polite">
      <Text>Loading…</Text>
    </div>
  )
}
