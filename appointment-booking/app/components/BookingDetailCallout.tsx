import { Callout, InlineAlert, Text } from '@bcgov/design-system-react-components'

import type { ServiceLocation } from '~/api/service-locations'
import type { Service } from '~/api/services'
import type { BookingSlot } from '~/booking/booking-store'

type BookingDetailCalloutProps = {
  selectedService: Service | null
  selectedLocation: ServiceLocation | null
  /** When set (datetime step), show chosen date/time under location details. */
  selectedSlot?: BookingSlot | null
  formatDate?: (date: string) => string
  formatTimeRange?: (startTime: string, endTime: string) => string
}

export function BookingDetailCallout({
  selectedService,
  selectedLocation,
  selectedSlot = null,
  formatDate,
  formatTimeRange,
}: BookingDetailCalloutProps) {
  return (
    <Callout variant="lightBlue">
      <div className="booking-detail-callout-content">
        <Text>
          {selectedService ? (
            <>
              Selected service - <strong>{selectedService.name}</strong>
              <br />
            </>
          ) : (
            <>Please go back to choose a service before selecting a location.</>
          )}
          {selectedLocation ? (
            <>
              {!selectedService ? <br /> : null}
              Appointment location - <strong>{selectedLocation.name}</strong>
              {selectedLocation.address ? (
                <>
                  <br />
                  Address - <strong>{selectedLocation.address}</strong>
                </>
              ) : null}
            </>
          ) : selectedService ? (
            <>Select a location from the list to view details.</>
          ) : null}
          {selectedSlot && formatDate && formatTimeRange ? (
            <>
              <br />
              Appointment date - <strong>{formatDate(selectedSlot.date)}</strong>
              <br />
              Appointment time -{' '}
              <strong>{formatTimeRange(selectedSlot.startTime, selectedSlot.endTime)}</strong>
            </>
          ) : null}
        </Text>
        {selectedLocation?.appointmentMessage ? (
          <InlineAlert variant="info" title="Location notice">
            {selectedLocation.appointmentMessage}
          </InlineAlert>
        ) : null}
      </div>
    </Callout>
  )
}
