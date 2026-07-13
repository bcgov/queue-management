import { useEffect, useMemo, useState } from 'react'
import { Button, InlineAlert, ProgressBar, SvgChevronDownIcon, SvgChevronUpIcon, TextField } from '@bcgov/design-system-react-components'
import { getPublicServices, type Service } from '../api/services'

const BOOKING_STEP = 1
const BOOKING_STEP_COUNT = 5
const BOOKING_STEP_HEADING =
  'Select the service you need to book an appointment at a Service BC location.'

type SortDirection = 'asc' | 'desc'

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
  const [loadError, setLoadError] = useState(false)
  const [selectedId, setSelectedId] = useState('')
  const [search, setSearch] = useState('')
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc')

  // Cancel in-flight state updates if the user navigates away before the request finishes.
  useEffect(() => {
    let cancelled = false
    getPublicServices()
      .then((loaded) => {
        if (!cancelled) {
          setServices(loaded)
          setLoadError(false)
        }
      })
      .catch(() => {
        if (!cancelled) {
          setLoadError(true)
        }
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

  // Derived view of the loaded list: filtered by search keywords, then sorted by name.
  const visibleServices = useMemo(() => {
    const tokens = search.trim().toLowerCase().split(/\s+/).filter(Boolean)
    const results = tokens.length
      ? services.filter((service) => {
          const name = service.name.toLowerCase()
          return tokens.every((token) => name.includes(token))
        })
      : [...services]

    results.sort((a, b) => {
      const comparison = a.name.localeCompare(b.name, undefined, { sensitivity: 'base' })
      return sortDirection === 'asc' ? comparison : -comparison
    })

    return results
  }, [services, search, sortDirection])

  // Navigate between bookable services using arrow keys
  const handleRowKeyDown = (e: React.KeyboardEvent<HTMLTableRowElement>) => {
    if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return

    const bookable = visibleServices.filter((s) => s.isOnlineBookable)
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
  const showLoadError = !isLoading && loadError
  const showUnavailable = !isLoading && !loadError && services.length === 0
  const showNoResults = !isLoading && services.length > 0 && visibleServices.length === 0

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

      {showLoadError ? (
        <InlineAlert variant="danger" title="Unable to load services">
          Please try again.
        </InlineAlert>
      ) : showUnavailable ? (
        <InlineAlert variant="info" title="Online booking unavailable">
          Please try again.
        </InlineAlert>
      ) : (
        <>
          {!isLoading && (
            <div className="services-search-row">
              <TextField
                className="services-search"
                name="service-search"
                value={search}
                onChange={setSearch}
                // @ts-expect-error placeholder is supported by underlying react-aria TextField
                placeholder="Search services"
              />
              {search.trim() ? (
                <Button variant="secondary" size="medium" onPress={() => setSearch('')}>
                  Clear search
                </Button>
              ) : null}
            </div>
          )}

          <div className="services-table-wrapper">
            <table className="services-table">
              <thead>
                <tr>
                  <th scope="col" className="services-table-select-heading" aria-label="Select" />
                  <th
                    scope="col"
                    aria-sort={sortDirection === 'asc' ? 'ascending' : 'descending'}
                  >
                    <button
                      type="button"
                      className="services-sort-button"
                      onClick={() => setSortDirection((direction) => (direction === 'asc' ? 'desc' : 'asc'))}
                      aria-label={
                        sortDirection === 'asc'
                          ? 'Sort services Z to A'
                          : 'Sort services A to Z'
                      }
                    >
                      <span>Services</span>
                      <span className="services-sort-icons" aria-hidden="true">
                        <span className={sortDirection === 'asc' ? 'is-active' : undefined}>
                          <SvgChevronUpIcon />
                        </span>
                        <span className={sortDirection === 'desc' ? 'is-active' : undefined}>
                          <SvgChevronDownIcon />
                        </span>
                      </span>
                    </button>
                  </th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <tr>
                    <td colSpan={2}>Loading services...</td>
                  </tr>
                ) : showNoResults ? (
                  <tr>
                    <td colSpan={2}>
                      No services match your search. Try different keywords or clear the
                      search to see all services.
                    </td>
                  </tr>
                ) : (
                  visibleServices.map((service) => {
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

      <div className="booking-continue-row">
        <Button variant="primary" size="medium" isDisabled={!canContinue}>
          Continue
        </Button>
      </div>
    </>
  )
}
