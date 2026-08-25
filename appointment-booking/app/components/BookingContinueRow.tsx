import { Button } from '@bcgov/design-system-react-components'

// Shared primary nav button for booking steps. Label, enablement, and navigation are decided by the calling page.
type BookingContinueRowProps = {
  isDisabled?: boolean
  label?: string
  onContinue?: () => void
}

export function BookingContinueRow({
  isDisabled = false,
  label = 'Continue',
  onContinue,
}: BookingContinueRowProps) {
  return (
    <div className="booking-continue-row">
      <Button variant="primary" size="medium" isDisabled={isDisabled} onPress={onContinue}>
        {label}
      </Button>
    </div>
  )
}
