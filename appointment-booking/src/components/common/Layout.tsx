import { Footer, Header } from '@bcgov/design-system-react-components'
import type { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <>
      <Header
        title="Service BC"
        skipLinks={[
          <a key="main" href="#main-content">
            Skip to main content
          </a>,
        ]}
      />
      <main id="main-content" className="layout-main">
        {children}
      </main>
      <Footer />
    </>
  )
}
