import { useEffect, useMemo, useState } from 'react'
import { Callout, InlineAlert, Text } from '@bcgov/design-system-react-components'
import { getDistance } from 'geolib'
import { useNavigate } from 'react-router'
import { getBookingLocations, type Location } from '../api/locations'
import type { Service } from '../api/services'
import { useBooking } from '../booking/booking-context'
import { BookingBackRow } from '../components/BookingBackRow'
import { BookingContinueRow } from '../components/BookingContinueRow'
import { BookingStepProgress } from '../components/BookingStepProgress'
import { LocationsSearch, useNearestSort, type Coordinates } from '../components/LocationsSearch'
import { LocationsTable } from '../components/LocationsTable'

const BOOKING_STEP = 2
const BOOKING_STEP_COUNT = 5
const BOOKING_STEP_HEADING = 'Select a Service BC location for your appointment.'

// Selection summary; nested InlineAlert shows the office online appointment message when set.
function BookingDetailCallout({
  selectedService,
  selectedLocation,
}: {
  selectedService: Service | null
  selectedLocation: Location | null
}) {
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
              Appointment Location - <strong>{selectedLocation.name}</strong>
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

type SortDirection = 'asc' | 'desc'

// geolib returns meters; nearest-sort ranks by kilometres. Missing coords sort last.
function kmFromUser(user: Coordinates, location: Location) {
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

  const [locations, setLocations] = useState<Location[]>([])
  const [isLoading, setIsLoading] = useState(true)
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

  // Ignore late responses if the user leaves the page mid-fetch (SSR/client remounts).
  useEffect(() => {
    let cancelled = false
    getBookingLocations()
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
  }, [])

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
            <LocationsSearch
              value={search}
              onChange={setSearch}
              onClear={() => setSearch('')}
              nearestSort={nearestSort}
              nearestStatus={locationStatus}
              onNearestSortPress={toggleNearestSort}
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
        <BookingContinueRow isDisabled={!canContinue} />
      </div>
    </>
  )
}
