import { Layout, Page } from '@/components/common'
import {
  getServiceLocationBySlug,
  getServiceLocations,
  type ServiceLocation,
} from '@/data/service-locations'
import { Button, Callout, Heading, Link, Tag, TagGroup, TagList } from '@bcgov/design-system-react-components'
import './App.css'

type AppProps = {
  initialPath?: string
  locations?: ServiceLocation[]
}

function getCurrentPath(initialPath?: string) {
  if (initialPath) {
    return initialPath
  }

  if (typeof window !== 'undefined') {
    return `${window.location.pathname}${window.location.search}${window.location.hash}`
  }

  return '/locations'
}

function renderServiceTags(location: ServiceLocation) {
  const serviceItems = location.services.map((service) => ({ id: service, label: service }))

  return (
    <TagGroup aria-label={`${location.name} services`} className="tag-list" selectionMode="none">
      <div className="tag-list-inner">
        <TagList items={serviceItems}>
          {(item: { id: string; label: string }) => (
            <Tag key={item.id} color="blue" className="service-tag-item" id={item.id}>
              {item.label}
            </Tag>
          )}
        </TagList>
      </div>
    </TagGroup>
  )
}

function renderDirectoryPage(locations: ServiceLocation[]) {

  return (
    <Page title="Service BC Locations">
      <p className="intro-paragraph">
        Browse Service BC locations, hours of operation, and the services available at each office.
      </p>

      <section aria-labelledby="location-list-heading" className="content-section">
        <Heading id="location-list-heading" level={2}>All locations</Heading>
        <div className="card-grid">
          {locations.map((location) => (
            <article key={location.slug} className="location-card">
              <Heading level={3}>
                <Link href={`/locations/${location.slug}`}>{location.name}</Link>
              </Heading>
              <p>{location.address}</p>
              <p>
                <strong>Hours:</strong> {location.hours}
              </p>
              <p>{location.summary}</p>
              {renderServiceTags(location)}
            </article>
          ))}
        </div>
      </section>

      <section aria-labelledby="book-appointment-heading" className="content-section">
        <Callout title="Book an appointment" variant="lightBlue">
          <p>
            Start from a service selection when you are ready to book. The location directory is
            available separately for people who only need office information.
          </p>
          <p className="cta-paragraph">
            <a href="/book-an-appointment" role="button">
              <Button variant="primary">
                Continue to the appointment booking flow
              </Button>
            </a>
          </p>
        </Callout>
      </section>
    </Page>
  )
}

function renderLocationDetailPage(location: ServiceLocation) {
  return (
    <Page title={location.name}>
      <p className="intro-paragraph">View office details for {location.name}.</p>

      <section aria-labelledby="location-details-heading" className="content-section">
        <Heading id="location-details-heading" level={2}>Location details</Heading>
        <p>{location.address}</p>
        <p>
          <strong>Hours:</strong> {location.hours}
        </p>
        <p>{location.summary}</p>
      </section>

      <section aria-labelledby="services-heading" className="content-section">
        <Heading id="services-heading" level={2}>Services at this location</Heading>
        {renderServiceTags(location)}
      </section>

      <section aria-labelledby="booking-cta-heading" className="content-section">
        {location.appointmentsEnabledInd === 1 ? (
          <Callout title="Ready to book?" variant="lightBlue">
            <p>
              Booking starts with choosing a service, then choosing an eligible location, then a date
              and time.
            </p>
            <p className="cta-paragraph">
              <a href="/book-an-appointment" role="button">
                <Button variant="primary">
                  Start booking an appointment
                </Button>
              </a>
            </p>
          </Callout>
        ) : (
          <Callout title="Booking unavailable" variant="lightBlue">
            <p>
              Online appointment booking is currently unavailable for this office.
            </p>
          </Callout>
        )}
      </section>
    </Page>
  )
}

function renderBookingLandingPage() {
  return (
    <Page title="Book an appointment">
      <p className="intro-paragraph">
        Start by choosing a service. The appointment flow will continue with eligible locations
        and available times.
      </p>

      <section aria-labelledby="booking-start-heading" className="content-section">
        <Callout title="Booking starts with a service" variant="lightBlue">
          <p>
            This foundation keeps the booking flow service-focused so people can continue to a
            location, then choose a date and time.
          </p>
          <p className="cta-paragraph">
            <a href="/locations" role="button">
              <Button variant="primary">
                Browse Service BC locations
              </Button>
            </a>
          </p>
        </Callout>
      </section>
    </Page>
  )
}

function App({ initialPath, locations = getServiceLocations() }: AppProps) {
  const currentPath = getCurrentPath(initialPath)
  const locationMatch = currentPath.match(/^\/locations\/([^/?#]+)\/?$/)
  const locationSlug = locationMatch?.[1]
  const location = locationSlug ? getServiceLocationBySlug(locationSlug, locations) : null

  if (currentPath === '/book-an-appointment' || currentPath === '/book-an-appointment/') {
    return (
      <Layout>
        {renderBookingLandingPage()}
      </Layout>
    )
  }

  if (locationSlug && !location) {
    return (
      <Layout>
        <Page title="Location not found">
          <p className="intro-paragraph">
            The Service BC location you requested does not exist in this directory.
          </p>
          <p>
            <a href="/locations">
              <Button variant="secondary">
                View all Service BC locations
              </Button>
            </a>
          </p>
        </Page>
      </Layout>
    )
  }

  return (
    <Layout>
      {location ? renderLocationDetailPage(location) : renderDirectoryPage(locations)}
    </Layout>
  )
}

export default App
