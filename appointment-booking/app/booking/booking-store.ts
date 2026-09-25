import { createContext } from 'react'

import type { ServiceLocation } from '../api/service-locations'
import type { Service } from '../api/services'

// The chosen appointment date and time. Date is YYYY-MM-DD; times are HH:MM office-local.
// draftAppointmentId is required: a held slot always has a server draft.
export type BookingSlot = {
  date: string
  startTime: string
  endTime: string
  draftAppointmentId: number
}

// Snapshot shown on /confirmation after a successful book.
export type BookingConfirmation = {
  bookedByName: string
  serviceName: string
  locationName: string
  locationAddress: string | null
  date: string
  startTime: string
  endTime: string
}

export type BookingContextValue = {
  isReady: boolean
  selectedService: Service | null
  setSelectedService: (service: Service | null) => void
  selectedLocation: ServiceLocation | null
  setSelectedLocation: (location: ServiceLocation | null) => void
  selectedSlot: BookingSlot | null
  setSelectedSlot: (slot: BookingSlot | null) => void
  // When set, review confirms with PUT instead of POST.
  modifyingAppointmentId: number | null
  setModifyingAppointmentId: (appointmentId: number | null) => void
  // Clears service/location/slot without releasing a draft (draft already consumed on confirm).
  clearBookingAfterConfirm: () => void
}

// Isolated from component exports so Vite/Fast Refresh cannot duplicate this context.
export const BookingContext = createContext<BookingContextValue | null>(null)
