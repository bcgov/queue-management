import type { ReactNode } from 'react'

interface PageProps {
  title: string
  children: ReactNode
}

export function Page({ title, children }: PageProps) {
  return (
    <div className="page">
      <h1>{title}</h1>
      <div className="page-content">{children}</div>
    </div>
  )
}
