import { Button, TextField, Tooltip, TooltipTrigger } from '@bcgov/design-system-react-components'
import { faLocationDot } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import type { NearestLocationStatus } from '~/components/useNearestSort'

type SearchRowNearest = {
  sort: boolean
  status: NearestLocationStatus
  onPress: () => void
}

type SearchRowProps = {
  value: string
  onChange: (value: string) => void
  onClear: () => void
  name: string
  ariaLabel: string
  placeholder: string
  /** When set, show the nearest-sort pin (location pages only). */
  nearest?: SearchRowNearest
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

// Shared search row for booking lists. Optional nearest pin for location pages.
export function SearchRow({
  value,
  onChange,
  onClear,
  name,
  ariaLabel,
  placeholder,
  nearest,
}: SearchRowProps) {
  const isNearestLoading = nearest?.status === 'loading'
  const rowClassName = nearest ? 'locations-search-row' : 'services-search-row'
  const fieldClassName = nearest ? 'locations-search' : 'services-search'

  return (
    <div className={rowClassName}>
      <TextField
        className={fieldClassName}
        name={name}
        value={value}
        onChange={onChange}
        aria-label={ariaLabel}
        iconRight={
          nearest ? (
            <TooltipTrigger>
              <Button
                className={
                  nearest.sort ? 'locations-nearest-button is-active' : 'locations-nearest-button'
                }
                variant={nearest.sort ? 'primary' : 'secondary'}
                size="medium"
                isIconButton
                onPress={nearest.onPress}
                isDisabled={isNearestLoading}
                aria-pressed={nearest.sort}
                aria-label={
                  isNearestLoading
                    ? 'Finding your location'
                    : nearest.sort
                      ? 'Clear nearest sort'
                      : 'Sort offices by nearest to you'
                }
              >
                <FontAwesomeIcon icon={faLocationDot} className="locations-pin-icon" />
              </Button>
              <Tooltip>{nearestSortTooltipText(nearest.sort, nearest.status)}</Tooltip>
            </TooltipTrigger>
          ) : undefined
        }
        // @ts-expect-error placeholder is supported by underlying react-aria TextField
        placeholder={placeholder}
      />
      {nearest?.sort ? <span className="locations-nearest-label">Nearest first</span> : null}
      {value.trim() ? (
        <Button variant="secondary" size="medium" onPress={onClear}>
          Clear search
        </Button>
      ) : null}
    </div>
  )
}
