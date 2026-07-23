// Keycloak login helpers for citizen booking (BCSC or email OTP).
// Handles: start login, read tokens after redirect, reject disallowed IdPs, logout.

import Keycloak, { type KeycloakLoginOptions } from 'keycloak-js'

import { getKeycloakConfigUrl } from '../runtime-config'
import { addToSession, getFromSession, removeFromSession } from './session'
import { AUTH_SESSION_KEYS, isAllowedBookingIdp, SessionKeys } from './session-keys'

// What the rest of the app treats as "signed in".
export type AuthSession = {
  token: string
  idToken: string
  refreshToken: string
  userFullName: string
  kcGuid: string
  loginSource: string
}

type TokenClaims = {
  email?: string
  sub?: string
  loginSource?: string
  identity_provider?: string
  display_name?: string
}

// Thrown when Keycloak signed someone in with a disallowed identity provider.
export class WrongIdpError extends Error {
  readonly identityProvider: string

  constructor(identityProvider: string) {
    super('WRONG_IDP')
    this.name = 'WrongIdpError'
    this.identityProvider = identityProvider
  }
}

// Reused on logout so we can call Keycloak logout with the current tokens.
let kcInstance: Keycloak | undefined

// Prevents a second /signin mount from starting a new login while one is in progress
// (would burn the OAuth code and loop on "Signing you in…").
let loginInFlight: Promise<AuthSession | null> | null = null

// Removes auth tokens/profile from sessionStorage. Does not touch booking selections.
export function clearStoredAuthSession(): void {
  for (const key of AUTH_SESSION_KEYS) {
    removeFromSession(key)
  }
}

// JWT middle section → JSON claims (name, IdP, user id, etc.).
function decodeTokenClaims(token: string): TokenClaims {
  const base64Url = token.split('.')[1]
  if (!base64Url) return {}
  const base64 = decodeURIComponent(
    window
      .atob(base64Url)
      .split('')
      .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join(''),
  )
  return JSON.parse(base64) as TokenClaims
}

// Which login method was used: bcsc, idir, bceid, ...
function resolveIdentityProvider(claims: TokenClaims): string {
  return (claims.identity_provider || claims.loginSource || '').trim().toLowerCase()
}

// Prefer display_name; then email; then "Appointment User".
function resolveFullName(claims: TokenClaims): string {
  return claims.display_name?.trim() || claims.email?.trim() || 'Appointment User'
}

// Rebuilds the auth session after a refresh/redirect. Drops disallowed IdP sessions.
export function readAuthSessionFromStorage(): AuthSession | null {
  const token = getFromSession(SessionKeys.KeyCloakToken)
  if (!token) return null

  let identityProvider = getFromSession(SessionKeys.UserAccountType) || ''
  let userFullName = getFromSession(SessionKeys.UserFullName) || ''
  let kcGuid = getFromSession(SessionKeys.UserKcId) || ''

  try {
    const claims = decodeTokenClaims(token)
    if (!identityProvider) {
      identityProvider = resolveIdentityProvider(claims)
    }
    if (!userFullName) {
      userFullName = resolveFullName(claims)
    }
    if (!kcGuid) {
      kcGuid = claims.sub || ''
    }
  } catch {
    // Keep stored values if the token cannot be decoded.
  }

  if (!isAllowedBookingIdp(identityProvider)) {
    clearStoredAuthSession()
    return null
  }

  return {
    token,
    idToken: getFromSession(SessionKeys.KeyCloakIdToken) || '',
    refreshToken: getFromSession(SessionKeys.KeyCloakRefreshToken) || '',
    userFullName,
    kcGuid,
    loginSource: identityProvider,
  }
}

// Saves tokens + display fields so login survives the Keycloak redirect.
export function writeAuthSession(session: AuthSession): void {
  addToSession(SessionKeys.KeyCloakToken, session.token)
  addToSession(SessionKeys.KeyCloakIdToken, session.idToken)
  addToSession(SessionKeys.KeyCloakRefreshToken, session.refreshToken)
  addToSession(SessionKeys.UserFullName, session.userFullName)
  addToSession(SessionKeys.UserKcId, session.kcGuid)
  addToSession(SessionKeys.UserAccountType, session.loginSource)
}

