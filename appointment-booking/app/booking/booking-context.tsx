// Shared service + location selection across booking steps.
// Also saved to sessionStorage so selections survive the BCSC redirect.
import { useContext, useEffect, useState, type ReactNode } from 'react'

import type { Location } from '../api/locations'
import type { Service } from '../api/services'
import { addJsonToSession, getJsonFromSession, removeFromSession } from '../auth/session'
import { SessionKeys } from '../auth/session-keys'
import { BookingContext } from './booking-store'

export function BookingProvider({ children }: { children: ReactNode }) {
  const [isReady, setIsReady] = useState(false)
  const [selectedService, setSelectedServiceState] = useState<Service | null>(null)
  const [selectedLocation, setSelectedLocationState] = useState<Location | null>(null)

  useEffect(() => {
    // sessionStorage is browser-only, so restore it after the initial render.
    const id = window.setTimeout(() => {
      setSelectedServiceState(getJsonFromSession<Service>(SessionKeys.BookingSelectedService))
      setSelectedLocationState(getJsonFromSession<Location>(SessionKeys.BookingSelectedLocation))
      setIsReady(true)
    }, 0)
    return () => window.clearTimeout(id)
  }, [])

  function setSelectedService(service: Service | null) {
    setSelectedServiceState(service)
    if (service) {
      addJsonToSession(SessionKeys.BookingSelectedService, service)
    } else {
      removeFromSession(SessionKeys.BookingSelectedService)
    }
  }

  function setSelectedLocation(location: Location | null) {
    setSelectedLocationState(location)
    if (location) {
      addJsonToSession(SessionKeys.BookingSelectedLocation, location)
    } else {
      removeFromSession(SessionKeys.BookingSelectedLocation)
    }
  }

  return (
    <BookingContext.Provider
      value={{
        isReady,
        selectedService,
        setSelectedService,
        selectedLocation,
        setSelectedLocation,
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
