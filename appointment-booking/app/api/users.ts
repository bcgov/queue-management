import { getApiBaseUrl } from '../runtime-config'
import { getAccessToken } from '../auth/token-refresh'

export type PublicUser = {
  user_id: number
  email: string | null
  telephone: string | null
  send_email_reminders: boolean
  send_sms_reminders: boolean
}

export type UserUpdateBody = {
  email: string
  telephone: string
  send_email_reminders: boolean
  send_sms_reminders: boolean
}

function parseUser(body: PublicUser[]): PublicUser {
  const user = body[0] // API returns a one-item array.
  if (!user) {
    throw new Error('User profile not found')
  }
  return user
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

  return parseUser((await res.json()) as PublicUser[])
}

// Saves contact details and confirmation opt-in flags before booking.
// The API uses these flags to send email/SMS confirmation after a successful book.
export async function updateUser(userId: number, body: UserUpdateBody): Promise<PublicUser> {
  const token = await getAccessToken()

  const baseUrl = await getApiBaseUrl()
  const res = await fetch(`${baseUrl}/users/${userId}/`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    throw new Error(`Failed to update contact details (${res.status})`)
  }

  return parseUser((await res.json()) as PublicUser[])
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
