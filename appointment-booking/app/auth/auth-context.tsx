// Holds the signed-in user for the whole app (header + booking steps).
import { useCallback, useContext, useEffect, useState, type ReactNode } from 'react'

import {
  clearStoredAuthSession,
  logoutKeycloak,
  readAuthSessionFromStorage,
  type AuthSession,
  writeAuthSession,
} from './keycloak'
import { clearStoredBookingSession } from './session'
import { AuthContext } from './auth-store'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isReady, setIsReady] = useState(false)
  const [session, setSessionState] = useState<AuthSession | null>(null)

  useEffect(() => {
    // sessionStorage is browser-only, so restore it after the initial render.
    const id = window.setTimeout(() => {
      setSessionState(readAuthSessionFromStorage())
      setIsReady(true)
    }, 0)
    return () => window.clearTimeout(id)
  }, [])

  // Stable callbacks — /signin effect depends on setSession and must not re-run mid-login.
  const setSession = useCallback((next: AuthSession | null) => {
    if (next) {
      writeAuthSession(next)
    } else {
      clearStoredAuthSession()
    }
    setSessionState(next)
    setIsReady(true)
  }, [])

  const logout = useCallback(async () => {
    const logoutPromise = logoutKeycloak(`${window.location.origin}/services`)
    // Logout ends the booking attempt too — do not leave service/location for the next user.
    clearStoredAuthSession()
    clearStoredBookingSession()
    setSessionState(null)
    await logoutPromise
  }, [])

  return (
    <AuthContext.Provider
      value={{
        isReady,
        isAuthenticated: !!session?.token,
        session,
        setSession,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const value = useContext(AuthContext)
  if (!value) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return value
}
