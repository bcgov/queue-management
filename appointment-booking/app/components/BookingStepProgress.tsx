import { ProgressBar } from '@bcgov/design-system-react-components'

// Shared step progress header for booking steps. Step number and heading come from the page.
type BookingStepProgressProps = {
  step: number
  stepCount: number
  heading: string
}

export function BookingStepProgress({ step, stepCount, heading }: BookingStepProgressProps) {
  return (
    <div className="booking-step-progress">
      <p className="booking-step-count">
        Step {step} of {stepCount}
      </p>
      <p className="booking-step-heading">{heading}</p>
      <ProgressBar
        value={(step / stepCount) * 100}
        aria-label={`Step ${step} of ${stepCount}. ${heading}`}
      />
    </div>
  )
}
