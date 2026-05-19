import '@bcgov/design-tokens/css/variables.css'
import '@bcgov/bc-sans/css/BC_Sans.css'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'
import type { ServiceLocation } from './data/service-locations'

type InitialRenderData = {
  locations?: ServiceLocation[]
}

declare global {
  interface Window {
    __APPOINTMENT_BOOKING_INITIAL_DATA__?: InitialRenderData
  }
}

const initialData = window.__APPOINTMENT_BOOKING_INITIAL_DATA__

createRoot(document.getElementById('app')!).render(
  <StrictMode>
    <App
      initialPath={`${window.location.pathname}${window.location.search}${window.location.hash}`}
      locations={initialData?.locations}
    />
  </StrictMode>,
)
