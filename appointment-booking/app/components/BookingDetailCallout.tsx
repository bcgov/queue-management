import { Callout, InlineAlert, Text } from '@bcgov/design-system-react-components'

import type { ServiceLocation } from '~/api/service-locations'
import type { Service } from '~/api/services'
import type { BookingSlot } from '~/booking/booking-store'

// Shared by the callout and the datetime step (calendar / time labels).
export function formatDate(date: string) {
  const [year, month, day] = date.split('-').map(Number)
  return new Intl.DateTimeFormat('en-CA', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(year, month - 1, day))
}

function formatTime(time: string) {
  const [hour, minute] = time.split(':').map(Number)
  return new Intl.DateTimeFormat('en-CA', {
    hour: 'numeric',
    minute: '2-digit',
  }).format(new Date(2000, 0, 1, hour, minute))
}

export function formatTimeRange(startTime: string, endTime: string) {
  return `${formatTime(startTime)} – ${formatTime(endTime)}`
}

type BookingDetailCalloutProps = {
  selectedService: Service | null
  selectedLocation: ServiceLocation | null
  /** When set, show chosen date/time under location details. */
  selectedSlot?: BookingSlot | null
}

export function BookingDetailCallout({
  selectedService,
  selectedLocation,
  selectedSlot = null,
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
          {selectedSlot ? (
            <>
              <br />
              Appointment date - <strong>{formatDate(selectedSlot.date)}</strong>
              <br />
              Appointment time -{' '}
              <strong>{formatTimeRange(selectedSlot.startTime, selectedSlot.endTime)}</strong>
            </>
          ) : null}
        </Text>
        {selectedLocation?.appointmentsDisabled === true ? (
          <InlineAlert variant="info" title="Availability">
            Appointments are not available at this location. Please select another location.
          </InlineAlert>
        ) : selectedLocation?.isBookable === false ? (
          <InlineAlert variant="info" title="Availability">
            No appointments available. Select another location, or visit for walk-in service.
          </InlineAlert>
        ) : null}
        {selectedLocation?.appointmentMessage ? (
          <InlineAlert variant="info" title="Location notice">
            {selectedLocation.appointmentMessage}
          </InlineAlert>
        ) : null}
      </div>
    </Callout>
  )
}
