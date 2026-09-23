// Shared service, location, appointment time, and draft hold across booking steps.
// Also saved in the browser so choices survive the sign-in redirect.
import { useContext, useEffect, useState, type ReactNode } from 'react'

import { deleteDraftAppointment } from '../api/appointments'
import type { ServiceLocation } from '../api/service-locations'
import type { Service } from '../api/services'
import { addJsonToSession, getJsonFromSession, removeFromSession } from '../auth/session'
import { SessionKeys } from '../auth/session-keys'
import { BookingContext, type BookingSlot } from './booking-store'

function persistJson(key: string, value: unknown) {
  if (value) {
    addJsonToSession(key, value)
  } else {
    removeFromSession(key)
  }
}

export function BookingProvider({ children }: { children: ReactNode }) {
  const [isReady, setIsReady] = useState(false)
  const [selectedService, setSelectedServiceState] = useState<Service | null>(null)
  const [selectedLocation, setSelectedLocationState] = useState<ServiceLocation | null>(null)
  const [selectedSlot, setSelectedSlotState] = useState<BookingSlot | null>(null)

  useEffect(() => {
    // Restore saved choices after the page first loads in the browser.
    const id = window.setTimeout(() => {
      setSelectedServiceState(getJsonFromSession<Service>(SessionKeys.BookingSelectedService))
      setSelectedLocationState(
        getJsonFromSession<ServiceLocation>(SessionKeys.BookingSelectedLocation),
      )
      const savedSlot = getJsonFromSession<BookingSlot>(SessionKeys.BookingSelectedSlot)
      // Slot is only valid when it still carries a draft id (source of truth for the hold).
      setSelectedSlotState(savedSlot?.draftAppointmentId ? savedSlot : null)
      setIsReady(true)
    }, 0)
    return () => window.clearTimeout(id)
  }, [])

  // Clearing the time also releases the held slot. Expired drafts are already gone server-side.
  function setSelectedSlot(slot: BookingSlot | null) {
    if (!slot && selectedSlot?.draftAppointmentId != null) {
      void deleteDraftAppointment(selectedSlot.draftAppointmentId).catch(() => {})
    }
    setSelectedSlotState(slot)
    persistJson(SessionKeys.BookingSelectedSlot, slot)
  }

  // Changing service or office drops the time already chosen; refreshing the same one keeps it.
  function setSelectedService(service: Service | null) {
    if (service?.id !== selectedService?.id) {
      setSelectedSlot(null)
    }
    setSelectedServiceState(service)
    persistJson(SessionKeys.BookingSelectedService, service)
  }

  function setSelectedLocation(location: ServiceLocation | null) {
    if (location?.id !== selectedLocation?.id) {
      setSelectedSlot(null)
    }
    setSelectedLocationState(location)
    persistJson(SessionKeys.BookingSelectedLocation, location)
  }

  // After POST /appointments/ the draft is already gone — clear local selection without DELETE.
  function clearBookingAfterConfirm() {
    setSelectedSlotState(null)
    setSelectedServiceState(null)
    setSelectedLocationState(null)
    removeFromSession(SessionKeys.BookingSelectedSlot)
    removeFromSession(SessionKeys.BookingSelectedService)
    removeFromSession(SessionKeys.BookingSelectedLocation)
  }

  return (
    <BookingContext.Provider
      value={{
        isReady,
        selectedService,
        setSelectedService,
        selectedLocation,
        setSelectedLocation,
        selectedSlot,
        setSelectedSlot,
        clearBookingAfterConfirm,
      }}
    >
      {children}
    </BookingContext.Provider>
  )
}

export function useBooking() {
  const value = useContext(BookingContext)
  if (!value) {
    throw new Error('useBooking must be used within BookingProvider')
  }
  return value
}
