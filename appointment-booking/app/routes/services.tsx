import { useEffect, useMemo, useState } from 'react'
import { InlineAlert } from '@bcgov/design-system-react-components'
import { useNavigate } from 'react-router'
import { getPublicServices, type Service } from '~/api/services'
import { useBooking } from '~/booking/booking-context'
import { BookingContinueRow } from '~/components/BookingContinueRow'
import { BookingStepProgress } from '~/components/BookingStepProgress'
import { SearchRow } from '~/components/SearchRow'
import { ServicesTable } from '~/components/ServicesTable'

const BOOKING_STEP = 1
const BOOKING_STEP_COUNT = 5
const BOOKING_STEP_HEADING =
  'Select the service you need to book an appointment at a Service BC location.'

type SortDirection = 'asc' | 'desc'

export function meta() {
  return [{ title: 'Services' }]
}

export default function ServicesPage() {
  const navigate = useNavigate()
  // Selection lives in booking context so later steps can reuse it.
  const { selectedService, setSelectedService } = useBooking()
  const selectedId = selectedService ? String(selectedService.id) : ''

  const [services, setServices] = useState<Service[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
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

  // Page owns Continue enablement; only a bookable selection unlocks the next step.
  const canContinue = !!selectedService?.isOnlineBookable
  const hasUnavailableServices = services.some((service) => !service.isOnlineBookable)
  const showLoadError = !isLoading && loadError
  const showUnavailable = !isLoading && !loadError && services.length === 0
  const showNoResults = !isLoading && services.length > 0 && visibleServices.length === 0

  return (
    <>
      <h1 className="sr-only">Services</h1>

      <BookingStepProgress
        step={BOOKING_STEP}
        stepCount={BOOKING_STEP_COUNT}
        heading={BOOKING_STEP_HEADING}
      />

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
            <SearchRow
              value={search}
              onChange={setSearch}
              onClear={() => setSearch('')}
              name="service-search"
              ariaLabel="Search services"
              placeholder="Search services"
            />
          )}

          <ServicesTable
            services={visibleServices}
            isLoading={isLoading}
            showNoResults={showNoResults}
            sortDirection={sortDirection}
            onToggleSort={() =>
              setSortDirection((direction) => (direction === 'asc' ? 'desc' : 'asc'))
            }
            selectedId={selectedId}
            onSelect={setSelectedService}
          />

          {!isLoading && hasUnavailableServices && (
            <p className="services-table-note">
              Services that cannot be selected are not available for online booking.
            </p>
          )}
        </>
      )}

      <BookingContinueRow
        isDisabled={!canContinue}
        onContinue={() => navigate('/service-locations')}
      />
    </>
  )
}
