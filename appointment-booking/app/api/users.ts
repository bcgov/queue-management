import { getApiBaseUrl } from '../runtime-config'
import { getAccessToken } from '../auth/token-refresh'

export type PublicUser = {
  user_id: number
  email: string
  telephone: string
}

// Load the signed-in user's profile for contact pre-fill on the review step.
export async function getCurrentUser(): Promise<PublicUser> {
  const token = await getAccessToken()

  const baseUrl = await getApiBaseUrl()
  const res = await fetch(`${baseUrl}/users/me/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!res.ok) {
    throw new Error(`Failed to load user profile (${res.status})`)
  }

  const body = (await res.json()) as PublicUser[]
  const user = body[0] // API returns a one-item array.
  if (!user) {
    throw new Error('User profile not found')
  }

  return user
}

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
