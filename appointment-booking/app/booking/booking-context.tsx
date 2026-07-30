// Shared service, location, and appointment time across booking steps.
// Also saved in the browser so choices survive the sign-in redirect.
import { useContext, useEffect, useState, type ReactNode } from 'react'

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
      setSelectedSlotState(getJsonFromSession<BookingSlot>(SessionKeys.BookingSelectedSlot))
      setIsReady(true)
    }, 0)
    return () => window.clearTimeout(id)
  }, [])

  // Changing service or location clears any time already chosen.
  function setSelectedService(service: Service | null) {
    setSelectedServiceState(service)
    setSelectedSlot(null)
    persistJson(SessionKeys.BookingSelectedService, service)
  }

  function setSelectedLocation(location: ServiceLocation | null) {
    setSelectedLocationState(location)
    setSelectedSlot(null)
    persistJson(SessionKeys.BookingSelectedLocation, location)
  }

  function setSelectedSlot(slot: BookingSlot | null) {
    setSelectedSlotState(slot)
    persistJson(SessionKeys.BookingSelectedSlot, slot)
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
