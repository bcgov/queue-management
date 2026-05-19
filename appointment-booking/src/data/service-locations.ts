export interface ServiceLocation {
  officeId: number
  slug: string
  name: string
  address: string
  hours: string
  summary: string
  services: string[]
  appointmentsEnabledInd: 0 | 1
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
  quick_list?: OfficeApiService[]
  back_office_list?: OfficeApiService[]
}

const serviceLocations: ServiceLocation[] = [
  {
    officeId: 94,
    slug: 'victoria-courthouse',
    name: 'Service BC - Victoria Courthouse',
    address: '800 Fort St, Victoria, BC',
    hours: 'Monday to Friday, 8:30 a.m. to 4:30 p.m.',
    summary: 'Central downtown location serving residents and visitors across greater Victoria.',
    services: ['BCID services', 'Driver licensing support', 'Housing and tenancy information'],
    appointmentsEnabledInd: 1,
  },
  {
    officeId: 95,
    slug: 'nanaimo-service-centre',
    name: 'Service BC - Nanaimo Service Centre',
    address: '4601 Rutherford Rd, Nanaimo, BC',
    hours: 'Monday to Friday, 8:30 a.m. to 4:30 p.m.',
    summary: 'A regional office supporting mid-Island service needs and public counter visits.',
    services: ['Property tax support', 'Income assistance', 'Identity document assistance'],
    appointmentsEnabledInd: 1,
  },
  {
    officeId: 96,
    slug: 'kelowna-civic-centre',
    name: 'Service BC - Kelowna Civic Centre',
    address: '1435 Water St, Kelowna, BC',
    hours: 'Monday to Friday, 8:30 a.m. to 4:30 p.m.',
    summary: 'An Okanagan location with general counter services for the public.',
    services: ['Accessible parking information', 'General office services', 'Public information support'],
    appointmentsEnabledInd: 1,
  },
]

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

export function mapApiOfficeToServiceLocation(office: OfficeApiModel): ServiceLocation {
  const normalizedName = office.office_name.startsWith('Service BC - ')
    ? office.office_name
    : `Service BC - ${office.office_name}`

  return {
    officeId: office.office_id,
    slug: `${slugifyOfficeName(office.office_name)}-${office.office_id}`,
    name: normalizedName,
    address: office.civic_address || 'Address information unavailable',
    hours: 'Hours not published online for this office.',
    summary: office.office_appointment_message || 'Visit this office for in-person services and support.',
    services: toOfficeServices(office),
    appointmentsEnabledInd: normalizeAppointmentsEnabled(office.appointments_enabled_ind),
  }
}

export function mapApiOfficesToVisibleLocations(offices: OfficeApiModel[]): ServiceLocation[] {
  return offices
    .filter((office) => office.online_status === 'Status.SHOW')
    .map(mapApiOfficeToServiceLocation)
    .sort((a, b) => a.name.localeCompare(b.name))
}

export function getServiceLocations() {
  return serviceLocations
}

export function getServiceLocationBySlug(slug: string, locations: ServiceLocation[] = serviceLocations) {
  return locations.find((location) => location.slug === slug) ?? null
}