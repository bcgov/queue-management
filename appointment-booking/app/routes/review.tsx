// Booking step 5: review service, location, date/time, and confirmation email. No confirm yet.
import { useState } from 'react'
import { Button, InlineAlert, Text, TextField } from '@bcgov/design-system-react-components'
import { useNavigate } from 'react-router'

import { useAuth } from '~/auth/auth-context'
import { useBooking } from '~/booking/booking-context'
import { BookingBackRow } from '~/components/BookingBackRow'
import { BookingDetailCallout } from '~/components/BookingDetailCallout'
import { BookingStepProgress } from '~/components/BookingStepProgress'

const BOOKING_STEP = 5
const BOOKING_STEP_COUNT = 5
const BOOKING_STEP_HEADING = 'Review your appointment details before confirming.'

export function meta() {
  return [{ title: 'Review Appointment' }]
}

export default function ReviewPage() {
  const navigate = useNavigate()
  const { isReady: isAuthReady, isAuthenticated, session } = useAuth()
  const {
    isReady: isBookingReady,
    selectedService,
    selectedLocation,
    selectedSlot,
  } = useBooking()
  // null = still using signed-in email; string = user edited (including cleared).
  const [contactEmail, setContactEmail] = useState<string | null>(null)
  const confirmationEmail = contactEmail ?? session?.email?.trim() ?? ''

  const stepProgress = (
    <BookingStepProgress
      step={BOOKING_STEP}
      stepCount={BOOKING_STEP_COUNT}
      heading={BOOKING_STEP_HEADING}
    />
  )

  // Wait until sessionStorage restore finishes so we do not flash the wrong screen.
  if (!isAuthReady || !isBookingReady) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading booking…</Text>
      </div>
    )
  }

  if (!selectedService || !selectedLocation || !selectedSlot) {
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
          Please sign in before reviewing your appointment.
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
      <h1 className="sr-only">Review Appointment</h1>
      {stepProgress}

      <BookingDetailCallout
        selectedService={selectedService}
        selectedLocation={selectedLocation}
        selectedSlot={selectedSlot}
      />

      <div className="review-contact">
        <TextField
          label="Confirmation email"
          type="email"
          name="confirmationEmail"
          value={confirmationEmail}
          onChange={setContactEmail}
          // @ts-expect-error placeholder is supported by underlying react-aria TextField
          placeholder="name@example.com"
        />
        <p className="review-contact-hint">
          Appointment details will be sent to this email.
        </p>
      </div>

      <div className="booking-nav-row">
        <BookingBackRow onBack={() => navigate('/datetime')} />
      </div>
    </>
  )
}
