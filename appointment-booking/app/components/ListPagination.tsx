import { Button } from '@bcgov/design-system-react-components'

type ListPaginationProps = {
  page: number
  totalPages: number
  onPrevious: () => void
  onNext: () => void
}

// Simple Prev / Page X of Y / Next bar. Hidden when there is only one page.
export function ListPagination({ page, totalPages, onPrevious, onNext }: ListPaginationProps) {
  if (totalPages <= 1) {
    return null
  }

  return (
    <nav className="list-pagination" aria-label="List pagination">
      <Button variant="secondary" size="small" isDisabled={page <= 1} onPress={onPrevious}>
        Previous
      </Button>
      <span className="list-pagination-status" aria-live="polite">
        Page {page} of {totalPages}
      </span>
      <Button variant="secondary" size="small" isDisabled={page >= totalPages} onPress={onNext}>
        Next
      </Button>
    </nav>
  )
}
