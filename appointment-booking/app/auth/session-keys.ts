// Session keys and IdP hints

export const SessionKeys = {
  KeyCloakToken: 'KEYCLOAK_TOKEN',
  KeyCloakRefreshToken: 'KEYCLOAK_REFRESH_TOKEN',
  KeyCloakIdToken: 'KEYCLOAK_ID_TOKEN',
  UserFullName: 'USER_FULL_NAME',
  UserKcId: 'USER_KC_ID',
  UserAccountType: 'USER_ACCOUNT_TYPE',
  // Booking selections survive the IdP redirect round-trip.
  BookingSelectedService: 'BOOKING_SELECTED_SERVICE',
  BookingSelectedLocation: 'BOOKING_SELECTED_LOCATION',
} as const

// Cleared on logout and when discarding a bad/non-BCSC auth session.
export const AUTH_SESSION_KEYS = [
  SessionKeys.KeyCloakToken,
  SessionKeys.KeyCloakRefreshToken,
  SessionKeys.KeyCloakIdToken,
  SessionKeys.UserFullName,
  SessionKeys.UserKcId,
  SessionKeys.UserAccountType,
] as const

// Cleared on logout only — kept across BCSC login redirect.
export const BOOKING_SESSION_KEYS = [
  SessionKeys.BookingSelectedService,
  SessionKeys.BookingSelectedLocation,
] as const

export const IdpHint = {
  BCSC: 'bcsc',
} as const

// Citizen booking accepts only BCSC for now (OTP may be added later).
export const ALLOWED_BOOKING_IDPS = [IdpHint.BCSC] as const

// True only for IdPs we allow in this booking app (currently BCSC).
export function isAllowedBookingIdp(identityProvider: string | null | undefined): boolean {
  const normalized = identityProvider?.trim().toLowerCase()
  return !!normalized && (ALLOWED_BOOKING_IDPS as readonly string[]).includes(normalized)
}
