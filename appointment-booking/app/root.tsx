import { Button, Footer, Header } from '@bcgov/design-system-react-components'
import { config } from '@fortawesome/fontawesome-svg-core'
import { isRouteErrorResponse, Links, Meta, Outlet, Scripts, ScrollRestoration } from 'react-router'

import type { Route } from './+types/root'
import { AuthProvider, useAuth } from '~/auth/auth-context'
import { BookingProvider } from '~/booking/booking-context'
import '@bcgov/design-tokens/css/variables.css'
import '@bcgov/bc-sans/css/BC_Sans.css'
import './bcds-shell.css'
import './app.css'

config.autoAddCss = false

export function Layout({ children }: { children: React.ReactNode }) {
  // Document shell only — context providers must live in the root route component,
  // not Layout, so they share the same React tree as route modules.
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" type="image/png" href="/favicon.png" />
        <Meta />
        <Links />
      </head>
      <body className="app-shell">
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BookingProvider>
        <AppShell />
      </BookingProvider>
    </AuthProvider>
  )
}

function AppShell() {
  const { isAuthenticated, session, logout } = useAuth()

  return (
    <>
      <Header
        title="Service BC"
        skipLinks={[
          <a key="main" href="#main-content">
            Skip to main content
          </a>,
        ]}
      >
        {isAuthenticated ? (
          <div className="header-account">
            <span className="header-account-name">
              Signed in as {session?.userFullName?.trim() || 'Appointment User'}
            </span>
            <Button size="small" onPress={() => void logout()}>
              Log out
            </Button>
          </div>
        ) : null}
      </Header>
      <main id="main-content" className="layout-main">
        <Outlet />
      </main>
      <Footer />
    </>
  )
}

export function ErrorBoundary({ error }: Route.ErrorBoundaryProps) {
  let message = 'Oops!'
  let details = 'An unexpected error occurred.'
  let stack: string | undefined

  if (isRouteErrorResponse(error)) {
    message = error.status === 404 ? '404' : 'Error'
    details =
      error.status === 404 ? 'The requested page could not be found.' : error.statusText || details
  } else if (import.meta.env.DEV && error && error instanceof Error) {
    details = error.message
    stack = error.stack
  }

  return (
    <main className="layout-main">
      <h1>{message}</h1>
      <p>{details}</p>
      {stack ? (
        <pre className="w-full p-4 overflow-x-auto">
          <code>{stack}</code>
        </pre>
      ) : null}
    </main>
  )
}
