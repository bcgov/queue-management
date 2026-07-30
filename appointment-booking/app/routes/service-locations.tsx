import { useEffect, useMemo, useState } from 'react'
import { InlineAlert } from '@bcgov/design-system-react-components'
import { getDistance } from 'geolib'
import { useNavigate } from 'react-router'
import { getServiceLocations, type ServiceLocation } from '~/api/service-locations'
import { useBooking } from '~/booking/booking-context'
import { BookingBackRow } from '~/components/BookingBackRow'
import { BookingContinueRow } from '~/components/BookingContinueRow'
import { BookingDetailCallout } from '~/components/BookingDetailCallout'
import { BookingStepProgress } from '~/components/BookingStepProgress'
import { SearchRow } from '~/components/SearchRow'
import { useNearestSort, type Coordinates } from '~/components/useNearestSort'
import { LocationsTable } from '~/components/LocationsTable'

const BOOKING_STEP = 2
const BOOKING_STEP_COUNT = 5
const BOOKING_STEP_HEADING = 'Select a Service BC location for your appointment.'

type SortDirection = 'asc' | 'desc'

// geolib returns meters; nearest-sort ranks by kilometres. Missing coords sort last.
function kmFromUser(user: Coordinates, location: ServiceLocation) {
  if (location.latitude === null || location.longitude === null) {
    return Number.POSITIVE_INFINITY
  }
  return getDistance(user, { latitude: location.latitude, longitude: location.longitude }) / 1000
}

export function meta() {
  return [{ title: 'Select Location' }]
}

export default function ServiceLocationsPage() {
  const navigate = useNavigate()
  const { selectedService, selectedLocation, setSelectedLocation } = useBooking()
  const selectedId = selectedLocation ? String(selectedLocation.id) : ''

  // nextAppointmentDate is mapped in the API client for a later UI; unused on this page yet.
  const [locations, setLocations] = useState<ServiceLocation[]>([])
  const [isLoading, setIsLoading] = useState(() => !!selectedService)
  const [loadError, setLoadError] = useState(false)
  const [search, setSearch] = useState('')
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc')
  const {
    nearestSort,
    status: locationStatus,
    userLocation,
    error: locationError,
    clearNearestSort,
    toggleNearestSort,
  } = useNearestSort()

  const serviceId = selectedService?.id

  // Ignore late responses if the user leaves the page mid-fetch (SSR/client remounts).
  useEffect(() => {
    if (serviceId == null) {
      return
    }

    let cancelled = false
    getServiceLocations(serviceId)
      .then((loaded) => {
        if (!cancelled) {
          setLocations(loaded)
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
  }, [serviceId])

  const visibleLocations = useMemo(() => {
    const tokens = search.trim().toLowerCase().split(/\s+/).filter(Boolean)
    // Copy before sort — Array.sort mutates in place.
    const results = tokens.length
      ? locations.filter((location) => {
          const haystack = `${location.name} ${location.address}`.toLowerCase()
          return tokens.every((token) => haystack.includes(token))
        })
      : [...locations]

    if (nearestSort && userLocation) {
      results.sort((a, b) => kmFromUser(userLocation, a) - kmFromUser(userLocation, b))
      return results
    }

    results.sort((a, b) => {
      const comparison = a.name.localeCompare(b.name, undefined, { sensitivity: 'base' })
      return sortDirection === 'asc' ? comparison : -comparison
    })
    return results
  }, [locations, search, sortDirection, nearestSort, userLocation])

  const canContinue = !!selectedService && !!selectedLocation
  const showLoadError = !isLoading && loadError
  const showUnavailable = !isLoading && !loadError && locations.length === 0
  const showNoResults = !isLoading && locations.length > 0 && visibleLocations.length === 0

  return (
    <>
      <h1 className="sr-only">Select Location</h1>

      <BookingStepProgress
        step={BOOKING_STEP}
        stepCount={BOOKING_STEP_COUNT}
        heading={BOOKING_STEP_HEADING}
      />

      {showLoadError ? (
        <InlineAlert variant="danger" title="Unable to load locations">
          Please try again.
        </InlineAlert>
      ) : showUnavailable ? (
        <InlineAlert variant="info" title="No locations available">
          Please try again.
        </InlineAlert>
      ) : (
        <div className="booking-locations-layout">
          {!isLoading && (
            <SearchRow
              value={search}
              onChange={setSearch}
              onClear={() => setSearch('')}
              name="location-search"
              ariaLabel="Search locations"
              placeholder="Search locations"
              nearest={{
                sort: nearestSort,
                status: locationStatus,
                onPress: toggleNearestSort,
              }}
            />
          )}

          {locationError ? (
            <InlineAlert variant="danger" title="Location unavailable">
              {locationError}
            </InlineAlert>
          ) : null}

          <div className="booking-locations-body">
            <LocationsTable
              locations={visibleLocations}
              isLoading={isLoading}
              showNoResults={showNoResults}
              sortDirection={sortDirection}
              onToggleSort={() => {
                // Name sort and nearest sort are mutually exclusive.
                clearNearestSort()
                setSortDirection((direction) => (direction === 'asc' ? 'desc' : 'asc'))
              }}
              selectedId={selectedId}
              onSelect={setSelectedLocation}
            />

            <aside
              className="booking-locations-detail"
              aria-label="Booking selection details"
              role="status"
            >
              <BookingDetailCallout
                selectedService={selectedService}
                selectedLocation={selectedLocation}
              />
            </aside>
          </div>
        </div>
      )}

      <div className="booking-nav-row">
        <BookingBackRow onBack={() => navigate('/services')} />
        <BookingContinueRow
          isDisabled={!canContinue}
          onContinue={() => {
            navigate('/login')
          }}
        />
      </div>
    </>
  )
}
