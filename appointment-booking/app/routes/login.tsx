// Login page: booking step 3, or header Login when there is no booking in progress.
import { useEffect } from 'react'
import { Button, InlineAlert, Text } from '@bcgov/design-system-react-components'
import { faArrowUpRightFromSquare } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useNavigate, useSearchParams } from 'react-router'

import { useAuth } from '~/auth/auth-context'
import { getJsonFromSession, removeFromSession } from '~/auth/session'
import { IdpHint, SessionKeys } from '~/auth/session-keys'
import { useBooking } from '~/booking/booking-context'
import { BookingBackRow } from '~/components/BookingBackRow'
import { BookingContinueRow } from '~/components/BookingContinueRow'
import { BookingDetailCallout } from '~/components/BookingDetailCallout'
import { BookingStepProgress } from '~/components/BookingStepProgress'

const BOOKING_STEP = 3
const BOOKING_STEP_COUNT = 5

export function meta() {
  return [{ title: 'Login' }]
}

function SignInMethods() {
  const navigate = useNavigate()

  return (
    <div className="sign-in-actions">
      <Button type="button" onPress={() => navigate(`/signin/${IdpHint.OTP}`, { replace: true })}>
        Login with Email OTP
      </Button>
      <a
        className="sign-in-learn-more"
        href="https://www2.gov.bc.ca/gov/content/governments/services-for-government/information-management-technology/id-services/one-time-pc"
        target="_blank"
        rel="noopener noreferrer"
      >
        <FontAwesomeIcon
          icon={faArrowUpRightFromSquare}
          className="sign-in-external-icon"
          aria-hidden="true"
        />
        <span>Learn more about one-time passcode</span>
      </a>

      <div className="sign-in-or" role="separator" aria-label="or">
        OR
      </div>

      <Button type="button" onPress={() => navigate(`/signin/${IdpHint.BCSC}`, { replace: true })}>
        Login with BC Services Card
      </Button>
      <a
        className="sign-in-learn-more"
        href="https://www2.gov.bc.ca/gov/content/governments/government-id/bcservicescardapp"
        target="_blank"
        rel="noopener noreferrer"
      >
        <FontAwesomeIcon
          icon={faArrowUpRightFromSquare}
          className="sign-in-external-icon"
          aria-hidden="true"
        />
        <span>Learn more about BC Services Card</span>
      </a>
    </div>
  )
}

export default function LoginPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { isReady: isAuthReady, isAuthenticated, session } = useAuth()
  const { isReady: isBookingReady, selectedService, selectedLocation } = useBooking()
  const hasSelections = !!selectedService && !!selectedLocation
  const idpError = searchParams.get('error') === 'idp'
  const signedInAs = session?.userFullName?.trim() || 'Appointment User'

  // Header login / deep-link return: after auth with no booking, go to returnTo or appointments.
  useEffect(() => {
    if (!isAuthReady || !isBookingReady || !isAuthenticated || hasSelections) return
    const returnTo = getJsonFromSession<string>(SessionKeys.LoginReturnTo)
    removeFromSession(SessionKeys.LoginReturnTo)
    const safeReturnTo =
      typeof returnTo === 'string' && /^\/appointments\/\d+\/modify$/.test(returnTo)
        ? returnTo
        : null
    navigate(safeReturnTo ?? '/appointments', { replace: true })
  }, [isAuthReady, isBookingReady, isAuthenticated, hasSelections, navigate])

  if (!isAuthReady || !isBookingReady) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading…</Text>
      </div>
    )
  }

  if (!hasSelections) {
    if (isAuthenticated) {
      return (
        <div className="sign-in-panel" role="status" aria-live="polite">
          <Text>Loading…</Text>
        </div>
      )
    }

    return (
      <div className="sign-in-panel">
        {idpError ? (
          <div className="login-alert">
            <InlineAlert variant="danger" title="Login method not accepted">
              Please login with BC Services Card or email OTP.
            </InlineAlert>
          </div>
        ) : null}
        <Text>
          Please login using one of the following methods to view your appointments or continue a
          booking.
        </Text>
        <SignInMethods />
      </div>
    )
  }

  const heading = isAuthenticated
    ? 'You have successfully logged in.'
    : 'Login to continue your booking.'

  if (!isAuthenticated) {
    return (
      <>
        <BookingStepProgress step={BOOKING_STEP} stepCount={BOOKING_STEP_COUNT} heading={heading} />

        {idpError ? (
          <div className="login-alert">
            <InlineAlert variant="danger" title="Login method not accepted">
              Please login with BC Services Card or email OTP.
            </InlineAlert>
          </div>
        ) : null}

        <div className="sign-in-panel">
          <Text>
            To continue your appointment booking, please login using one of the following methods.
          </Text>
          <SignInMethods />
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
        <InlineAlert variant="success" title="Logged in">
          You are successfully logged in as {signedInAs}.
        </InlineAlert>
      </div>

      <BookingDetailCallout selectedService={selectedService} selectedLocation={selectedLocation} />

      <p className="login-next-copy">
        Continue to the next step to choose a date and time for your appointment.
      </p>

      <div className="booking-nav-row">
        <BookingBackRow onBack={() => navigate('/service-locations')} />
        <BookingContinueRow onContinue={() => navigate('/datetime')} />
      </div>
    </>
  )
}
