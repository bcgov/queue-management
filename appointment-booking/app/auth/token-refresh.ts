// Proactive Keycloak access-token refresh while the tab stays open.
// Keycloak realm Access Token Lifespan is 5 minutes. We schedule one timer to fire
// ~30 seconds before that expiry, call updateToken(30), write the new tokens if
// refreshed, then schedule the next timer from the new expiry.

import Keycloak from 'keycloak-js'

import { getKeycloakConfigUrl } from '../runtime-config'
import { getFromSession } from './session'
import { SessionKeys } from './session-keys'
import {
  type AuthSession,
  clearStoredAuthSession,
  writeAuthSession,
} from './keycloak'

// How early before access-token expiry we refresh (realm lifespan is 5 minutes).
const REFRESH_EARLY_SECONDS = 30

let refreshKc: Keycloak | undefined
let refreshTimerId: number | undefined
// Bumped on stop so a late ensure/refresh after logout/unmount does not reschedule.
let refreshRunId = 0
// Set by startTokenRefresh so getAccessToken failures clear React auth state too.
let onAuthSessionUpdated: ((session: AuthSession | null) => void) | null = null

async function ensureKeycloakFromStorage(): Promise<Keycloak | null> {
  const token = getFromSession(SessionKeys.KeyCloakToken) || undefined
  const refreshToken = getFromSession(SessionKeys.KeyCloakRefreshToken) || undefined
  const idToken = getFromSession(SessionKeys.KeyCloakIdToken) || undefined
  if (!token || !refreshToken) return null
  if (refreshKc?.authenticated && refreshKc.token) return refreshKc

  const kc = new Keycloak(await getKeycloakConfigUrl())
  refreshKc = kc
  const authenticated = await kc.init({
    token,
    refreshToken,
    idToken,
    checkLoginIframe: false,
    pkceMethod: 'S256',
  })
  if (!authenticated || !kc.token) return null
  return kc
}

function sessionFromKeycloakTokens(kc: Keycloak): AuthSession {
  return {
    token: kc.token || '',
    idToken: kc.idToken || '',
    refreshToken: kc.refreshToken || '',
    userFullName: getFromSession(SessionKeys.UserFullName) || '',
    kcGuid: getFromSession(SessionKeys.UserKcId) || '',
    loginSource: getFromSession(SessionKeys.UserAccountType) || '',
  }
}

function persistRefreshedSession(kc: Keycloak): void {
  const session = sessionFromKeycloakTokens(kc)
  writeAuthSession(session)
  onAuthSessionUpdated?.(session)
}

function clearRefreshTimer(): void {
  if (refreshTimerId !== undefined) {
    window.clearTimeout(refreshTimerId)
    refreshTimerId = undefined
  }
}

export function stopTokenRefresh(): void {
  refreshRunId += 1
  clearRefreshTimer()
  // Drop the in-memory client so the next ensure re-reads sessionStorage tokens.
  refreshKc = undefined
}

function failRefresh(): void {
  stopTokenRefresh()
  clearStoredAuthSession()
  onAuthSessionUpdated?.(null)
}

// updateToken uses in-memory tokens; keep them aligned with sessionStorage (e.g. after DevTools edits).
function syncTokensFromStorage(kc: Keycloak): boolean {
  const token = getFromSession(SessionKeys.KeyCloakToken) || undefined
  const refreshToken = getFromSession(SessionKeys.KeyCloakRefreshToken) || undefined
  const idToken = getFromSession(SessionKeys.KeyCloakIdToken) || undefined
  if (!token || !refreshToken) return false
  kc.token = token
  kc.refreshToken = refreshToken
  if (idToken) kc.idToken = idToken
  return true
}

function scheduleRefresh(kc: Keycloak, runId: number): void {
  if (runId !== refreshRunId) return

  clearRefreshTimer()

  const exp = kc.tokenParsed?.exp
  const timeSkew = kc.timeSkew
  if (exp == null || timeSkew == null) {
    failRefresh()
    return
  }

  // Seconds left on the 5-minute access token, adjusted for Keycloak clock skew.
  const expiresInSec = exp - Math.ceil(Date.now() / 1000) + timeSkew
  const delayMs = Math.max(0, (expiresInSec - REFRESH_EARLY_SECONDS) * 1000)

  refreshTimerId = window.setTimeout(() => {
    void (async () => {
      if (runId !== refreshRunId) return
      try {
        if (!syncTokensFromStorage(kc)) {
          failRefresh()
          return
        }
        const refreshed = await kc.updateToken(REFRESH_EARLY_SECONDS)
        // Persist before the generation check so a remount/stop during await cannot drop tokens.
        if (refreshed) persistRefreshedSession(kc)
        if (runId !== refreshRunId) return
        scheduleRefresh(kc, runId)
      } catch {
        // Keycloak returns 400 for a bad refresh token and rejects updateToken.
        // Always clear app auth — do not skip when runId changed mid-request (Strict Mode / remount).
        failRefresh()
      }
    })()
  }, delayMs)
}

export async function startTokenRefresh(
  onUpdated: (session: AuthSession | null) => void,
): Promise<void> {
  stopTokenRefresh()
  onAuthSessionUpdated = onUpdated
  const runId = refreshRunId

  const kc = await ensureKeycloakFromStorage()
  if (runId !== refreshRunId) return
  if (!kc) {
    failRefresh()
    return
  }

  scheduleRefresh(kc, runId)
}

// For protected API calls: refresh if needed, then return a usable access token.
// On any failure, clear auth the same way the timer does, then throw a consistent error.
export async function getAccessToken(): Promise<string> {
  try {
    const kc = await ensureKeycloakFromStorage()
    if (!kc?.token) {
      throw new Error('Session expired')
    }

    if (!syncTokensFromStorage(kc)) {
      throw new Error('Session expired')
    }

    const refreshed = await kc.updateToken(REFRESH_EARLY_SECONDS)
    if (refreshed) persistRefreshedSession(kc)

    if (!kc.token) {
      throw new Error('Session expired')
    }
    return kc.token
  } catch {
    failRefresh()
    throw new Error('Session expired')
  }
}
