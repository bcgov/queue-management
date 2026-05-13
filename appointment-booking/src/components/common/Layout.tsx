import React from 'react'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="layout-wrapper">
      <header className="layout-header">
        <div className="header-content">
          <picture>
            <source media="(max-width: 600px)" srcSet="/gov3_bc_logo_mobile.png" />
            <img src="/gov3_bc_logo.png" alt="BC Government Logo" className="bc-logo" />
          </picture>
        </div>
      </header>
      <main className="layout-main">{children}</main>
      <footer className="layout-footer">
        <div className="footer-content">
          <p>&copy; 2026 Province of British Columbia</p>
        </div>
      </footer>
    </div>
  )
}
