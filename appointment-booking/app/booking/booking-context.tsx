import { createContext, useContext, useState, type ReactNode } from 'react'

import type { Location } from '../api/locations'
import type { Service } from '../api/services'

// Booking-flow state shared across steps (in-memory; not page-refresh persistent).
// Mounted once in root so selection survives navigation between booking steps.
type BookingContextValue = {
  // Full service object so later steps can use id/name/bookable without re-fetching.
  selectedService: Service | null
  setSelectedService: (service: Service | null) => void
  // Full location object so later steps can use id/name/address without re-fetching.
  selectedLocation: Location | null
  setSelectedLocation: (location: Location | null) => void
}

const BookingContext = createContext<BookingContextValue | null>(null)

// Owns booking selections for the SPA session. Step pages remount; this provider does not.
export function BookingProvider({ children }: { children: ReactNode }) {
  const [selectedService, setSelectedService] = useState<Service | null>(null)
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null)

  return (
    <BookingContext.Provider
      value={{ selectedService, setSelectedService, selectedLocation, setSelectedLocation }}
    >
      {children}
    </BookingContext.Provider>
  )
}

// Used by booking step pages (services, locations; time/etc. later).
export function useBooking() {
  const value = useContext(BookingContext)
  if (!value) {
    throw new Error('useBooking must be used within BookingProvider')
  }
  return value
}
