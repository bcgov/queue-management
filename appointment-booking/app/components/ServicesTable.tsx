import { SvgChevronDownIcon, SvgChevronUpIcon } from '@bcgov/design-system-react-components'
import type { KeyboardEvent } from 'react'
import type { Service } from '../api/services'

type SortDirection = 'asc' | 'desc'

// Presentational table: page owns fetch/filter/sort state, selection, and keyboard navigation.
type ServicesTableProps = {
  services: Service[]
  isLoading: boolean
  showNoResults: boolean
  sortDirection: SortDirection
  onToggleSort: () => void
  selectedId: string
  onSelect: (service: Service) => void
  onRowKeyDown: (e: KeyboardEvent<HTMLTableRowElement>) => void
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

export function ServicesTable({
  services,
  isLoading,
  showNoResults,
  sortDirection,
  onToggleSort,
  selectedId,
  onSelect,
  onRowKeyDown,
}: ServicesTableProps) {
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
                  sortDirection === 'asc' ? 'Sort services Z to A' : 'Sort services A to Z'
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
                No services match your search. Try different keywords or clear the search to see all
                services.
              </td>
            </tr>
          ) : (
            services.map((service) => {
              const id = String(service.id)

              return (
                <tr
                  key={service.id}
                  className={getRowClassName(service, selectedId)}
                  onClick={() => {
                    // Unavailable services are shown but not selectable.
                    if (service.isOnlineBookable) onSelect(service)
                  }}
                  onKeyDown={onRowKeyDown}
                  role="radio"
                  aria-checked={selectedId === id}
                  // Only the selected row is in the tab order; arrows move selection.
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
                      // Visual/a11y only; selection is handled on the row.
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
  )
}
