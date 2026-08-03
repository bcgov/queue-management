import { ApiClient } from '@/services/api-client.service'

export async function getOffices(client: ApiClient) {
  return client.get<unknown[]>('/offices/')
}
