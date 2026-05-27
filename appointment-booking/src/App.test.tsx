import { render, screen } from '@testing-library/react'
import type { ReactNode } from 'react'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import App from './App'
import type { ServiceLocation } from './data/service-locations'

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
    expect(screen.getAllByText('Monday to Friday, 9 am to 4:30 pm')[0]).toBeInTheDocument()
    expect(screen.getAllByText('Book an appointment')).toHaveLength(3)
  })

  it('renders a public location detail page', () => {
    render(<App initialPath="/locations/nanaimo-service-centre" />)

    expect(screen.getByRole('heading', { name: 'Service BC - Nanaimo Service Centre' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Services at this location' })).toBeInTheDocument()
    expect(screen.queryByText('Start booking an appointment')).not.toBeInTheDocument()
  })

  it('hides booking button and shows unavailable state for non-bookable office', () => {
    const nonBookableOffice: ServiceLocation = {
      officeId: 999,
      slug: 'test-office',
      name: 'Service BC - Test Office',
      address: '123 Test St, Victoria, BC V8V 1A1',
      hours: 'Monday to Friday, 9 am to 4:30 pm',
      phone: '250-000-0000',
      email: 'ServiceBC.TestOffice@gov.bc.ca',
      summary: 'Test office for verifying non-bookable location behavior.',
      services: ['General information'],
      appointmentsEnabledInd: 0,
    }

    render(<App initialPath="/locations/test-office" locations={[nonBookableOffice]} />)

    expect(screen.getByRole('heading', { name: 'Service BC - Test Office' })).toBeInTheDocument()
    expect(screen.queryByText('Start booking an appointment')).not.toBeInTheDocument()
    expect(screen.queryByText('Online appointment booking is currently unavailable for this office.')).not.toBeInTheDocument()
  })

  it('shows a public not found page for unknown locations', () => {
    render(<App initialPath="/locations/unknown-office" />)

    expect(screen.getByRole('heading', { name: 'Location not found' })).toBeInTheDocument()
    expect(screen.getByText('View all Service BC locations')).toBeInTheDocument()
  })
})
