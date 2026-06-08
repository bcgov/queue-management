import '@bcgov/design-tokens/css/variables.css'
import '@bcgov/bc-sans/css/BC_Sans.css'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'
import { getServiceLocations, mapApiOfficesToVisibleLocations } from './data/service-locations'
import { ApiClient } from './services/api-client.service'
import { getOffices } from './services/booking-api.service'
import { loadRuntimeConfig } from './services/runtime-config.service'

const container = document.getElementById('app')!
const initialPath = `${window.location.pathname}${window.location.search}${window.location.hash}`

const root = createRoot(container)

function renderApp(locations = getServiceLocations()) {
  root.render(
    <StrictMode>
      <App initialPath={initialPath} locations={locations} />
    </StrictMode>,
  )
}

renderApp()

loadRuntimeConfig()
  .then((config) => {
    const client = new ApiClient(config)
    return getOffices(client)
  })
  .then((result) => {
    const apiLocations = mapApiOfficesToVisibleLocations(result.offices)
    if (apiLocations.length > 0) {
      renderApp(apiLocations)
    }
  })
  .catch(() => {
    // API unreachable — fixtures already showing, nothing to do.
  })
