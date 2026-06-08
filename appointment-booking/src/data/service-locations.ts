export interface ServiceLocation {
  officeId: number
  slug: string
  name: string
  address: string
  hours: string
  phone: string
  email: string
  summary: string
  services: string[]
  appointmentsEnabledInd: 0 | 1
  latitude?: number | null
  longitude?: number | null
  externalMapLink?: string | null
}

type OfficeApiService = {
  service_name?: string
  serviceName?: string
  external_service_name?: string
  externalServiceName?: string
}

export interface OfficeApiModel {
  office_id: number
  office_name: string
  civic_address?: string | null
  office_appointment_message?: string | null
  online_status?: string | null
  appointments_enabled_ind?: number | null
  telephone?: string | null
  office_hours?: string | null
  office_contact_email?: string | null
  latitude?: number | null
  longitude?: number | null
  external_map_link?: string | null
  quick_list?: OfficeApiService[]
  back_office_list?: OfficeApiService[]
}

const serviceLocations: ServiceLocation[] = []

function slugifyOfficeName(name: string) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

function toOfficeServices(office: OfficeApiModel) {
  const merged = [...(office.quick_list || []), ...(office.back_office_list || [])]
  const services = merged
    .map((service) => {
      return (
        service.service_name ||
        service.serviceName ||
        service.external_service_name ||
        service.externalServiceName ||
        ''
      )
    })
    .filter((name) => Boolean(name))

  return Array.from(new Set(services))
}

function normalizeAppointmentsEnabled(value: number | null | undefined): 0 | 1 {
  return value === 1 ? 1 : 0
}

function isOfficeVisible(office: OfficeApiModel): boolean {
  const onlineStatus = (office.online_status || '').trim().toUpperCase()
  return !onlineStatus.endsWith('HIDE')
}

export function mapApiOfficeToServiceLocation(office: OfficeApiModel): ServiceLocation {
  const normalizedName = office.office_name.startsWith('Service BC - ')
    ? office.office_name
    : `Service BC - ${office.office_name}`

  return {
    officeId: office.office_id,
    slug: `${slugifyOfficeName(office.office_name)}-${office.office_id}`,
    name: normalizedName,
    address: office.civic_address || 'TODO - Data not available from API',
    hours: office.office_hours || 'TODO - Data not available from API',
    phone: office.telephone || 'TODO - Data not available from API',
    email: office.office_contact_email || 'TODO - Data not available from API',
    summary: office.office_appointment_message || 'TODO - Data not available from API',
    services: toOfficeServices(office),
    appointmentsEnabledInd: normalizeAppointmentsEnabled(office.appointments_enabled_ind),
    latitude: office.latitude,
    longitude: office.longitude,
    externalMapLink: office.external_map_link,
  }
}

export function mapApiOfficesToVisibleLocations(offices: OfficeApiModel[]): ServiceLocation[] {
  return offices
    .filter(isOfficeVisible)
    .map(mapApiOfficeToServiceLocation)
    .sort((a, b) => a.name.localeCompare(b.name))
}

export function getServiceLocations() {
  return serviceLocations
}

export function getServiceLocationBySlug(
  slug: string,
  locations: ServiceLocation[] = serviceLocations,
) {
  return locations.find((location) => location.slug === slug) ?? null
}
