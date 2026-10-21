import { getApiBaseUrl } from '../runtime-config'

// Start and end time shown in the booking UI.
export type TimeSlot = {
  startTime: string
  endTime: string
}

// Available times grouped by date (YYYY-MM-DD).
export type AvailableTimeSlots = Record<string, TimeSlot[]>

// One slot as returned by the office slots API.
type ApiTimeSlot = {
  start_time: string
  end_time: string
  no_of_slots: number
}

// The API groups slots by MM/DD/YYYY dates.
type ApiAvailableTimeSlots = Record<string, ApiTimeSlot[]>

// Convert MM/DD/YYYY to YYYY-MM-DD. Skip bad dates instead of failing the whole load.
function toIsoDate(date: string): string | null {
  const [month, day, year] = date.split('/')
  if (!month || !day || !year) {
    return null
  }
  return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
}

// Load bookable times for the selected office and service.
// Throws when the request fails so the page can show an error, not "no times available".
export async function getAvailableTimeSlots(
  officeId: number,
  serviceId: number,
): Promise<AvailableTimeSlots> {
  const url = `${await getApiBaseUrl()}/offices/${officeId}/slots/?service_id=${serviceId}`

  let body: ApiAvailableTimeSlots
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error('Failed to load time slots')
    }
    body = (await response.json()) as ApiAvailableTimeSlots
  } catch {
    throw new Error('Failed to load time slots')
  }

  if (!body || typeof body !== 'object') {
    throw new Error('Failed to load time slots')
  }

  const availableTimeSlots: AvailableTimeSlots = {}

  for (const [date, slots] of Object.entries(body)) {
    const isoDate = toIsoDate(date)
    if (!isoDate) {
      continue
    }

    // Skip slots with no openings left, in case the API includes them.
    const availableSlots = slots
      .filter((slot) => slot.no_of_slots > 0)
      .map((slot) => ({
        startTime: slot.start_time,
        endTime: slot.end_time,
      }))

    // Leave empty days out so the calendar can mark them unavailable.
    if (availableSlots.length > 0) {
      availableTimeSlots[isoDate] = availableSlots
    }
  }

  return availableTimeSlots
}
