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

  // Knowledge-test bookings omit SHOW offices with no DLKT capacity / no slots.
  // Disabled offices stay visible with an availability message.
  const locationsForService = useMemo(() => {
    if (!selectedService?.isDlkt) {
      return locations
    }
    return locations.filter(
      (location) => location.appointmentsDisabled || location.nextAppointmentDate !== null,
    )
  }, [locations, selectedService?.isDlkt])

  // Keep the booking selection aligned with the latest mapped availability for this service.
  useEffect(() => {
    if (isLoading || loadError || !selectedLocation) {
      return
    }

    const match = locationsForService.find((location) => location.id === selectedLocation.id)
    if (!match) {
      setSelectedLocation(null)
      return
    }

    if (
      match.isBookable !== selectedLocation.isBookable ||
      match.appointmentsDisabled !== selectedLocation.appointmentsDisabled ||
      match.nextAppointmentDate !== selectedLocation.nextAppointmentDate
    ) {
      setSelectedLocation(match)
    }
  }, [isLoading, loadError, locationsForService, selectedLocation, setSelectedLocation])

  const visibleLocations = useMemo(() => {
    const tokens = search.trim().toLowerCase().split(/\s+/).filter(Boolean)
    // Copy before sort — Array.sort mutates in place.
    const results = tokens.length
      ? locationsForService.filter((location) => {
          const haystack = `${location.name} ${location.address}`.toLowerCase()
          return tokens.every((token) => haystack.includes(token))
        })
      : [...locationsForService]

    // Bookable locations first; then name or nearest order within each group.
    const byBookable = (a: ServiceLocation, b: ServiceLocation) =>
      Number(b.isBookable) - Number(a.isBookable)

    if (nearestSort && userLocation) {
      results.sort((a, b) => {
        const bookableOrder = byBookable(a, b)
        if (bookableOrder !== 0) {
          return bookableOrder
        }
        return kmFromUser(userLocation, a) - kmFromUser(userLocation, b)
      })
      return results
    }

    results.sort((a, b) => {
      const bookableOrder = byBookable(a, b)
      if (bookableOrder !== 0) {
        return bookableOrder
      }
      const comparison = a.name.localeCompare(b.name, undefined, { sensitivity: 'base' })
      return sortDirection === 'asc' ? comparison : -comparison
    })
    return results
  }, [locationsForService, search, sortDirection, nearestSort, userLocation])

  // Only a bookable location unlocks the next step; unavailable rows stay selectable for info.
  const canContinue = !!selectedService && !!selectedLocation?.isBookable
  const showLoadError = !isLoading && loadError
  const showUnavailable = !isLoading && !loadError && locationsForService.length === 0
  const showNoResults =
    !isLoading && locationsForService.length > 0 && visibleLocations.length === 0

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
