import { useEffect, useState } from 'react'
import { Button, InlineAlert, ProgressBar } from '@bcgov/design-system-react-components'

import { getPublicServices, type Service } from '../api/services'

const BOOKING_STEP = 1
const BOOKING_STEP_COUNT = 5
const BOOKING_STEP_HEADING =
  'Select the service you need to book an appointment at a Service BC location.'

export function meta() {
  return [{ title: 'Services' }]
}

function getRowClassName(service: Service, selectedId: string) {
  if (!service.isOnlineBookable) {
    return 'is-unavailable'
  }
  if (String(service.id) === selectedId) {
    return 'is-selected'
  }
  return ''
}

export default function ServicesPage() {
  const [services, setServices] = useState<Service[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedId, setSelectedId] = useState('')

  useEffect(() => {
    let cancelled = false
    getPublicServices()
      .then((loaded) => {
        if (!cancelled) {
          setServices(loaded)
        }
      })
      .catch(() => {
        // Silently fail — empty list shows unavailable message
      })
      .finally(() => {
        if (!cancelled) {
          setIsLoading(false)
        }
      })
    return () => {
      cancelled = true
    }
  }, [])

  // Navigate between bookable services using arrow keys
  const handleRowKeyDown = (e: React.KeyboardEvent<HTMLTableRowElement>) => {
    if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return

    const bookable = services.filter((s) => s.isOnlineBookable)
    const idx = bookable.findIndex((s) => String(s.id) === selectedId)
    const nextIdx = e.key === 'ArrowDown' ? idx + 1 : idx - 1

    if (nextIdx >= 0 && nextIdx < bookable.length) {
      e.preventDefault()
      setSelectedId(String(bookable[nextIdx].id))
    }
  }

  const selectedService = services.find((service) => String(service.id) === selectedId)
  const canContinue = !!selectedService?.isOnlineBookable
  const hasUnavailableServices = services.some((service) => !service.isOnlineBookable)
  const showUnavailable = !isLoading && services.length === 0

  return (
    <>
      <h1 className="sr-only">Services</h1>

      <div className="services-booking-progress">
        <p className="services-booking-step-count">
          Step {BOOKING_STEP} of {BOOKING_STEP_COUNT}
        </p>
        <p className="services-booking-step">{BOOKING_STEP_HEADING}</p>
        <ProgressBar
          value={(BOOKING_STEP / BOOKING_STEP_COUNT) * 100}
          aria-label={`Step ${BOOKING_STEP} of ${BOOKING_STEP_COUNT}. ${BOOKING_STEP_HEADING}`}
        />
      </div>

      {showUnavailable ? (
        <InlineAlert variant="info" title="Online booking unavailable">
          Please try again.
        </InlineAlert>
      ) : (
        <>
          <div className="services-table-wrapper">
            <table className="services-table">
              <thead>
                <tr>
                  <th scope="col" className="services-table-select-heading" aria-label="Select" />
                  <th scope="col">Services</th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <tr>
                    <td colSpan={2}>Loading services...</td>
                  </tr>
                ) : (
                  services.map((service) => {
                    const id = String(service.id)

                    return (
                      <tr
                        key={service.id}
                        className={getRowClassName(service, selectedId)}
                        onClick={() => {
                          if (service.isOnlineBookable) setSelectedId(id)
                        }}
                        onKeyDown={handleRowKeyDown}
                        role="radio"
                        aria-checked={selectedId === id}
                        tabIndex={selectedId === id ? 0 : -1}
                      >
                        <td className="services-table-select-cell">
                          <input
                            type="radio"
                            name="service"
                            className="services-table-radio"
                            value={id}
                            checked={selectedId === id}
                            disabled={!service.isOnlineBookable}
                            readOnly
                            aria-label={service.name}
                          />
                        </td>
                        <td>{service.name}</td>
                      </tr>
                    )
                  })
                )}
              </tbody>
            </table>
          </div>

          {!isLoading && hasUnavailableServices && (
            <p className="services-table-note">
              Services that cannot be selected are not available for online booking.
            </p>
          )}
        </>
      )}

      <Button variant="primary" size="medium" isDisabled={!canContinue}>
        Continue
      </Button>
    </>
  )
}
