// Booking step 3: ask for BCSC sign-in, or show success after login.
import { useEffect, useState } from 'react'
import { Button, Callout, InlineAlert, Text } from '@bcgov/design-system-react-components'
import { useNavigate, useSearchParams } from 'react-router'

import { useAuth } from '~/auth/auth-context'
import { IdpHint } from '~/auth/session-keys'
import { useBooking } from '~/booking/booking-context'
import { BookingBackRow } from '../components/BookingBackRow'
import { BookingContinueRow } from '../components/BookingContinueRow'
import { BookingStepProgress } from '../components/BookingStepProgress'
import { getBCServicesCardUrl } from '../runtime-config'

const BOOKING_STEP = 3
const BOOKING_STEP_COUNT = 5

export function meta() {
  return [{ title: 'Login' }]
}

export default function LoginPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { isReady: isAuthReady, isAuthenticated, session } = useAuth()
  const { isReady: isBookingReady, selectedService, selectedLocation } = useBooking()
  const hasSelections = !!selectedService && !!selectedLocation
  const [bcscUrl, setBcscUrl] = useState('')
  const idpError = searchParams.get('error') === 'idp'

  useEffect(() => {
    void getBCServicesCardUrl().then(setBcscUrl)
  }, [])

  // Wait until sessionStorage restore finishes so we do not flash the wrong screen.
  if (!isAuthReady || !isBookingReady) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading booking…</Text>
      </div>
    )
  }

  const heading = isAuthenticated
    ? 'You have successfully signed in.'
    : 'Sign in to continue your booking.'
  const signedInAs = session?.userFullName?.trim() || 'BC Services Card user'

  if (!hasSelections) {
    return (
      <>
        <BookingStepProgress step={BOOKING_STEP} stepCount={BOOKING_STEP_COUNT} heading={heading} />

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
        <BookingStepProgress step={BOOKING_STEP} stepCount={BOOKING_STEP_COUNT} heading={heading} />

        {idpError ? (
          <div className="login-alert">
            <InlineAlert variant="danger" title="BC Services Card required">
              This booking app only accepts BC Services Card sign-in. Please sign in again with BC
              Services Card. Use a private browser window if you were signed in to Keycloak as IDIR.
            </InlineAlert>
          </div>
        ) : null}

        <div className="sign-in-panel">
          <Text>To continue your appointment booking, please sign in using BC Services Card.</Text>

          <div className="sign-in-actions">
            <Button type="button" onPress={() => navigate(`/signin/${IdpHint.BCSC}`)}>
              Login with BC Services Card
            </Button>

            {bcscUrl ? (
              <a
                className="sign-in-learn-more"
                href={bcscUrl}
                target="_blank"
                rel="noopener noreferrer"
              >
                Learn more about BC Services Card app
              </a>
            ) : null}
          </div>
        </div>

        <div className="booking-nav-row">
          <BookingBackRow onBack={() => navigate('/service-locations')} />
        </div>
      </>
    )
  }

  return (
    <>
      <BookingStepProgress step={BOOKING_STEP} stepCount={BOOKING_STEP_COUNT} heading={heading} />

      <div className="login-alert">
        <InlineAlert variant="success" title="Signed in">
          You are successfully signed in as {signedInAs}.
        </InlineAlert>
      </div>

      <Callout variant="lightBlue">
        <div className="booking-detail-callout-content">
          <Text>
            Selected service - <strong>{selectedService.name}</strong>
            <br />
            Appointment Location - <strong>{selectedLocation.name}</strong>
            {selectedLocation.address ? (
              <>
                <br />
                Address - <strong>{selectedLocation.address}</strong>
              </>
            ) : null}
          </Text>
        </div>
      </Callout>

      <p className="login-next-copy">
        Continue to the next step to choose a date and time for your appointment.
      </p>

      <div className="booking-nav-row">
        <BookingBackRow onBack={() => navigate('/service-locations')} />
        {/* Date/time step is not built yet — Continue stays disabled. */}
        <BookingContinueRow isDisabled />
      </div>
    </>
  )
}