function buildSessionFromKeycloak(kc: Keycloak, requestedIdpHint: string): AuthSession {
  const token = kc.token || ''
  const claims = token ? decodeTokenClaims(token) : {}
  const claimedIdp = resolveIdentityProvider(claims)
  // Prefer the token claim; if the OTP/BCSC IdP mapper has not set it yet, use the IdP we asked for.
  const loginSource = claimedIdp || requestedIdpHint.trim().toLowerCase()

  return {
    token,
    idToken: kc.idToken || '',
    refreshToken: kc.refreshToken || '',
    userFullName: resolveFullName(claims),
    kcGuid: claims.sub || '',
    loginSource,
  }
}

function appLoginRedirectUri(): string {
  // Always return to this environment's app (localhost / test / prod), not a hardcoded URL.
  return `${window.location.origin}/login`
}

// Where Keycloak must send the browser back after IdP login (finishes the OAuth code exchange).
function appSigninCallbackUri(idpHint: string): string {
  return `${window.location.origin}/signin/${idpHint}`
}

// First call: redirect to Keycloak with the chosen IdP (bcsc or otp).
// Second call (after return to /signin/:idpHint): finish login and return the session.
// Rejects any IdP not in ALLOWED_BOOKING_IDPS.
export async function initKeycloakLogin(idpHint: string): Promise<AuthSession | null> {
  if (loginInFlight) return loginInFlight

  loginInFlight = (async () => {
    clearStoredAuthSession()

    const keycloakConfigUrl = await getKeycloakConfigUrl()
    const kc = new Keycloak(keycloakConfigUrl)
    kcInstance = kc

    // OAuth callback must return to this page so keycloak-js can finish the code exchange.
    const callbackUri = appSigninCallbackUri(idpHint)
    // True when Keycloak has redirected back with an auth code (not a silent SSO reuse).
    const isOAuthReturn =
      window.location.search.includes('code=') || window.location.hash.includes('code=')

    // Force the chosen IdP + a fresh login so an existing Keycloak SSO session cannot win.
    const originalLogin = kc.login.bind(kc)
    const loginWithRequestedIdp = () =>
      originalLogin({
        idpHint,
        redirectUri: callbackUri,
        prompt: 'login',
      })

    kc.login = (options?: KeycloakLoginOptions) => {
      const next: KeycloakLoginOptions = {
        ...(options || {}),
        idpHint,
        redirectUri: options?.redirectUri || callbackUri,
        prompt: 'login',
      }
      return originalLogin(next)
    }

    const authenticated = await kc.init({
      onLoad: 'login-required',
      checkLoginIframe: false,
      pkceMethod: 'S256',
      redirectUri: callbackUri,
    })

    if (!authenticated || !kc.token) {
      return null
    }

    const session = buildSessionFromKeycloak(kc, idpHint)
    if (!isAllowedBookingIdp(session.loginSource)) {
      // If SSO reused a disallowed session (no OAuth code yet), force a fresh IdP login.
      if (!isOAuthReturn) {
        await loginWithRequestedIdp()
        return null
      }

      await kc.logout({ redirectUri: `${appLoginRedirectUri()}?error=idp` })
      throw new WrongIdpError(session.loginSource || 'unknown')
    }

    return session
  })().finally(() => {
    loginInFlight = null
  })

  return loginInFlight
}

export async function logoutKeycloak(redirectUri: string): Promise<void> {
  // Capture tokens before AuthProvider clears local session storage.
  const token = getFromSession(SessionKeys.KeyCloakToken) || undefined
  const refreshToken = getFromSession(SessionKeys.KeyCloakRefreshToken) || undefined
  const idToken = getFromSession(SessionKeys.KeyCloakIdToken) || undefined

  if (!token) {
    window.location.assign(redirectUri)
    return
  }

  const keycloakConfigUrl = await getKeycloakConfigUrl()
  const kc = kcInstance || new Keycloak(keycloakConfigUrl)
  kcInstance = kc

  if (!kc.authenticated) {
    await kc.init({
      token,
      refreshToken,
      idToken,
      checkLoginIframe: false,
      pkceMethod: 'S256',
    })
  }

  await kc.logout({ redirectUri })
}
