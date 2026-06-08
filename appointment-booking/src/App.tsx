import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import { Icon } from 'leaflet'
import { Layout, Page } from '@/components/common'
import {
  getServiceLocationBySlug,
  getServiceLocations,
  type ServiceLocation,
} from '@/data/service-locations'
import {
  Button,
  Callout,
  Heading,
  Link,
  TagGroup,
  TagList,
} from '@bcgov/design-system-react-components'
import { ApiClient } from '@/services/api-client.service'
import { getServicesByOfficeId } from '@/services/booking-api.service'
import { loadRuntimeConfig } from '@/services/runtime-config.service'
import './App.css'
import 'leaflet/dist/leaflet.css'

const locationPinIcon = new Icon({
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).toString(),
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).toString(),
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
})

function RemoveLeafletAttributionPrefix() {
  const map = useMap()

  useEffect(() => {
    map.attributionControl.setPrefix(false)
  }, [map])

  return null
}

type AppProps = {
  initialPath?: string
  locations?: ServiceLocation[]
}

type Coordinates = {
  latitude: number
  longitude: number
}

function navigateTo(path: string) {
  if (typeof window !== 'undefined') {
    window.location.assign(path)
  }
}

function getCurrentPath(initialPath?: string) {
  if (initialPath) {
    const normalized = initialPath.split(/[?#]/)[0]
    return normalized || '/locations'
  }

  if (typeof window !== 'undefined') {
    return window.location.pathname
  }

  return '/locations'
}

function renderServiceTags(location: ServiceLocation) {
  if (location.services.length === 0) {
    return <p className="no-services-text">Contact this office for service information.</p>
  }

  const serviceItems = location.services.map((service) => ({ id: service, textValue: service }))

  return (
    <TagGroup aria-label={`Services at ${location.name}`}>
      <TagList items={serviceItems} />
    </TagGroup>
  )
}

function hasCoordinates(
  location: ServiceLocation,
): location is ServiceLocation & { latitude: number; longitude: number } {
  return location.latitude != null && location.longitude != null
}

function distanceKm(from: Coordinates, to: Coordinates) {
  const toRadians = (value: number) => (value * Math.PI) / 180
  const earthRadiusKm = 6371
  const dLat = toRadians(to.latitude - from.latitude)
  const dLon = toRadians(to.longitude - from.longitude)
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRadians(from.latitude)) *
      Math.cos(toRadians(to.latitude)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return earthRadiusKm * c
}

function LocationMap({ location }: { location: ServiceLocation }) {
  if (location.latitude == null || location.longitude == null) {
    return null
  }

  return (
    <aside className="location-map-panel" aria-label={`Map for ${location.name}`}>
      <div className="location-map-wrapper">
        <MapContainer
          center={[location.latitude, location.longitude]}
          zoom={14}
          scrollWheelZoom={false}
          className="location-map"
        >
          <RemoveLeafletAttributionPrefix />
          <TileLayer
            attribution="&copy; OpenStreetMap contributors"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={[location.latitude, location.longitude]} icon={locationPinIcon}>
            <Popup>{location.name}</Popup>
          </Marker>
        </MapContainer>
      </div>
    </aside>
  )
}

function renderDirectoryPage(
  locations: ServiceLocation[],
  searchQuery: string,
  onSearchChange: (query: string) => void,
  onFindNearestOffice: () => void,
  nearestLocationSlug: string | null,
) {
  return (
    <Page title="Service BC Locations">
      <p className="intro-paragraph directory-intro-paragraph">
        Browse Service BC locations, hours of operation, and the services available at each office.
      </p>

      <div className="search-bar-wrapper" role="search">
        <label htmlFor="location-search" className="search-label">
          Search locations
        </label>
        <div className="search-input-row">
          <div className="search-input-group">
            <svg
              className="search-icon"
              aria-hidden="true"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              id="location-search"
              type="search"
              className="search-input"
              placeholder="Search by office, city, postal code, or street address"
              aria-label="Search Service BC locations"
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
            />
          </div>
          <div className="nearest-office-action-row">
            <Button variant="secondary" size="small" onClick={onFindNearestOffice}>
              <span className="nearest-button-content">
                <svg
                  className="nearest-button-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  aria-hidden="true"
                >
                  <path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z" />
                  <circle cx="12" cy="10" r="3" />
                </svg>
                <span>Find nearest office</span>
              </span>
            </Button>
          </div>
        </div>
      </div>

      <section aria-labelledby="location-list-heading" className="content-section">
        <Heading id="location-list-heading" level={2}>
          All locations <span className="location-count">({locations.length})</span>
        </Heading>
        {locations.length === 0 && searchQuery.trim() && (
          <p className="no-results-text">No locations found for &ldquo;{searchQuery}&rdquo;.</p>
        )}
        <ul className="location-list" aria-label="Service BC office locations">
          {locations.map((location) => (
            <li key={location.slug} className="location-row">
              <Heading level={3} className="location-row-title">
                <Link href={`/locations/${location.slug}`}>{location.name}</Link>
                {nearestLocationSlug === location.slug && (
                  <span className="nearest-badge">Nearest</span>
                )}
              </Heading>
              <div className="location-row-body">
                <div className="location-col location-col-contact">
                  <p className="col-label">Contact</p>
                  <div className="location-meta-item">
                    <svg
                      aria-hidden="true"
                      className="meta-icon"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                    >
                      <path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z" />
                      <circle cx="12" cy="10" r="3" />
                    </svg>
                    <span>{location.address}</span>
                  </div>
                  {location.phone && (
                    <div className="location-meta-item">
                      <svg
                        aria-hidden="true"
                        className="meta-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                      >
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13.5 19.79 19.79 0 0 1 1.61 4.9 2 2 0 0 1 3.59 2.72h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 10.09a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.28 17.5z" />
                      </svg>
                      <a href={`tel:${location.phone}`}>{location.phone}</a>
                    </div>
                  )}
                  {location.email && (
                    <div className="location-meta-item">
                      <svg
                        aria-hidden="true"
                        className="meta-icon"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                      >
                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                        <polyline points="22,6 12,13 2,6" />
                      </svg>
                      <a href={`mailto:${location.email}`}>{location.email}</a>
                    </div>
                  )}
                  <div className="location-row-actions">
                    <a
                      href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(location.address)}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="row-action-link"
                    >
                      Get directions
                    </a>
                    {location.appointmentsEnabledInd !== 1 && (
                      <>
                        <span className="action-sep" aria-hidden="true">
                          ·
                        </span>
                        <span className="walkin-label">Walk-in service available</span>
                      </>
                    )}
                  </div>
                </div>
                <div className="location-col location-col-hours">
                  <p className="col-label">Hours of operation</p>
                  <div className="location-meta-item">
                    <svg
                      aria-hidden="true"
                      className="meta-icon"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                    >
                      <circle cx="12" cy="12" r="10" />
                      <polyline points="12 6 12 12 16 14" />
                    </svg>
                    <span>{location.hours}</span>
                  </div>
                  {location.appointmentsEnabledInd === 1 && (
                    <div className="location-row-actions location-row-actions-hours">
                      <Button
                        variant="primary"
                        size="small"
                        onClick={() => navigateTo('/')}
                      >
                        Book an appointment
                      </Button>
                    </div>
                  )}
                </div>
                <div className="location-col location-col-services">
                  <p className="col-label">Services available</p>
                  {renderServiceTags(location)}
                  <p className="services-detail-link-wrap">
                    <a
                      href={`/locations/${location.slug}#services-heading`}
                      className="row-action-link"
                    >
                      Check all services
                    </a>
                  </p>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </Page>
  )
}

function LocationDetailPage({ location }: { location: ServiceLocation }) {
  const [services, setServices] = useState<string[]>(location.services)

  useEffect(() => {
    loadRuntimeConfig()
      .then((config) => {
        const client = new ApiClient(config)
        return getServicesByOfficeId(client, location.officeId)
      })
      .then((result) => {
        const names = result.services.map((s) => s.service_name).filter(Boolean)
        if (names.length > 0) setServices(names)
      })
      .catch(() => {})
  }, [location.officeId])

  const serviceLocation = { ...location, services }

  return (
    <Page title={location.name}>
      <p className="intro-paragraph">View office details for {location.name}.</p>

      <section aria-labelledby="location-details-heading" className="content-section">
        <Heading id="location-details-heading" level={2}>
          Location details
        </Heading>
        <div className="location-details-layout">
          <div className="location-details-text">
            <dl className="detail-list">
              <div className="detail-item">
                <dt>Address</dt>
                <dd>{location.address}</dd>
              </div>
              <div className="detail-item">
                <dt>Hours</dt>
                <dd>{location.hours}</dd>
              </div>
              {location.phone && (
                <div className="detail-item">
                  <dt>Phone</dt>
                  <dd>
                    <a href={`tel:${location.phone}`}>{location.phone}</a>
                  </dd>
                </div>
              )}
              {location.email && (
                <div className="detail-item">
                  <dt>Email</dt>
                  <dd>
                    <a href={`mailto:${location.email}`}>{location.email}</a>
                  </dd>
                </div>
              )}
              {location.summary && (
                <div className="detail-item">
                  <dt>About</dt>
                  <dd>{location.summary}</dd>
                </div>
              )}
            </dl>
            {location.appointmentsEnabledInd === 1 && (
              <p className="detail-book-cta">
                <Button
                  variant="primary"
                  size="small"
                  onClick={() => navigateTo('/')}
                >
                  Book an appointment
                </Button>
              </p>
            )}
          </div>
          <LocationMap location={serviceLocation} />
        </div>
      </section>

      <section aria-labelledby="services-heading" className="content-section">
        <Heading id="services-heading" level={2}>
          Services at this location
        </Heading>
        {renderServiceTags(serviceLocation)}
      </section>
    </Page>
  )
}

function renderBookingLandingPage() {
  return (
    <Page title="Book an appointment">
      <p className="intro-paragraph">
        Start by choosing a service. The appointment flow will continue with eligible locations and
        available times.
      </p>

      <section aria-labelledby="booking-start-heading" className="content-section">
        <Callout title="Booking starts with a service" variant="lightBlue">
          <p>
            This foundation keeps the booking flow service-focused so people can continue to a
            location, then choose a date and time.
          </p>
          <p className="cta-paragraph">
            <a href="/locations" role="button">
              <Button variant="primary">Browse Service BC locations</Button>
            </a>
          </p>
        </Callout>
      </section>
    </Page>
  )
}

function App({ initialPath, locations = getServiceLocations() }: AppProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const [currentLocationCoords, setCurrentLocationCoords] = useState<Coordinates | null>(null)
  const currentPath = getCurrentPath(initialPath)
  const locationMatch = currentPath.match(/^\/locations\/([^/?#]+)\/?$/)
  const locationSlug = locationMatch?.[1]
  const location = locationSlug ? getServiceLocationBySlug(locationSlug, locations) : null

  const normalizedQuery = searchQuery.trim().toLowerCase()
  const textFilteredLocations = normalizedQuery
    ? locations.filter(
        (loc) =>
          loc.name.toLowerCase().includes(normalizedQuery) ||
          loc.address.toLowerCase().includes(normalizedQuery),
      )
    : locations

  const sortedByNearest = currentLocationCoords
    ? [...textFilteredLocations].sort((a, b) => {
        const aHasCoords = hasCoordinates(a)
        const bHasCoords = hasCoordinates(b)

        if (!aHasCoords && !bHasCoords) {
          return a.name.localeCompare(b.name)
        }
        if (!aHasCoords) {
          return 1
        }
        if (!bHasCoords) {
          return -1
        }

        const aDistance = distanceKm(currentLocationCoords, {
          latitude: a.latitude,
          longitude: a.longitude,
        })
        const bDistance = distanceKm(currentLocationCoords, {
          latitude: b.latitude,
          longitude: b.longitude,
        })
        return aDistance - bDistance
      })
    : textFilteredLocations

  const nearestLocationSlug = currentLocationCoords
    ? (sortedByNearest.find((location) => hasCoordinates(location))?.slug ?? null)
    : null

  const handleFindNearestOffice = () => {
    if (typeof navigator === 'undefined' || !navigator.geolocation) {
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setCurrentLocationCoords({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        })
      },
      undefined,
      { enableHighAccuracy: true, timeout: 10000 },
    )
  }

  if (currentPath === '/book-an-appointment' || currentPath === '/book-an-appointment/') {
    return <Layout>{renderBookingLandingPage()}</Layout>
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
              <Button variant="secondary">View all Service BC locations</Button>
            </a>
          </p>
        </Page>
      </Layout>
    )
  }

  return (
    <Layout>
      {location ? (
        <LocationDetailPage location={location} />
      ) : (
        renderDirectoryPage(
          sortedByNearest,
          searchQuery,
          setSearchQuery,
          handleFindNearestOffice,
          nearestLocationSlug,
        )
      )}
    </Layout>
  )
}

export default App
