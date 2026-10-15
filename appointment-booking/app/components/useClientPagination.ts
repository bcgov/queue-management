import { useEffect, useState } from 'react'

export const DEFAULT_LIST_PAGE_SIZE = 10

// Client-side paging for already-filtered/sorted lists. Resets to page 1 when the item list changes.
export function useClientPagination<T>(items: T[], pageSize: number = DEFAULT_LIST_PAGE_SIZE) {
  const [page, setPage] = useState(1)
  const totalPages = Math.max(1, Math.ceil(items.length / pageSize))
  const currentPage = Math.min(page, totalPages)

  useEffect(() => {
    setPage(1)
  }, [items])

  const start = (currentPage - 1) * pageSize
  const pageItems = items.slice(start, start + pageSize)

  return {
    page: currentPage,
    pageItems,
    totalPages,
    goPrevious: () => setPage((current) => Math.max(1, current - 1)),
    goNext: () => setPage((current) => Math.min(totalPages, current + 1)),
  }
}
