import React from 'react'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="layout-wrapper">
      <header className="layout-header">
        <div className="header-content">
          <h1>BC Government</h1>
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
