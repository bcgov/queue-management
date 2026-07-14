import { Button } from '@bcgov/design-system-react-components'

// Shared Continue button for booking steps. Enablement is decided by the calling page.
type BookingContinueRowProps = {
  isDisabled?: boolean
}

export function BookingContinueRow({ isDisabled = false }: BookingContinueRowProps) {
  return (
    <div className="booking-continue-row">
      <Button variant="primary" size="medium" isDisabled={isDisabled}>
        Continue
      </Button>
    </div>
  )
}
