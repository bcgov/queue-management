import { getApiBaseUrl } from '../runtime-config'
import { getAccessToken } from '../auth/token-refresh'

// Tells the API "this Keycloak user exists" after a successful login.
export async function createUser(): Promise<void> {
  const token = await getAccessToken()

  const baseUrl = await getApiBaseUrl()
  const res = await fetch(`${baseUrl}/users/`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
  })

  if (!res.ok) {
    throw new Error(`Failed to create user (${res.status})`)
  }
}
