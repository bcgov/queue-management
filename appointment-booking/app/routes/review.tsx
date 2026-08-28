// Booking step 5: review service, location, date/time, and contact details. No confirm yet.
import { useEffect, useState } from 'react'
import { Button, InlineAlert, Text, TextField } from '@bcgov/design-system-react-components'
import { useNavigate } from 'react-router'

import { getCurrentUser, type PublicUser } from '~/api/users'
import { useAuth } from '~/auth/auth-context'
import { useBooking } from '~/booking/booking-context'
import { getContactValidation } from '~/booking/validate-contact'
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
  const { isReady: isBookingReady, selectedService, selectedLocation, selectedSlot } = useBooking()
  const [profile, setProfile] = useState<PublicUser | null>(null)
  // null = use profile/session default; string = user edited (including cleared).
  const [contactEmail, setContactEmail] = useState<string | null>(null)
  const [contactPhone, setContactPhone] = useState<string | null>(null)
  const [contactTouched, setContactTouched] = useState(false)

  useEffect(() => {
    if (!isAuthReady || !isAuthenticated) return

    let cancelled = false
    getCurrentUser()
      .then((user) => {
        if (!cancelled) setProfile(user)
      })
      .catch(() => {
        // Profile load failed; session email is still used when available.
      })

    return () => {
      cancelled = true
    }
  }, [isAuthReady, isAuthenticated])

  const email = contactEmail ?? (profile?.email?.trim() || session?.email?.trim() || '')
  const phone = contactPhone ?? (profile?.telephone?.trim() || '')
  const validation = getContactValidation(email, phone)

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

      <section className="review-contact" aria-labelledby="review-contact-heading">
        <h2 id="review-contact-heading">Contact details</h2>
        <p className="review-contact-intro">Provide your contact information for confirmation.</p>

        <TextField
          label="Email"
          type="email"
          name="email"
          value={email}
          onChange={(value) => {
            setContactEmail(value)
            setContactTouched(true)
          }}
          isInvalid={contactTouched && !!validation.emailError}
          errorMessage={contactTouched ? (validation.emailError ?? undefined) : undefined}
          // BC DS TextField only shows errorMessage when isInvalid is also set.
          // @ts-expect-error placeholder is supported by underlying react-aria TextField
          placeholder="name@example.com"
        />

        <TextField
          label="Phone number"
          type="tel"
          name="phone"
          value={phone}
          onChange={(value) => {
            setContactPhone(value)
            setContactTouched(true)
          }}
          isInvalid={contactTouched && !!validation.phoneError}
          errorMessage={contactTouched ? (validation.phoneError ?? undefined) : undefined}
          // @ts-expect-error placeholder is supported by underlying react-aria TextField
          placeholder="250-555-0100"
        />

        {contactTouched && validation.sectionError ? (
          // Shown when both fields are empty; individual field errors do not cover that case.
          <p className="review-contact-section-error" role="alert">
            {validation.sectionError}
          </p>
        ) : null}
      </section>

      <div className="booking-nav-row">
        <BookingBackRow onBack={() => navigate('/datetime')} />
      </div>
    </>
  )
}
