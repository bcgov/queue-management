import '@bcgov/design-tokens/css/variables.css'
import '@bcgov/bc-sans/css/BC_Sans.css'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'

createRoot(document.getElementById('app')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
