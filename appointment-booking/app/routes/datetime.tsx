import { useEffect, useState } from 'react'
import { Button, Calendar, InlineAlert, Select, Text } from '@bcgov/design-system-react-components'
import { parseDate } from '@internationalized/date'
import { useNavigate } from 'react-router'

import { createDraftAppointment, deleteDraftAppointment } from '~/api/appointments'
import { getAvailableTimeSlots, type AvailableTimeSlots } from '~/api/timeslots'
import { useAuth } from '~/auth/auth-context'
import { useBooking } from '~/booking/booking-context'
import type { BookingSlot } from '~/booking/booking-store'
import { formatDate, formatTimeRange, officeWallTimeToIso } from '~/booking/format-slot'
import { BookingBackRow } from '~/components/BookingBackRow'
import { BookingContinueRow } from '~/components/BookingContinueRow'
import { BookingDetailCallout } from '~/components/BookingDetailCallout'
import { BookingStepProgress } from '~/components/BookingStepProgress'

const BOOKING_STEP = 4
const BOOKING_STEP_COUNT = 5
const BOOKING_STEP_HEADING = 'Select a date and time for your appointment.'

function slotValue(startTime: string, endTime: string) {
  return `${startTime}|${endTime}`
}

export function meta() {
  return [{ title: 'Select Date and Time' }]
}

