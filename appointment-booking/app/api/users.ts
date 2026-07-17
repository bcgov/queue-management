import { getApiBaseUrl } from '../runtime-config'
import { getFromSession } from '../auth/session'
import { SessionKeys } from '../auth/session-keys'

// Tells the API "this Keycloak user exists" after a successful login.
export async function createUser(): Promise<void> {
  const token = getFromSession(SessionKeys.KeyCloakToken)
  if (!token) {
    throw new Error('Cannot create user without an access token')
  }

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
