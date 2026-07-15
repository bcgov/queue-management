import { useState } from 'react'
import { Button, TextField, Tooltip, TooltipTrigger } from '@bcgov/design-system-react-components'
import { faLocationDot } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

// Hook + search UI are one locations-search module (directory + booking step 2).
/* eslint-disable react-refresh/only-export-components */
export type NearestLocationStatus = 'idle' | 'loading' | 'active' | 'error'
export type Coordinates = { latitude: number; longitude: number }

type LocationsSearchProps = {
  value: string
  onChange: (value: string) => void
  onClear: () => void
  // From useNearestSort — this component only renders pin state and click.
  nearestSort: boolean
  nearestStatus: NearestLocationStatus
  onNearestSortPress: () => void
  ariaLabel?: string
  placeholder?: string
}

function nearestSortTooltipText(isActive: boolean, status: NearestLocationStatus) {
  if (status === 'loading') {
    return 'Finding your location...'
  }

  if (isActive) {
    return 'Nearest sort is on. Click to turn off.'
  }

  return 'Use your location to sort offices by distance.'
}

// Shared geolocation + nearest-sort state for the directory and booking locations step.
// LocationsSearch only renders the pin; pages use userLocation to sort their lists.
export function useNearestSort() {
  const [nearestSort, setNearestSort] = useState(false)
  const [status, setStatus] = useState<NearestLocationStatus>('idle')
  const [userLocation, setUserLocation] = useState<Coordinates | null>(null)
  const [error, setError] = useState<string | null>(null)

  function clearNearestSort() {
    setNearestSort(false)
    setStatus('idle')
    setUserLocation(null)
    setError(null)
  }

  function toggleNearestSort() {
    if (nearestSort) {
      clearNearestSort()
      return
    }

    // Guard for SSR / browsers without geolocation — pin must not throw.
    if (typeof navigator === 'undefined' || !navigator.geolocation) {
      setStatus('error')
      setError('Your browser does not support location services.')
      return
    }

    setStatus('loading')
    setError(null)

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setUserLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        })
        setNearestSort(true)
        setStatus('active')
      },
      (geoError) => {
        setStatus('error')
        setNearestSort(false)
        setUserLocation(null)
        setError(
          geoError.code === geoError.PERMISSION_DENIED
            ? 'Location access was denied. Allow location in your browser to sort by nearest office.'
            : 'Unable to determine your location. Please try again.',
        )
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 },
    )
  }

  return {
    nearestSort,
    status,
    userLocation,
    error,
    clearNearestSort,
    toggleNearestSort,
  }
}

// Shared location search bar (directory + booking step 2): search, clear, nearest pin.
export function LocationsSearch({
  value,
  onChange,
  onClear,
  nearestSort,
  nearestStatus,
  onNearestSortPress,
  ariaLabel = 'Search locations',
  placeholder = 'Search locations',
}: LocationsSearchProps) {
  const isLoading = nearestStatus === 'loading'

  return (
    <div className="locations-search-row">
      <TextField
        className="locations-search"
        name="location-search"
        value={value}
        onChange={onChange}
        aria-label={ariaLabel}
        iconRight={
          <TooltipTrigger>
            <Button
              className={
                nearestSort ? 'locations-nearest-button is-active' : 'locations-nearest-button'
              }
              variant={nearestSort ? 'primary' : 'secondary'}
              size="medium"
              isIconButton
              onPress={onNearestSortPress}
              isDisabled={isLoading}
              aria-pressed={nearestSort}
              aria-label={
                isLoading
                  ? 'Finding your location'
                  : nearestSort
                    ? 'Clear nearest sort'
                    : 'Sort offices by nearest to you'
              }
            >
              <FontAwesomeIcon icon={faLocationDot} className="locations-pin-icon" />
            </Button>
            <Tooltip>{nearestSortTooltipText(nearestSort, nearestStatus)}</Tooltip>
          </TooltipTrigger>
        }
        // @ts-expect-error placeholder is supported by underlying react-aria TextField
        placeholder={placeholder}
      />
      {nearestSort ? <span className="locations-nearest-label">Nearest first</span> : null}
      {value.trim() ? (
        <Button variant="secondary" size="medium" onPress={onClear}>
          Clear search
        </Button>
      ) : null}
    </div>
  )
}
