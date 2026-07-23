// OAuth return page after Keycloak (BCSC or email OTP).
// Not a user-facing step — it finishes login, then sends the user back to /login.
import { useEffect, useState } from 'react'
import { Button, InlineAlert, Text } from '@bcgov/design-system-react-components'
import { useNavigate, useParams } from 'react-router'

import { createUser } from '~/api/users'
import { useAuth } from '~/auth/auth-context'
import { initKeycloakLogin, WrongIdpError } from '~/auth/keycloak'
import { addToSession, getFromSession, removeFromSession } from '~/auth/session'
import { isAllowedBookingIdp, SessionKeys } from '~/auth/session-keys'

export function meta() {
  return [{ title: 'Signing in' }]
}

export default function SigninCallbackPage() {
  const { idpHint } = useParams()
  const navigate = useNavigate()
  const { setSession } = useAuth()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    // Browser back can restore this page without re-running login. Send them to /login.
    function onPageShow(event: PageTransitionEvent) {
      const hasCode =
        window.location.search.includes('code=') || window.location.hash.includes('code=')
      if (event.persisted && !hasCode) {
        removeFromSession(SessionKeys.KeycloakLoginRedirectPending)
        window.location.replace('/login')
      }
    }

    window.addEventListener('pageshow', onPageShow)

    async function run() {
      // Only allowed booking IdPs (bcsc, otp) may start login from this route.
      if (!idpHint || !isAllowedBookingIdp(idpHint)) {
        removeFromSession(SessionKeys.KeycloakLoginRedirectPending)
        navigate('/login?error=idp', { replace: true })
        return
      }

      // Browser back from Keycloak lands here without an OAuth code. Without this guard,
      // login-required redirects to Keycloak again and the page appears to keep refreshing.
      const hasOAuthCode =
        window.location.search.includes('code=') || window.location.hash.includes('code=')

      if (!hasOAuthCode) {
        if (getFromSession(SessionKeys.KeycloakLoginRedirectPending) === idpHint) {
          removeFromSession(SessionKeys.KeycloakLoginRedirectPending)
          navigate('/login', { replace: true })
          return
        }
        addToSession(SessionKeys.KeycloakLoginRedirectPending, idpHint)
      }

      try {
        const session = await initKeycloakLogin(idpHint)
        removeFromSession(SessionKeys.KeycloakLoginRedirectPending)
        if (cancelled) return

        if (!session) {
          setError('Sign-in was not completed. Please try again.')
          return
        }

        setSession(session)
        // Create/update backend user; do not block moving on if this fails.
        void createUser().catch(() => {
          console.warn('[signin] POST /users/ failed; continuing with session')
        })

        navigate('/login', { replace: true })
      } catch (err) {
        removeFromSession(SessionKeys.KeycloakLoginRedirectPending)
        if (cancelled) return
        if (err instanceof WrongIdpError) {
          // Keycloak logout redirects to the login page with the IdP error.
          return
        }
        console.error('[signin] Keycloak login failed', err)
        setError('Unable to sign in. Please try again.')
      }
    }

    void run()

    return () => {
      cancelled = true
      window.removeEventListener('pageshow', onPageShow)
    }
    // Only re-run when the IdP changes. setSession/navigate are stable enough for this page.
  }, [idpHint]) // eslint-disable-line react-hooks/exhaustive-deps

  if (error) {
    return (
      <div className="sign-in-panel">
        <InlineAlert variant="danger" title="Sign-in failed">
          {error}
        </InlineAlert>
        <Button
          type="button"
          variant="secondary"
          onPress={() => navigate('/login', { replace: true })}
        >
          Back to login
        </Button>
      </div>
    )
  }

  return (
    <div className="sign-in-panel" role="status" aria-live="polite">
      <Text>Signing you in…</Text>
    </div>
  )
}
