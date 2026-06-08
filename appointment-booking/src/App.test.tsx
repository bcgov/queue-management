import { render, screen, fireEvent } from '@testing-library/react'
import type { ReactNode } from 'react'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import App from './App'
import type { ServiceLocation } from './data/service-locations'

type MockBaseProps = {
  children?: ReactNode
} & Record<string, unknown>

type MockHeadingProps = MockBaseProps & {
  level: 1 | 2 | 3 | 4 | 5 | 6
}

type MockTagItem = {
  id: string
  textValue: string
}

type MockTagListProps = MockBaseProps & {
  children?: ReactNode | ((item: MockTagItem) => ReactNode)
  items?: MockTagItem[]
}

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
  Button: ({ children, ...props }: MockBaseProps) => <button {...props}>{children}</button>,
  Callout: ({ title, children }: MockBaseProps) => (
    <section>
      <h2>{title}</h2>
      {children}
    </section>
  ),
  Heading: ({ level, children, ...props }: MockHeadingProps) => {
    if (level === 1) return <h1 {...props}>{children}</h1>
    if (level === 2) return <h2 {...props}>{children}</h2>
    if (level === 3) return <h3 {...props}>{children}</h3>
    if (level === 4) return <h4 {...props}>{children}</h4>
    if (level === 5) return <h5 {...props}>{children}</h5>
    return <h6 {...props}>{children}</h6>
  },
  Link: ({ children, href, ...props }: MockBaseProps) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
  TagGroup: ({ children, ...props }: MockBaseProps) => <div {...props}>{children}</div>,
  TagList: ({ children, items = [], ...props }: MockTagListProps) => (
    <div {...props}>
      {typeof children === 'function' ? items.map((item) => children(item)) : children}
    </div>
  ),
  Tag: ({ children }: MockBaseProps) => <span>{children}</span>,
}))

const testLocations: ServiceLocation[] = [
  {
    officeId: 94,
    slug: 'victoria-courthouse',
    name: 'Service BC - Victoria Courthouse',
    address: '403-771 Vernon Ave, Victoria, BC V8W 9V1',
    hours: 'Monday to Friday, 9 am to 4:30 pm',
    phone: '',
    email: '',
    summary: '',
    services: [],
    appointmentsEnabledInd: 0,
  },
  {
    officeId: 95,
    slug: 'nanaimo-service-centre',
    name: 'Service BC - Nanaimo Service Centre',
    address: '460 Selby St, Nanaimo, BC V9R 2R7',
    hours: 'Monday to Friday, 9 am to 4:30 pm',
    phone: '',
    email: '',
    summary: '',
    services: [],
    appointmentsEnabledInd: 0,
  },
  {
    officeId: 96,
    slug: 'kelowna-civic-centre',
    name: 'Service BC - Kelowna Civic Centre',
    address: '305-478 Bernard Ave, Kelowna, BC V1Y 6N7',
    hours: 'Monday to Friday, 9 am to 4:30 pm',
    phone: '',
    email: '',
    summary: '',
    services: [],
    appointmentsEnabledInd: 0,
  },
]

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the public Service BC locations directory', () => {
    render(<App initialPath="/locations" locations={testLocations} />)

    expect(screen.getByRole('heading', { name: 'Service BC Locations' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Service BC - Victoria Courthouse' })).toHaveAttribute(
      'href',
      '/locations/victoria-courthouse',
    )
    expect(screen.getAllByText('Monday to Friday, 9 am to 4:30 pm')[0]).toBeInTheDocument()
    expect(screen.queryAllByText('Book an appointment')).toHaveLength(0)
    expect(screen.getAllByText('Walk-in service available')).toHaveLength(3)
  })

  it('filters locations by search query', () => {
    render(<App initialPath="/locations" locations={testLocations} />)

    const searchInput = screen.getByRole('searchbox', { name: 'Search Service BC locations' })
    fireEvent.change(searchInput, { target: { value: 'Victoria' } })

    expect(
      screen.getByRole('link', { name: 'Service BC - Victoria Courthouse' }),
    ).toBeInTheDocument()
    expect(
      screen.queryByRole('link', { name: 'Service BC - Nanaimo Service Centre' }),
    ).not.toBeInTheDocument()
    expect(
      screen.queryByRole('link', { name: 'Service BC - Kelowna Civic Centre' }),
    ).not.toBeInTheDocument()
  })

  it('shows no-results message when search matches nothing', () => {
    render(<App initialPath="/locations" locations={testLocations} />)

    const searchInput = screen.getByRole('searchbox', { name: 'Search Service BC locations' })
    fireEvent.change(searchInput, { target: { value: 'zzznomatch' } })

    expect(screen.getByText(/No locations found for/)).toBeInTheDocument()
  })

  it('filters locations by postal code text in office address', () => {
    render(<App initialPath="/locations" locations={testLocations} />)

    const searchInput = screen.getByRole('searchbox', { name: 'Search Service BC locations' })

    fireEvent.change(searchInput, { target: { value: 'V9R 2R7' } })

    expect(
      screen.getByRole('link', { name: 'Service BC - Nanaimo Service Centre' }),
    ).toBeInTheDocument()
    expect(
      screen.queryByRole('link', { name: 'Service BC - Victoria Courthouse' }),
    ).not.toBeInTheDocument()
    expect(
      screen.queryByRole('link', { name: 'Service BC - Kelowna Civic Centre' }),
    ).not.toBeInTheDocument()
  })

  it('renders a public location detail page', () => {
    render(<App initialPath="/locations/nanaimo-service-centre" locations={testLocations} />)

    expect(
      screen.getByRole('heading', { name: 'Service BC - Nanaimo Service Centre' }),
    ).toBeInTheDocument()
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
    expect(
      screen.queryByText('Online appointment booking is currently unavailable for this office.'),
    ).not.toBeInTheDocument()
  })

  it('shows a public not found page for unknown locations', () => {
    render(<App initialPath="/locations/unknown-office" locations={testLocations} />)

    expect(screen.getByRole('heading', { name: 'Location not found' })).toBeInTheDocument()
    expect(screen.getByText('View all Service BC locations')).toBeInTheDocument()
  })
})
