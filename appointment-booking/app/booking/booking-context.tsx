import { createContext, useContext, useState, type ReactNode } from 'react'

import type { Service } from '../api/services'

// Booking-flow state shared across steps (in-memory; not page-refresh persistent).
// Mounted once in root so selection survives navigation between booking steps.
type BookingContextValue = {
  // Full service object so later steps can use id/name/bookable without re-fetching.
  selectedService: Service | null
  setSelectedService: (service: Service | null) => void
}

const BookingContext = createContext<BookingContextValue | null>(null)

// Owns booking selections for the SPA session. Step pages remount; this provider does not.
export function BookingProvider({ children }: { children: ReactNode }) {
  const [selectedService, setSelectedService] = useState<Service | null>(null)

  return (
    <BookingContext.Provider value={{ selectedService, setSelectedService }}>
      {children}
    </BookingContext.Provider>
  )
}

// Used by booking step pages (services now; location/time/etc. later).
export function useBooking() {
  const value = useContext(BookingContext)
  if (!value) {
    throw new Error('useBooking must be used within BookingProvider')
  }
  return value
}
