import { Button } from '@bcgov/design-system-react-components'

// Shared Continue button for booking steps. Enablement and navigation are decided by the calling page.
type BookingContinueRowProps = {
  isDisabled?: boolean
  onContinue?: () => void
}

export function BookingContinueRow({ isDisabled = false, onContinue }: BookingContinueRowProps) {
  return (
    <div className="booking-continue-row">
      <Button variant="primary" size="medium" isDisabled={isDisabled} onPress={onContinue}>
        Continue
      </Button>
    </div>
  )
}