export default function DateTimePage() {
  const navigate = useNavigate()
  const { isReady: isAuthReady, isAuthenticated } = useAuth()
  const {
    isReady: isBookingReady,
    selectedService,
    selectedLocation,
    selectedSlot,
    setSelectedSlot,
    draftAppointmentId,
    setDraftAppointmentId,
  } = useBooking()
  const [timeSlots, setTimeSlots] = useState<AvailableTimeSlots>({})
  const [selectedDay, setSelectedDay] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [isHoldingSlot, setIsHoldingSlot] = useState(false)
  const [holdError, setHoldError] = useState<string | null>(null)

  useEffect(() => {
    if (
      !isAuthReady ||
      !isBookingReady ||
      !isAuthenticated ||
      !selectedService ||
      !selectedLocation
    ) {
      return
    }

    let cancelled = false

    // Wait a moment before loading so we can clear any old error and show loading again.
    const startId = window.setTimeout(() => {
      if (cancelled) {
        return
      }

      setIsLoading(true)
      setLoadError(false)

      getAvailableTimeSlots(selectedLocation.id, selectedService.id)
        .then((loaded) => {
          if (!cancelled) setTimeSlots(loaded)
        })
        .catch(() => {
          if (!cancelled) {
            setTimeSlots({})
            setLoadError(true)
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
  }, [isAuthReady, isBookingReady, isAuthenticated, selectedLocation, selectedService])

  // Create (or replace) a draft hold as soon as a timeslot is chosen.
  async function holdSelectedSlot(slot: BookingSlot) {
    if (!selectedService || !selectedLocation) return

    setHoldError(null)
    setSelectedSlot(slot)
    setIsHoldingSlot(true)

    const timezoneName = selectedLocation.timezoneName

    try {
      if (!timezoneName) {
        throw new Error('Missing office timezone. Please go back and select the location again.')
      }

      // Release the previous hold first, so re-picking the same time is not a conflict.
      if (draftAppointmentId != null) {
        try {
          await deleteDraftAppointment(draftAppointmentId)
        } catch {
          // Expired or already deleted.
        }
        setDraftAppointmentId(null)
      }

      const draftId = await createDraftAppointment({
        office_id: selectedLocation.id,
        service_id: selectedService.id,
        start_time: officeWallTimeToIso(slot.date, slot.startTime, timezoneName),
        end_time: officeWallTimeToIso(slot.date, slot.endTime, timezoneName),
      })
      setDraftAppointmentId(draftId)
    } catch (err) {
      setSelectedSlot(null)
      setDraftAppointmentId(null)
      setHoldError(
        err instanceof Error
          ? err.message
          : 'Unable to hold this time slot. Please pick another time.',
      )
    } finally {
      setIsHoldingSlot(false)
    }
  }

  const availableDates = Object.keys(timeSlots).sort()
  // Prefer clicked day, then saved slot day, then next available date.
  const activeDay =
    selectedDay ??
    (selectedSlot && timeSlots[selectedSlot.date] ? selectedSlot.date : null) ??
    availableDates[0] ??
    null
  const activeDaySlots = activeDay ? (timeSlots[activeDay] ?? []) : []
  const selectedSlotValue =
    selectedSlot?.date === activeDay ? slotValue(selectedSlot.startTime, selectedSlot.endTime) : ''
  const nextDate = availableDates[0]
  const nextAppointment =
    nextDate && timeSlots[nextDate]?.[0] ? { date: nextDate, ...timeSlots[nextDate][0] } : null

  const stepProgress = (
    <BookingStepProgress
      step={BOOKING_STEP}
      stepCount={BOOKING_STEP_COUNT}
      heading={BOOKING_STEP_HEADING}
    />
  )

  if (!isAuthReady || !isBookingReady) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading booking…</Text>
      </div>
    )
  }

  if (!selectedService || !selectedLocation) {
    return (
      <>
        {stepProgress}
        <InlineAlert variant="warning" title="Start your booking">
          Please go back to the services page and start by selecting a service, then a location.
        </InlineAlert>
        <div className="booking-nav-row">
          <Button type="button" onPress={() => navigate('/services')}>
            Go to services
          </Button>
        </div>
      </>
    )
  }

  if (!isAuthenticated) {
    return (
      <>
        {stepProgress}
        <InlineAlert variant="warning" title="Sign in to continue">
          Please sign in before selecting a date and time for your appointment.
        </InlineAlert>
        <div className="booking-nav-row">
          <Button type="button" onPress={() => navigate('/login')}>
            Go to login
          </Button>
        </div>
      </>
    )
  }

  return (
    <>
      <h1 className="sr-only">Select Date and Time</h1>
      {stepProgress}

      <BookingDetailCallout
        selectedService={selectedService}
        selectedLocation={selectedLocation}
        selectedSlot={selectedSlot}
      />

      {holdError ? (
        <div className="datetime-status">
          <InlineAlert variant="danger" title="Time slot unavailable">
            {holdError}
          </InlineAlert>
        </div>
      ) : null}

      {isLoading ? (
        <div className="datetime-status" role="status" aria-live="polite">
          <Text>Loading available dates and times…</Text>
        </div>
      ) : loadError ? (
        <div className="datetime-status">
          <InlineAlert variant="danger" title="Unable to load available times">
            Please try again.
          </InlineAlert>
        </div>
      ) : availableDates.length === 0 ? (
        <div className="datetime-status">
          <InlineAlert variant="info" title="No appointments available">
            There are no available dates or times for this service and location.
          </InlineAlert>
        </div>
      ) : (
        <div className="datetime-selection-panel">
          <div className="datetime-selection">
            <section aria-labelledby="datetime-date-heading">
              <h2 id="datetime-date-heading">Select Date</h2>
              <Calendar
                aria-label="Available appointment dates"
                value={activeDay ? parseDate(activeDay) : null}
                minValue={parseDate(availableDates[0])}
                maxValue={parseDate(availableDates[availableDates.length - 1])}
                defaultFocusedValue={parseDate(availableDates[0])}
                isDateUnavailable={(date) => !timeSlots[date.toString()]}
                isDisabled={isHoldingSlot}
                onChange={(date) => {
                  const nextDay = date.toString()
                  if (nextDay !== activeDay) {
                    setHoldError(null)
                    setSelectedSlot(null)
                  }
                  setSelectedDay(nextDay)
                }}
              />
              <ul className="datetime-calendar-legend">
                <li>
                  <span className="datetime-calendar-legend-unavailable">Red line</span> — no
                  appointments available
                </li>
                <li>
                  <span className="datetime-calendar-legend-disabled">Greyed out</span> — outside
                  the booking window or not selectable
                </li>
              </ul>
            </section>

            <section aria-labelledby="datetime-time-heading">
              <h2 id="datetime-time-heading">Select Time</h2>
              {nextAppointment ? (
                <div className="datetime-time-panel">
                  <p className="datetime-selected-day" aria-live="polite">
                    {formatDate(nextAppointment.date)}
                    <br />
                    {formatTimeRange(nextAppointment.startTime, nextAppointment.endTime)}
                  </p>
                  <div className="datetime-next-available-action">
                    <Button
                      type="button"
                      variant="primary"
                      size="medium"
                      isDisabled={isHoldingSlot}
                      onPress={() => {
                        setSelectedDay(nextAppointment.date)
                        void holdSelectedSlot(nextAppointment)
                      }}
                    >
                      Select next available appointment
                    </Button>
                    <p className="datetime-next-available-or" aria-hidden="true">
                      OR
                    </p>
                  </div>
                </div>
              ) : null}
              {activeDay ? (
                <div className="datetime-time-panel">
                  <p className="datetime-selected-day" aria-live="polite">
                    {formatDate(activeDay)}
                    {selectedSlot?.date === activeDay ? (
                      <>
                        <br />
                        {formatTimeRange(selectedSlot.startTime, selectedSlot.endTime)}
                      </>
                    ) : null}
                  </p>
                  <div className="datetime-time-slots">
                    <Select
                      aria-label={`Available times for ${formatDate(activeDay)}`}
                      placeholder="Select a Time Slot"
                      selectedKey={selectedSlotValue || null}
                      isDisabled={isHoldingSlot}
                      items={activeDaySlots.map((slot) => ({
                        id: slotValue(slot.startTime, slot.endTime),
                        label: formatTimeRange(slot.startTime, slot.endTime),
                      }))}
                      onSelectionChange={(value) => {
                        const slot = activeDaySlots.find(
                          ({ startTime, endTime }) => slotValue(startTime, endTime) === value,
                        )
                        if (slot) void holdSelectedSlot({ date: activeDay, ...slot })
                      }}
                    />
                  </div>
                </div>
              ) : null}
            </section>
          </div>
        </div>
      )}

      <div className="booking-nav-row">
        <BookingBackRow onBack={() => navigate('/login')} />
        <BookingContinueRow
          label="Review"
          isDisabled={!selectedSlot || !draftAppointmentId || isHoldingSlot}
          onContinue={() => navigate('/review')}
        />
      </div>
    </>
  )
}
