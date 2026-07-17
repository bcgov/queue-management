import { createContext } from 'react'

import type { AuthSession } from './keycloak'

export type AuthContextValue = {
  isReady: boolean
  isAuthenticated: boolean
  session: AuthSession | null
  setSession: (session: AuthSession | null) => void
  logout: () => Promise<void>
}

// Isolated from component exports so Vite/Fast Refresh cannot duplicate this context.
export const AuthContext = createContext<AuthContextValue | null>(null)
