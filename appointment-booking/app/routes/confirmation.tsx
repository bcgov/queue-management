// Shown after a successful book. Print-friendly summary for the user's records.
import { useEffect, useState } from 'react'
import {
  Button,
  Callout,
  InlineAlert,
  SvgBcLogo,
  Text,
} from '@bcgov/design-system-react-components'
import { useNavigate } from 'react-router'

import { getJsonFromSession } from '~/auth/session'
import { SessionKeys } from '~/auth/session-keys'
import type { BookingConfirmation } from '~/booking/booking-store'
import { formatDate, formatTimeRange } from '~/booking/format-slot'

export function meta() {
  return [{ title: 'Appointment Confirmation' }]
}

export default function ConfirmationPage() {
  const navigate = useNavigate()
  const [isReady, setIsReady] = useState(false)
  const [confirmation, setConfirmation] = useState<BookingConfirmation | null>(null)

  useEffect(() => {
    const id = window.setTimeout(() => {
      setConfirmation(getJsonFromSession<BookingConfirmation>(SessionKeys.BookingConfirmation))
      setIsReady(true)
    }, 0)
    return () => window.clearTimeout(id)
  }, [])

  if (!isReady) {
    return (
      <div className="sign-in-panel" role="status" aria-live="polite">
        <Text>Loading confirmation…</Text>
      </div>
    )
  }

  if (!confirmation) {
    return (
      <div className="confirmation-page">
        <h1>Appointment confirmation</h1>
        <InlineAlert variant="warning" title="No confirmation to show">
          There is no appointment confirmation to show. Book an appointment to see one here.
        </InlineAlert>
        <div className="booking-nav-row no-print">
          <Button type="button" onPress={() => navigate('/services')}>
            Go to services
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="confirmation-page">
      {/* Logo is print-only; the site header already shows it on screen. */}
      <div className="confirmation-brand print-only">
        <SvgBcLogo id="bcgov-logo-confirmation" />
        <p className="confirmation-brand-title">Service BC</p>
      </div>

      <header className="confirmation-header">
        <h1>Appointment confirmed</h1>
        <p className="confirmation-intro">
          Your booking is complete. A confirmation will be emailed to you. You can also optionally
          print or download this page for your records, and bring it when you visit the office.
        </p>
      </header>

      <Callout variant="lightBlue">
        <div className="booking-detail-callout-content">
          <Text>
            Booked by - <strong>{confirmation.bookedByName}</strong>
            <br />
            Selected service - <strong>{confirmation.serviceName}</strong>
            <br />
            Appointment location - <strong>{confirmation.locationName}</strong>
            {confirmation.locationAddress ? (
              <>
                <br />
                Address - <strong>{confirmation.locationAddress}</strong>
              </>
            ) : null}
            <br />
            Appointment date - <strong>{formatDate(confirmation.date)}</strong>
            <br />
            Appointment time -{' '}
            <strong>{formatTimeRange(confirmation.startTime, confirmation.endTime)}</strong>
          </Text>
        </div>
      </Callout>

      <div className="booking-nav-row no-print">
        <Button type="button" variant="secondary" onPress={() => navigate('/services')}>
          Book another appointment
        </Button>
        <Button type="button" variant="primary" onPress={() => window.print()}>
          Print Appointment Confirmation
        </Button>
      </div>
    </div>
  )
}
