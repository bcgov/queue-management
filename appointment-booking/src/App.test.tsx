import { render, screen } from '@testing-library/react'
import type { ReactNode } from 'react'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import App from './App'

vi.mock('@/components/common', () => ({
  Layout: ({ children }: { children: ReactNode }) => <div>{children}</div>,
  Page: ({ children, title }: { children: ReactNode; title: string }) => (
    <section>
      <h1>{title}</h1>
      {children}
    </section>
  ),
}))

vi.mock('@bcgov/design-system-react-components', () => ({
  Button: ({ children, variant, ...props }: any) => (
    <button {...props}>
      {children}
    </button>
  ),
  Callout: ({ title, children }: any) => (
    <section>
      <h2>{title}</h2>
      {children}
    </section>
  ),
  Heading: ({ level, children, ...props }: any) => {
    const Tag = `h${level}` as any
    return <Tag {...props}>{children}</Tag>
  },
  Link: ({ children, href, ...props }: any) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
  TagGroup: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  TagList: ({ children, items = [], ...props }: any) => (
    <div {...props}>
      {typeof children === 'function' ? items.map((item: any) => children(item)) : children}
    </div>
  ),
  Tag: ({ children }: any) => <span>{children}</span>,
}))

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the public Service BC locations directory', () => {
    render(<App initialPath="/locations" />)

    expect(screen.getByRole('heading', { name: 'Service BC Locations' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Service BC - Victoria Courthouse' })).toHaveAttribute(
      'href',
      '/locations/victoria-courthouse',
    )
    expect(screen.getAllByText('Monday to Friday, 8:30 a.m. to 4:30 p.m.')[0]).toBeInTheDocument()
    expect(screen.getByText('Continue to the appointment booking flow')).toBeInTheDocument()
  })

  it('renders a public location detail page', () => {
    render(<App initialPath="/locations/nanaimo-service-centre" />)

    expect(screen.getByRole('heading', { name: 'Service BC - Nanaimo Service Centre' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Services at this location' })).toBeInTheDocument()
    expect(screen.getByText('Start booking an appointment')).toBeInTheDocument()
  })

  it('shows a public not found page for unknown locations', () => {
    render(<App initialPath="/locations/unknown-office" />)

    expect(screen.getByRole('heading', { name: 'Location not found' })).toBeInTheDocument()
    expect(screen.getByText('View all Service BC locations')).toBeInTheDocument()
  })
})
