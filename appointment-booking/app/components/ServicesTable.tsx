import { SvgChevronDownIcon, SvgChevronUpIcon } from '@bcgov/design-system-react-components'
import type { Service } from '../api/services'

type SortDirection = 'asc' | 'desc'

type ServicesTableProps = {
  services: Service[]
  isLoading: boolean
  showNoResults: boolean
  sortDirection: SortDirection
  onToggleSort: () => void
  selectedId: string
  onSelect: (service: Service) => void
}

function getRowClassName(service: Service) {
  return service.isOnlineBookable ? undefined : 'is-unavailable'
}

export function ServicesTable({
  services,
  isLoading,
  showNoResults,
  sortDirection,
  onToggleSort,
  selectedId,
  onSelect,
}: ServicesTableProps) {
  return (
    <fieldset className="services-table-fieldset">
      <legend className="sr-only">Select a service</legend>
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
                  No services match your search. Try different keywords or clear the search to see
                  all services.
                </td>
              </tr>
            ) : (
              services.map((service) => {
                const inputId = `service-${service.id}`

                return (
                  <tr key={service.id} className={getRowClassName(service)}>
                    <td className="services-table-select-cell">
                      <input
                        type="radio"
                        id={inputId}
                        name="service"
                        checked={selectedId === String(service.id)}
                        disabled={!service.isOnlineBookable}
                        onChange={() => onSelect(service)}
                      />
                    </td>
                    <td>
                      {service.isOnlineBookable ? (
                        <label htmlFor={inputId}>{service.name}</label>
                      ) : (
                        service.name
                      )}
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
