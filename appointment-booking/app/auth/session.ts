// Tiny sessionStorage helpers.
// Browser-only: if sessionStorage is missing (server render), do nothing so we don't crash.

import { BOOKING_SESSION_KEYS } from './session-keys'

export function getFromSession(key: string): string | null {
  if (typeof sessionStorage === 'undefined') return null
  return sessionStorage.getItem(key)
}

export function addToSession(key: string, value: string): void {
  if (typeof sessionStorage === 'undefined') return
  sessionStorage.setItem(key, value)
}

export function removeFromSession(key: string): void {
  if (typeof sessionStorage === 'undefined') return
  sessionStorage.removeItem(key)
}

// Clears selected service/location. Used on logout only.
export function clearStoredBookingSession(): void {
  for (const key of BOOKING_SESSION_KEYS) {
    removeFromSession(key)
  }
}

export function getJsonFromSession<T>(key: string): T | null {
  const raw = getFromSession(key)
  if (!raw) return null
  try {
    return JSON.parse(raw) as T
  } catch {
    return null
  }
}

export function addJsonToSession(key: string, value: unknown): void {
  addToSession(key, JSON.stringify(value))
}
