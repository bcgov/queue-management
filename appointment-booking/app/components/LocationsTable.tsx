import { SvgChevronDownIcon, SvgChevronUpIcon } from '@bcgov/design-system-react-components'
import type { KeyboardEvent } from 'react'
import type { Location } from '../api/locations'

type SortDirection = 'asc' | 'desc'

// Presentational table: page owns fetch/filter/sort state, selection, and keyboard navigation.
type LocationsTableProps = {
  locations: Location[]
  isLoading: boolean
  showNoResults: boolean
  sortDirection: SortDirection
  onToggleSort: () => void
  selectedId: string
  onSelect: (location: Location) => void
  onRowKeyDown: (e: KeyboardEvent<HTMLTableRowElement>) => void
}

export function LocationsTable({
  locations,
  isLoading,
  showNoResults,
  sortDirection,
  onToggleSort,
  selectedId,
  onSelect,
  onRowKeyDown,
}: LocationsTableProps) {
  return (
    <div className="services-table-wrapper">
      <table className="services-table">
        <thead>
          <tr>
            <th scope="col" className="services-table-select-heading" aria-label="Select" />
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
            <th scope="col">Address</th>
          </tr>
        </thead>
        <tbody>
          {isLoading ? (
            <tr>
              <td colSpan={3}>Loading locations...</td>
            </tr>
          ) : showNoResults ? (
            <tr>
              <td colSpan={3}>
                No locations match your search. Try different keywords or clear the search to see
                all locations.
              </td>
            </tr>
          ) : (
            locations.map((location) => {
              const id = String(location.id)

              return (
                <tr
                  key={location.id}
                  className={id === selectedId ? 'is-selected' : undefined}
                  onClick={() => onSelect(location)}
                  onKeyDown={onRowKeyDown}
                  role="radio"
                  aria-checked={selectedId === id}
                  // Only the selected row is in the tab order; arrows move selection.
                  tabIndex={selectedId === id ? 0 : -1}
                >
                  <td className="services-table-select-cell">
                    <input
                      type="radio"
                      name="location"
                      className="services-table-radio"
                      value={id}
                      checked={selectedId === id}
                      // Visual/a11y only; selection is handled on the row.
                      readOnly
                      aria-label={`${location.name}${location.address ? `, ${location.address}` : ''}`}
                    />
                  </td>
                  <td className="services-table-name-cell">{location.name}</td>
                  <td className="services-table-address-cell">{location.address || '—'}</td>
                </tr>
              )
            })
          )}
        </tbody>
      </table>
    </div>
  )
}
