import { createContext } from 'react'

import type { Location } from '../api/locations'
import type { Service } from '../api/services'

// The chosen appointment date and time. Date is YYYY-MM-DD; times are HH:MM.
export type BookingSlot = {
  date: string
  startTime: string
  endTime: string
}

export type BookingContextValue = {
  isReady: boolean
  selectedService: Service | null
  setSelectedService: (service: Service | null) => void
  selectedLocation: Location | null
  setSelectedLocation: (location: Location | null) => void
  selectedSlot: BookingSlot | null
  setSelectedSlot: (slot: BookingSlot | null) => void
}

// Isolated from component exports so Vite/Fast Refresh cannot duplicate this context.
export const BookingContext = createContext<BookingContextValue | null>(null)
