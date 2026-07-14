import { Button, TextField, Tooltip, TooltipTrigger } from '@bcgov/design-system-react-components'
import { faLocationDot } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

export type NearestLocationStatus = 'idle' | 'loading' | 'active' | 'error'

type LocationsSearchProps = {
  value: string
  onChange: (value: string) => void
  onClear: () => void
  // Page owns geolocation; this component only renders pin state and click.
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
