import { ApiClient } from '@/services/api-client.service'
import type { OfficeApiModel } from '@/data/service-locations'

export async function getOffices(client: ApiClient) {
  return client.get<{ offices: OfficeApiModel[] }>('/offices/')
}
