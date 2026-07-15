import { Button } from '@bcgov/design-system-react-components'

// Shared Back button for booking steps after step 1. Navigation is decided by the calling page.
type BookingBackRowProps = {
  onBack: () => void
}

export function BookingBackRow({ onBack }: BookingBackRowProps) {
  return (
    <div className="booking-back-row">
      <Button variant="secondary" size="medium" onPress={onBack}>
        Back
      </Button>
    </div>
  )
}
