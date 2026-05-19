import '@bcgov/design-tokens/css/variables.css'
import '@bcgov/bc-sans/css/BC_Sans.css'
import { StrictMode } from 'react'
import { hydrateRoot } from 'react-dom/client'
import './index.css'
import App from './App'

hydrateRoot(
  document.getElementById('app')!,
  <StrictMode>
    <App />
  </StrictMode>,
)
