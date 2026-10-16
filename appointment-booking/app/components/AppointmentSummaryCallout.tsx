import { Callout, Text } from '@bcgov/design-system-react-components'

import { formatDate, formatTimeRange } from '~/booking/format-slot'

type AppointmentSummaryCalloutProps = {
  serviceName: string
  locationName: string
  locationAddress: string | null
  date: string
  startTime: string
  endTime: string
}

// Shared service / location / date / time summary (cancel confirm + cancellation pages).
export function AppointmentSummaryCallout({
  serviceName,
  locationName,
  locationAddress,
  date,
  startTime,
  endTime,
}: AppointmentSummaryCalloutProps) {
  return (
    <Callout variant="lightBlue">
      <div className="booking-detail-callout-content">
        <Text>
          Selected service - <strong>{serviceName}</strong>
          <br />
          Appointment location - <strong>{locationName}</strong>
          {locationAddress ? (
            <>
              <br />
              Address - <strong>{locationAddress}</strong>
            </>
          ) : null}
          <br />
          Appointment date - <strong>{formatDate(date)}</strong>
          <br />
          Appointment time - <strong>{formatTimeRange(startTime, endTime)}</strong>
        </Text>
      </div>
    </Callout>
  )
}
