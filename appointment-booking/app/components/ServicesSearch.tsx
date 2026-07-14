import { Button, TextField } from '@bcgov/design-system-react-components'

// Presentational search row; the page owns the search string and filtering.
type ServicesSearchProps = {
  value: string
  onChange: (value: string) => void
  onClear: () => void
}

export function ServicesSearch({ value, onChange, onClear }: ServicesSearchProps) {
  return (
    <div className="services-search-row">
      <TextField
        className="services-search"
        name="service-search"
        value={value}
        onChange={onChange}
        aria-label="Search services"
        // @ts-expect-error placeholder is supported by underlying react-aria TextField
        placeholder="Search services"
      />
      {value.trim() ? (
        <Button variant="secondary" size="medium" onPress={onClear}>
          Clear search
        </Button>
      ) : null}
    </div>
  )
}
