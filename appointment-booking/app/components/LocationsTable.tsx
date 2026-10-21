import { SvgChevronDownIcon, SvgChevronUpIcon } from '@bcgov/design-system-react-components'
import type { ServiceLocation } from '../api/service-locations'

type SortDirection = 'asc' | 'desc'

type LocationsTableProps = {
  locations: ServiceLocation[]
  isLoading: boolean
  showNoResults: boolean
  sortDirection: SortDirection
  onToggleSort: () => void
  selectedId: string
  onSelect: (location: ServiceLocation) => void
}

export function LocationsTable({
  locations,
  isLoading,
  showNoResults,
  sortDirection,
  onToggleSort,
  selectedId,
  onSelect,
}: LocationsTableProps) {
  return (
    <fieldset className="services-table-fieldset">
      <legend className="sr-only">Select a location</legend>
      <div className="services-table-wrapper">
        <table className="services-table">
          <thead>
            <tr>
              <th scope="col" className="services-table-select-heading" aria-hidden="true" />
              <th scope="col" aria-sort={sortDirection === 'asc' ? 'ascending' : 'descending'}>
                <button
                  type="button"
                  className="services-sort-button"
                  onClick={onToggleSort}
                  aria-label={
                    sortDirection === 'asc' ? 'Sort locations Z to A' : 'Sort locations A to Z'
                  }
                >
                  <span>Location</span>
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
                <td colSpan={2}>Loading locations...</td>
              </tr>
            ) : showNoResults ? (
              <tr>
                <td colSpan={2}>
                  No locations match your search. Try different keywords or clear the search to see
                  all locations.
                </td>
              </tr>
            ) : (
              locations.map((location) => {
                const inputId = `location-${location.id}`
                const address = location.address || '—'

                return (
                  <tr
                    key={location.id}
                    className={location.isBookable ? undefined : 'is-unavailable'}
                  >
                    <td className="services-table-select-cell">
                      <input
                        type="radio"
                        id={inputId}
                        name="location"
                        checked={selectedId === String(location.id)}
                        onChange={() => onSelect(location)}
                      />
                    </td>
                    <td>
                      <label htmlFor={inputId}>
                        {location.name}
                        <span className="sr-only">, {address}</span>
                      </label>
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>
    </fieldset>
  )
}
