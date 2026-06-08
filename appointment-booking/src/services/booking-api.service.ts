import { ApiClient } from '@/services/api-client.service'
import type { OfficeApiModel } from '@/data/service-locations'

export interface ServiceApiModel {
  service_id: number
  service_name: string
}

export async function getOffices(client: ApiClient) {
  return client.get<{ offices: OfficeApiModel[] }>('/offices/')
}

export async function getServicesByOfficeId(client: ApiClient, officeId: number) {
  return client.get<{ services: ServiceApiModel[] }>(`/services/?office_id=${officeId}`)
}
