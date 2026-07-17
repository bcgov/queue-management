// Keycloak login helpers for citizen booking (BC Services Card).
// Handles: start login, read tokens after redirect, reject non-BCSC, logout.

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
  lastname?: string
  firstname?: string
  given_name?: string
  family_name?: string
  name?: string
  preferred_username?: string
  sub?: string
  loginSource?: string
  identity_provider?: string
  display_name?: string
}

// Thrown when Keycloak signed someone in with the wrong identity provider (not BCSC).
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

function resolveFullName(claims: TokenClaims): string {
  const firstName = claims.firstname || claims.given_name || ''
  const lastName = claims.lastname || claims.family_name || ''
  return (
    `${firstName} ${lastName}`.trim() ||
    claims.display_name ||
    claims.name ||
    claims.preferred_username ||
    ''
  )
}

// Rebuilds the auth session after a refresh/redirect. Drops non-BCSC sessions.
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

function buildSessionFromKeycloak(kc: Keycloak): AuthSession {
  const token = kc.token || ''
  const claims = token ? decodeTokenClaims(token) : {}

  return {
    token,
    idToken: kc.idToken || '',
    refreshToken: kc.refreshToken || '',
    userFullName: resolveFullName(claims),
    kcGuid: claims.sub || '',
    loginSource: resolveIdentityProvider(claims),
  }
}

function appLoginRedirectUri(): string {
  // Always return to this environment's app (localhost / test / prod), not a hardcoded URL.
  return `${window.location.origin}/login`
}

// Where Keycloak must send the browser back after BCSC (this finishes the OAuth code exchange).
function appSigninCallbackUri(idpHint: string): string {
  return `${window.location.origin}/signin/${idpHint}`
}

// First call: redirect to Keycloak/BCSC.
// Second call (after return to /signin/:idpHint): finish login and return the session.
// Rejects any IdP other than BCSC.
export async function initKeycloakLogin(idpHint: string): Promise<AuthSession | null> {
  clearStoredAuthSession()

  const keycloakConfigUrl = await getKeycloakConfigUrl()
  const kc = new Keycloak(keycloakConfigUrl)
  kcInstance = kc

  // OAuth callback must return to this page so keycloak-js can finish the code exchange.
  const callbackUri = appSigninCallbackUri(idpHint)

  // Force the chosen IdP (bcsc) and our callback URL on every Keycloak login redirect.
  const originalLogin = kc.login.bind(kc)
  kc.login = (options?: KeycloakLoginOptions) => {
    const next = options
      ? { ...options, idpHint, redirectUri: options.redirectUri || callbackUri }
      : { idpHint, redirectUri: callbackUri }
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

  const session = buildSessionFromKeycloak(kc)
  if (!isAllowedBookingIdp(session.loginSource)) {
    // End the Keycloak SSO session so the next attempt can use BCSC.
    await kc.logout({ redirectUri: `${appLoginRedirectUri()}?error=idp` })
    throw new WrongIdpError(session.loginSource || 'unknown')
  }

  return session
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
